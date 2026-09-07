"""
Realistic 7-Day Coupled Smog Episode Synthetic Data Generator.
Season-aware: scales AQI from post-monsoon (Sep~130 avg) to winter peak (Nov~400 avg).
Anchored to real current date so "now" ≈ step_hour 48 (mid-episode Day 3).
"""

import math
import numpy as np
from datetime import datetime, timedelta
from .stations import STATIONS

# Major Stubble Burning Clusters in Punjab & Haryana
STUBBLE_CLUSTERS = [
    {"name": "Sangrur Central", "state": "Punjab", "lat": 30.2458, "lon": 75.8421, "weight": 0.22},
    {"name": "Bhatinda South", "state": "Punjab", "lat": 30.2110, "lon": 74.9455, "weight": 0.18},
    {"name": "Mansa Belt", "state": "Punjab", "lat": 29.9880, "lon": 75.3980, "weight": 0.14},
    {"name": "Tarn Taran North", "state": "Punjab", "lat": 31.4520, "lon": 74.9250, "weight": 0.12},
    {"name": "Patiala Rural", "state": "Punjab", "lat": 30.3398, "lon": 76.3869, "weight": 0.10},
    {"name": "Kaithal Cluster", "state": "Haryana", "lat": 29.8015, "lon": 76.3996, "weight": 0.09},
    {"name": "Fatehabad West", "state": "Haryana", "lat": 29.5150, "lon": 75.4550, "weight": 0.08},
    {"name": "Jind Agro Corridor", "state": "Haryana", "lat": 29.3140, "lon": 76.3150, "weight": 0.07},
]


def calculate_indian_aqi(pm25, pm10):
    """CPCB Indian National Air Quality Index (NAQI) formula for PM2.5 and PM10."""
    pm25_bp = [
        (0, 30, 0, 50), (31, 60, 51, 100), (61, 90, 101, 200),
        (91, 120, 201, 300), (121, 250, 301, 400), (251, 500, 401, 500)
    ]
    aqi_pm25 = 0
    for c_low, c_high, i_low, i_high in pm25_bp:
        if c_low <= pm25 <= c_high:
            aqi_pm25 = ((i_high - i_low) / (c_high - c_low)) * (pm25 - c_low) + i_low
            break
    if pm25 > 500:
        aqi_pm25 = 500 + (pm25 - 500) * 0.5

    pm10_bp = [
        (0, 50, 0, 50), (51, 100, 51, 100), (101, 250, 101, 200),
        (251, 350, 201, 300), (351, 430, 301, 400), (431, 600, 401, 500)
    ]
    aqi_pm10 = 0
    for c_low, c_high, i_low, i_high in pm10_bp:
        if c_low <= pm10 <= c_high:
            aqi_pm10 = ((i_high - i_low) / (c_high - c_low)) * (pm10 - c_low) + i_low
            break
    if pm10 > 600:
        aqi_pm10 = 500 + (pm10 - 600) * 0.4

    return int(round(max(aqi_pm25, aqi_pm10)))


def get_aqi_category(aqi):
    if aqi <= 50:
        return "Good", "#10B981"
    elif aqi <= 100:
        return "Satisfactory", "#84CC16"
    elif aqi <= 200:
        return "Moderate", "#EAB308"
    elif aqi <= 300:
        return "Poor", "#F97316"
    elif aqi <= 400:
        return "Very Poor", "#EF4444"
    else:
        return "Severe", "#7F1D1D"


def _deg_to_cardinal(d):
    dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
            "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    ix = int((d + 11.25) / 22.5)
    return dirs[ix % 16]


def _get_seasonal_scale():
    """
    Scale factor (0.0–1.0) based on current month.
    0.0 = cleanest (Aug monsoon), 1.0 = worst (Dec/Jan winter smog peak).
    September (post-monsoon tail) → ~0.25 → realistic AQI 100-170 for Delhi.
    """
    month = datetime.now().month
    scales = {
        1: 0.95, 2: 0.82, 3: 0.62, 4: 0.48,
        5: 0.52, 6: 0.46, 7: 0.18, 8: 0.16,
        9: 0.26, 10: 0.46, 11: 0.78, 12: 0.95
    }
    return scales.get(month, 0.50)


