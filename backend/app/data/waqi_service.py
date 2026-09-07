"""
WAQI (World Air Quality Index) Live Real-Time Data Service.
Fetches official CPCB/DPCC ground station air quality telemetry across Delhi NCR.
Provides spatial mapping to the 58 CAAQMS monitoring network with in-memory caching.
"""

import os
import time
import math
import json
import logging
import urllib.request
from typing import Dict, Any, List, Optional
from .stations import STATIONS_DATA

logger = logging.getLogger("waqi_service")

DEFAULT_WAQI_TOKEN = "64804e6a2aa6b6bea50aeb7ada6733af50cca796"

def get_waqi_token() -> str:
    return (
        os.getenv("WAQI_API_TOKEN")
        or os.getenv("WAQI_API_KEY")
        or DEFAULT_WAQI_TOKEN
    ).strip()

def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Computes distance between two coordinate pairs in kilometers."""
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)

def get_aqi_category(aqi: int) -> Dict[str, str]:
    if aqi <= 50:
        return {"category": "Good", "color": "#8FFFB0", "grap_stage": "Stage 0", "severity": "Normal"}
    elif aqi <= 100:
        return {"category": "Satisfactory", "color": "#7FD4FF", "grap_stage": "Stage 0", "severity": "Normal"}
    elif aqi <= 200:
        return {"category": "Moderate", "color": "#FFE270", "grap_stage": "Stage I", "severity": "Moderate"}
    elif aqi <= 300:
        return {"category": "Poor", "color": "#FFAE5E", "grap_stage": "Stage II", "severity": "Poor"}
    elif aqi <= 400:
        return {"category": "Very Poor", "color": "#FF7B6B", "grap_stage": "Stage III", "severity": "High Alert"}
    elif aqi <= 450:
        return {"category": "Severe", "color": "#FF5252", "grap_stage": "Stage IV", "severity": "Emergency"}
    else:
        return {"category": "Severe+", "color": "#D32F2F", "grap_stage": "Stage IV+", "severity": "Public Health Emergency"}

class WaqiService:
    def __init__(self, cache_ttl_seconds: int = 300):
        self.cache_ttl = cache_ttl_seconds
        self._cached_bounds_data: Optional[List[Dict[str, Any]]] = None
        self._cached_bounds_time: float = 0.0
        self._cached_geo_data: Dict[str, Dict[str, Any]] = {}

    def fetch_delhi_ncr_bounds(self) -> List[Dict[str, Any]]:
        """
        Fetches all active WAQI monitors within the Delhi-NCR bounding box.
        Cached for 5 minutes.
        """
        now = time.time()
        if self._cached_bounds_data and (now - self._cached_bounds_time < self.cache_ttl):
            return self._cached_bounds_data

        token = get_waqi_token()
        # Bounding box covering Delhi NCT and entire NCR periphery: lat 28.1 to 29.1, lon 76.6 to 77.8
        url = f"https://api.waqi.info/map/bounds/?latlng=28.1,76.6,29.1,77.8&token={token}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "VayuCoupler-MoES/1.0"})
            with urllib.request.urlopen(req, timeout=6) as response:
                raw = json.loads(response.read().decode("utf-8"))
                if raw.get("status") == "ok":
                    stations = []
                    for item in raw.get("data", []):
                        try:
                            aqi_val = int(item.get("aqi"))
                            stations.append({
                                "uid": item.get("uid"),
                                "name": item.get("station", {}).get("name", "Unknown Station"),
                                "lat": float(item.get("lat")),
                                "lon": float(item.get("lon")),
                                "aqi": aqi_val,
                                "time": item.get("station", {}).get("time")
                            })
                        except (ValueError, TypeError):
                            continue
                    if stations:
                        self._cached_bounds_data = stations
                        self._cached_bounds_time = now
                        return stations
        except Exception as e:
            logger.warning(f"Failed to fetch WAQI bounds data: {e}")

        # Return stale cache if available
        if self._cached_bounds_data:
            return self._cached_bounds_data
        return []

    def fetch_geo_feed(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        """
        Fetches live WAQI feed for an arbitrary GPS coordinate.
        """
        cache_key = f"{round(lat, 3)}_{round(lon, 3)}"
        now = time.time()
        if cache_key in self._cached_geo_data:
            entry = self._cached_geo_data[cache_key]
            if now - entry["time"] < self.cache_ttl:
                return entry["data"]

        token = get_waqi_token()
        url = f"https://api.waqi.info/feed/geo:{lat};{lon}/?token={token}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "VayuCoupler-MoES/1.0"})
            with urllib.request.urlopen(req, timeout=6) as response:
                raw = json.loads(response.read().decode("utf-8"))
                if raw.get("status") == "ok":
                    data = raw.get("data", {})
                    aqi = data.get("aqi")
                    if isinstance(aqi, (int, float)):
                        aqi = int(aqi)
                    else:
                        aqi = None

                    iaqi = data.get("iaqi", {})
                    result = {
                        "aqi": aqi,
                        "station_name": data.get("city", {}).get("name"),
                        "geo": data.get("city", {}).get("geo"),
                        "dominant_pollutant": data.get("dominentpol", "pm25"),
                        "pm25": iaqi.get("pm25", {}).get("v"),
                        "pm10": iaqi.get("pm10", {}).get("v"),
                        "temperature": iaqi.get("t", {}).get("v"),
                        "humidity": iaqi.get("h", {}).get("v"),
                        "wind_speed": iaqi.get("w", {}).get("v"),
                        "no2": iaqi.get("no2", {}).get("v"),
                        "so2": iaqi.get("so2", {}).get("v"),
                        "co": iaqi.get("co", {}).get("v"),
                        "o3": iaqi.get("o3", {}).get("v"),
                        "timestamp": data.get("time", {}).get("s"),
                        "attributions": data.get("attributions", [])
                    }
                    self._cached_geo_data[cache_key] = {"data": result, "time": now}
                    return result
        except Exception as e:
            logger.warning(f"Failed to fetch WAQI geo feed for {lat},{lon}: {e}")
        return None

    def get_live_stations(self) -> List[Dict[str, Any]]:
        """
        Maps live WAQI station data onto the full 58 CAAQMS stations network.
        For each station, attaches live AQI from nearest WAQI monitor or exact match.
        """
        waqi_list = self.fetch_delhi_ncr_bounds()
        result_stations = []

        for st in STATIONS_DATA:
            st_copy = dict(st)
            if waqi_list:
                # Find nearest WAQI monitor
                nearest = min(waqi_list, key=lambda w: haversine(st["lat"], st["lon"], w["lat"], w["lon"]))
                dist = haversine(st["lat"], st["lon"], nearest["lat"], nearest["lon"])
                
                # Check for direct name match in WAQI list
                direct_match = next((w for w in waqi_list if st["name"].lower() in w["name"].lower() or w["name"].lower() in st["name"].lower()), None)
                chosen = direct_match if direct_match else nearest
                chosen_dist = 0.0 if direct_match else dist

                live_aqi = chosen["aqi"]
                meta = get_aqi_category(live_aqi)

                st_copy["aqi"] = live_aqi
                st_copy["baseAQI"] = live_aqi
                st_copy["zone"] = st.get("zone") or st.get("region") or "Delhi"
                st_copy["region"] = st.get("region") or st.get("zone") or "Delhi"
                st_copy["is_live"] = True
                st_copy["live_source"] = chosen["name"]
                st_copy["live_dist_km"] = chosen_dist
                st_copy["category"] = meta["category"]
                st_copy["category_color"] = meta["color"]
                st_copy["grap_stage"] = meta["grap_stage"]

                # Calibrate pollutant estimates if not present
                if "pm25" not in st_copy or st_copy.get("is_live"):
                    st_copy["pm25"] = max(15, int(live_aqi * 0.65))
                if "pm10" not in st_copy or st_copy.get("is_live"):
                    st_copy["pm10"] = max(25, int(live_aqi * 0.95))
            else:
                # Offline / Fallback
                base = st.get("baseAQI", 380)
                meta = get_aqi_category(base)
                st_copy["aqi"] = base
                st_copy["zone"] = st.get("zone") or st.get("region") or "Delhi"
                st_copy["region"] = st.get("region") or st.get("zone") or "Delhi"
                st_copy["is_live"] = False
                st_copy["category"] = meta["category"]
                st_copy["category_color"] = meta["color"]
                st_copy["grap_stage"] = meta["grap_stage"]

            result_stations.append(st_copy)

        return result_stations

    def get_zones_summary(self) -> List[Dict[str, Any]]:
        """
        Returns live calculated AQI averages and station counts for the 7 Delhi NCR Regional Zones.
        """
        stations = self.get_live_stations()
        zones_cfg = [
            {"id": "west_delhi", "name": "West Delhi", "filter": "West Delhi", "pred": lambda z: "West" in z and "South" not in z and "North" not in z},
            {"id": "north_delhi", "name": "North Delhi", "filter": "North Delhi", "pred": lambda z: "North" in z},
            {"id": "east_delhi", "name": "East Delhi", "filter": "East Delhi", "pred": lambda z: "East" in z and "North" not in z and "South" not in z},
            {"id": "south_delhi", "name": "South Delhi", "filter": "South Delhi", "pred": lambda z: "South" in z and "West" not in z},
            {"id": "central_delhi", "name": "Central Delhi", "filter": "Central Delhi", "pred": lambda z: "Central" in z},
            {"id": "sw_delhi", "name": "SW Delhi", "filter": "South West Delhi", "pred": lambda z: "South West" in z or "SW" in z},
            {"id": "ncr_fringe", "name": "NCR Fringe", "filter": "NCR", "pred": lambda z: z.startswith("NCR") or "Delhi" not in z},
        ]
        result = []
        for zc in zones_cfg:
            matched = [s for s in stations if zc["pred"](s.get("zone") or s.get("region") or "")]
            aqis = [s["aqi"] for s in matched if isinstance(s.get("aqi"), (int, float))]
            avg_aqi = round(sum(aqis) / len(aqis)) if aqis else 160
            cat_meta = get_aqi_category(avg_aqi)
            result.append({
                "id": zc["id"],
                "name": zc["name"],
                "filter_zone": zc["filter"],
                "avg_aqi": avg_aqi,
                "category": cat_meta["category"],
                "category_color": cat_meta["color"],
                "grap_stage": cat_meta["grap_stage"],
                "stations_count": len(matched)
            })
        return result

    def get_live_station_by_id(self, station_id: str) -> Dict[str, Any]:
        stations = self.get_live_stations()
        for s in stations:
            if s["id"] == station_id or s["name"].lower() == station_id.lower():
                return s
        return stations[0]

    def get_delhi_summary(self) -> Dict[str, Any]:
        stations = self.get_live_stations()
        if not stations:
            return {
                "status": "OFFLINE",
                "average_aqi": 380,
                "category": "Very Poor",
                "category_color": "#FF7B6B",
                "active_stations": 0,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }

        aqi_values = [s["aqi"] for s in stations if isinstance(s.get("aqi"), (int, float))]
        avg_aqi = round(sum(aqi_values) / len(aqi_values)) if aqi_values else 380
        meta = get_aqi_category(avg_aqi)

        return {
            "status": "ONLINE",
            "provider": "World Air Quality Index (WAQI / CPCB)",
            "average_aqi": avg_aqi,
            "max_aqi": max(aqi_values) if aqi_values else avg_aqi,
            "min_aqi": min(aqi_values) if aqi_values else avg_aqi,
            "category": meta["category"],
            "category_color": meta["color"],
            "grap_stage": meta["grap_stage"],
            "active_stations_count": len(stations),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }

# Global singleton
WAQI_SERVICE = WaqiService()