class SyntheticCoupledEpisode:
    """
    Generates 168 hours (7 days) of coupled meteorology, satellite stubble fires,
    and station pollutant records. Anchored to real current date; scales pollution
    to current season so displayed AQI values match real-world magnitudes.
    - September (monsoon tail): AQI ~100-170 range (Satisfactory/Moderate)
    - November-January (winter smog peak): AQI ~300-500 range (Poor/Severe)
    The "current" snapshot is step_hour 48 (start of Day 3 of the 7-day episode).
    """

    def __init__(self, start_date=None):
        if start_date is None:
            # Anchor so step_hour=48 ≈ "right now" (2 days ago = Day 1 of episode)
            now = datetime.now().replace(minute=0, second=0, microsecond=0)
            self.base_time = now - timedelta(hours=48)
        else:
            self.base_time = start_date

        self.total_hours = 168
        self.seasonal_scale = _get_seasonal_scale()
        self.timeline_data = self._generate_full_timeline()

    def _generate_full_timeline(self):
        timeline = []
        s = self.seasonal_scale  # 0.26 in Sep, 0.95 in winter

        for hour in range(self.total_hours):
            current_dt = self.base_time + timedelta(hours=hour)
            day = hour // 24
            # Use real wall-clock hour for diurnal cycles (traffic, temp, PBLH)
            # so 'current' snapshot (step 48 = now) shows correct time-of-day physics
            time_of_day = current_dt.hour

            # ── 1. METEOROLOGY ──────────────────────────────────────────────
            # Temperature: Sep 26-33°C, Jan 8-20°C
            temp_base_warm = 28.0
            temp_base_cold = 15.0
            temp_base = temp_base_warm * (1 - s) + temp_base_cold * s - 0.4 * day * s
            temp = temp_base + 5.0 * math.sin((time_of_day - 9) * math.pi / 12) + np.random.normal(0, 0.4)

            # Humidity: Sep monsoon residual ~70-85%, winter ~45-65%
            rh_base = 75.0 * (1 - s) + 56.0 * s
            rh = rh_base + 15.0 * math.cos((time_of_day - 4) * math.pi / 12)
            if 96 <= hour <= 143:
                rh += 10.0 * s
            rh = min(98.0, max(30.0, rh + np.random.normal(0, 1.5)))

            # Wind speed: Sep active SW monsoon winds, winter calm
            w_fast = 16.0 * (1 - s) + 13.0 * s
            w_stag = 7.0  * (1 - s) + 3.2 * s

            if hour < 48:
                wind_speed = w_fast + 3.0 * math.sin(time_of_day * math.pi / 12) + np.random.normal(0, 1.0)
            elif hour < 96:
                progress = (hour - 48) / 48.0
                wind_speed = w_fast * (1 - progress) + w_stag * progress + np.random.normal(0, 0.6)
            elif hour < 144:
                wind_speed = w_stag + 1.2 * math.sin(time_of_day * math.pi / 12) + np.random.normal(0, 0.4)
                wind_speed = max(1.5, wind_speed)
            else:
                progress = (hour - 144) / 24.0
                wind_speed = w_stag + w_fast * progress + np.random.normal(0, 1.0)

            # Wind direction: Sep = SW/W monsoon (210-250°), winter = NW stubble corridor (315°)
            if hour < 48:
                wind_dir = (220.0 * (1 - s) + 110.0 * s) + np.random.normal(0, 12.0)
            elif hour < 96:
                progress = (hour - 48) / 48.0
                base_start = 220.0 * (1 - s) + 110.0 * s
                wind_dir = base_start + progress * (315.0 - base_start) + np.random.normal(0, 8.0)
            elif hour < 144:
                wind_dir = 315.0 + np.random.normal(0, 7.0)
            else:
                wind_dir = 280.0 + np.random.normal(0, 15.0)
            wind_dir = (wind_dir + 360) % 360

            # PBLH: Sep daytime 1500-2000m (convective), winter 300-1400m (inversion)
            diurnal_pblh = 0.5 * (1.0 + math.sin((time_of_day - 8) * math.pi / 12))
            pblh_max_day   = 2000.0 * (1 - s) + 1400.0 * s
            pblh_min_night = 900.0  * (1 - s) + 550.0  * s

            if hour < 48:
                pblh = pblh_min_night + (pblh_max_day - pblh_min_night) * diurnal_pblh + np.random.normal(0, 30.0)
                inversion_strength = 0.2 * s if (time_of_day < 7 or time_of_day > 20) else 0.0
            elif hour < 96:
                progress = (hour - 48) / 48.0
                max_p = pblh_max_day * (1 - 0.45 * progress * s)
                min_p = pblh_min_night * (1 - 0.55 * progress * s)
                pblh = min_p + (max_p - min_p) * diurnal_pblh + np.random.normal(0, 20.0)
                inversion_strength = (progress * 3.5 * s) if (time_of_day < 8 or time_of_day > 19) else (progress * 0.8 * s)
            elif hour < 144:
                pblh_pk_min = 800.0 * (1 - s) + 240.0 * s
                pblh_pk_rng = 1200.0 * (1 - s) + 420.0 * s
                pblh = pblh_pk_min + pblh_pk_rng * diurnal_pblh + np.random.normal(0, 15.0)
                inversion_strength = (4.8 * s + 0.4 * (1 - s)) + 0.8 * math.cos(time_of_day * math.pi / 12) * s + np.random.normal(0, 0.2)
            else:
                progress = (hour - 144) / 24.0
                pblh = pblh_min_night + progress * 800.0 + 500.0 * diurnal_pblh + np.random.normal(0, 30.0)
                inversion_strength = max(0.0, 4.8 * s * (1 - progress))

            pblh = max(180.0, pblh)
            wind_speed_ms = (wind_speed * 1000.0) / 3600.0
            ventilation_index = wind_speed_ms * pblh

            # ── 2. STUBBLE BURNING ───────────────────────────────────────────
            # Sep: barely started (~50-200 fires), winter peak: 3000+
            fire_base = int(40  + 240  * s)
            fire_peak = int(350 + 2800 * s)

            if hour < 48:
                total_fire_count = int(fire_base + np.random.normal(0, 15 + 30 * s))
            elif hour < 96:
                progress = (hour - 48) / 48.0
                total_fire_count = int(fire_base + progress * (fire_peak - fire_base) + np.random.normal(0, 40 * s + 15))
            elif hour < 144:
                total_fire_count = int(fire_peak + 200 * s * math.sin(hour * 0.1) + np.random.normal(0, 60))
            else:
                progress = (hour - 144) / 24.0
                total_fire_count = int(fire_peak * (1 - 0.7 * progress) + np.random.normal(0, 35))
            total_fire_count = max(30, total_fire_count)

            angle_diff = abs(((wind_dir - 315) + 180) % 360 - 180)
            alignment_factor = max(0.0, math.cos(math.radians(angle_diff)))

            stubble_smoke_raw = (total_fire_count / 12.0) * alignment_factor
            trapping_multiplier = max(1.0, 3800.0 / max(ventilation_index, 600.0))
            stubble_pm25_contrib = stubble_smoke_raw * (0.4 + 0.6 * (trapping_multiplier - 1.0) / 4.0) * s

            # ── 3. STATION POLLUTANTS ────────────────────────────────────────
            stations_data = []
            station_aqi_list = []

            for st in STATIONS:
                # Realistic Delhi diurnal activity curve:
                if (8 <= time_of_day <= 11) or (18 <= time_of_day <= 22):
                    traffic_rush = 1.25
                elif 11 < time_of_day < 18:
                    traffic_rush = 1.05
                elif (6 <= time_of_day < 8) or (22 < time_of_day <= 23):
                    traffic_rush = 0.90
                else:
                    traffic_rush = 0.75

                # Calibrated to real Delhi CPCB data:
                # Sep: Janakpuri ~144 AQI (Moderate, ~73.5 µg/m³), city avg ~140-150
                # Nov-Jan smog peak: AQI 350-450 with intense trapping
                base_sep = 50.0 + st["base_pm25_bias"] * 0.70   # Sep realistic
                base_win = 65.0 + st["base_pm25_bias"]          # Winter peak
                effective_base = base_sep * (1 - s) + base_win * s
                base_local_pm25 = effective_base * traffic_rush

                # In Sep, PBLH is high so little trapping; in winter, severe trapping
                trapping_boost = 0.8 * (inversion_strength / 4.0) + (1000.0 / max(pblh, 250.0)) * 0.4 * s
                local_trapped_pm25 = base_local_pm25 * (1.0 + trapping_boost)

                nw_exposure = 1.0 + 0.18 * ((st["lat"] - 28.5) / 0.3) - 0.12 * ((st["lon"] - 77.1) / 0.3)
                stubble_station_pm25 = stubble_pm25_contrib * max(0.7, nw_exposure)

                total_pm25 = local_trapped_pm25 + stubble_station_pm25 + np.random.normal(0, 3.0)
                total_pm25 = max(10.0, total_pm25)

                dust_factor = 1.75 if not st["industrial_zone"] else 1.95
                total_pm10 = total_pm25 * dust_factor + np.random.normal(0, 7.0)
                total_pm10 = max(15.0, total_pm10)

                no2 = max(8.0, 20.0 + 0.30 * local_trapped_pm25 + np.random.normal(0, 2.0))
                so2 = max(4.0, 8.0  + 0.10 * local_trapped_pm25 + np.random.normal(0, 1.5))
                co  = round(max(0.3, 0.6 + (total_pm25 / 100.0) * 0.8), 2)
                o3  = max(10.0, 42.0 - 0.04 * total_pm25 + 18.0 * diurnal_pblh)

                aqi = calculate_indian_aqi(total_pm25, total_pm10)
                category, cat_color = get_aqi_category(aqi)
                station_aqi_list.append(aqi)

                stations_data.append({
                    "station_id": st["id"],
                    "name": st["name"],
                    "city": st["city"],
                    "region": st["region"],
                    "lat": st["lat"],
                    "lon": st["lon"],
                    "pm25": round(total_pm25, 1),
                    "pm10": round(total_pm10, 1),
                    "no2": round(no2, 1),
                    "so2": round(so2, 1),
                    "co": co,
                    "o3": round(o3, 1),
                    "aqi": aqi,
                    "category": category,
                    "category_color": cat_color,
                    "stubble_share_ugm3": round(stubble_station_pm25, 1),
                    "local_share_ugm3": round(local_trapped_pm25, 1)
                })

            avg_delhi_aqi = int(round(np.mean(station_aqi_list)))
            avg_cat, avg_color = get_aqi_category(avg_delhi_aqi)

            # ── 4. FIRE HOTSPOT VISUALIZATION ───────────────────────────────
            active_fire_hotspots = []
            for cl in STUBBLE_CLUSTERS:
                cluster_fires = int(total_fire_count * cl["weight"])
                num_pts = min(max(1, cluster_fires // 40), 5)
                for i in range(num_pts):
                    active_fire_hotspots.append({
                        "id": f"FIRE_{cl['name'][:3]}_{hour}_{i}",
                        "cluster_name": cl["name"],
                        "state": cl["state"],
                        "lat": round(cl["lat"] + np.random.normal(0, 0.06), 4),
                        "lon": round(cl["lon"] + np.random.normal(0, 0.06), 4),
                        "frp_mw": round(25.0 + 70.0 * np.random.random(), 1),
                        "confidence": int(np.random.randint(75, 100)),
                        "cluster_total_fires": cluster_fires
                    })

            # ── 5. SOURCE ATTRIBUTION ────────────────────────────────────────
            total_stubble_mass = sum(sd["stubble_share_ugm3"] for sd in stations_data)
            total_local_mass   = sum(sd["local_share_ugm3"]   for sd in stations_data)
            total_mass = max(1.0, total_stubble_mass + total_local_mass)
            stubble_pct = round((total_stubble_mass / total_mass) * 100.0, 1)
            remaining = 100.0 - stubble_pct
            vehicular_pct  = round(remaining * 0.42, 1)
            dust_pct       = round(remaining * 0.28, 1)
            industrial_pct = round(remaining * 0.20, 1)
            other_pct      = round(max(0.0, 100.0 - (stubble_pct + vehicular_pct + dust_pct + industrial_pct)), 1)

            step_record = {
                "step_hour": hour,
                "timestamp": current_dt.strftime("%Y-%m-%d %H:%M:%S"),
                "iso_timestamp": current_dt.isoformat(),
                "day_index": day + 1,
                "hour_of_day": time_of_day,
                "delhi_ncr_avg_aqi": avg_delhi_aqi,
                "category": avg_cat,
                "category_color": avg_color,
                "meteorology": {
                    "temperature_c": round(temp, 1),
                    "relative_humidity_pct": round(rh, 1),
                    "wind_speed_kmh": round(wind_speed, 1),
                    "wind_direction_deg": round(wind_dir, 1),
                    "wind_direction_cardinal": _deg_to_cardinal(wind_dir),
                    "boundary_layer_height_m": round(pblh, 1),
                    "inversion_strength_c": round(inversion_strength, 2),
                    "ventilation_index_m2s": round(ventilation_index, 1),
                    "ventilation_status": (
                        "Favorable" if ventilation_index > 3500
                        else ("Moderate" if ventilation_index > 2000
                              else "Critical Trapping (<1200 m²/s)")
                    )
                },
                "stubble_burning": {
                    "total_active_fires": total_fire_count,
                    "upwind_alignment_pct": round(alignment_factor * 100.0, 1),
                    "stubble_transport_potential": (
                        "High"     if (total_fire_count > 1500 and alignment_factor > 0.6)
                        else ("Moderate" if total_fire_count > 800
                              else "Low")
                    ),
                    "hotspots": active_fire_hotspots
                },
                "source_attribution": {
                    "stubble_burning": stubble_pct,
                    "vehicular_emissions": vehicular_pct,
                    "road_construction_dust": dust_pct,
                    "industrial_energy": industrial_pct,
                    "secondary_and_domestic": other_pct
                },
                "stations": stations_data
            }
            timeline.append(step_record)

        return timeline

    def get_step(self, hour):
        hour = max(0, min(self.total_hours - 1, hour))
        return self.timeline_data[hour]

    def get_full_timeline(self):
        return self.timeline_data


# Singleton instance for quick access
SYNTHETIC_DATASET = SyntheticCoupledEpisode()
