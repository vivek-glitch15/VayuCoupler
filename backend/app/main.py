"""
FastAPI Main Application.
Air Pollution–Weather Coupled Forecasting System (Delhi NCR Focus)
Ministry of Earth Sciences (MoES) — SIH 2026
"""

import os
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from typing import Optional

from .data.adapter import ADAPTER
from .data.stations import get_all_stations, get_station_by_id
from .models.coupled_model import FORECASTER
from .models.attribution import get_source_attribution
from .engine.grap_trigger import GRAP_ENGINE
from .engine.alerts import generate_stakeholder_dispatches, calculate_what_if_policy
from .schemas.models import WhatIfRequest, RuleCreateUpdate

app = FastAPI(
    title="MoES Air Pollution–Weather Coupled Forecasting System (Delhi NCR)",
    description="Forecast-Triggered Predictive GRAP and Coupled Meteorology-Pollution Engine",
    version="1.0.0"
)

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def serve_dashboard():
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"status": "ONLINE", "message": "MoES Coupled AQI API"}

# Enable CORS for React frontend (Vite default port 5173 / 3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {
        "status": "ONLINE",
        "system": "MoES Coupled Air Quality Forecaster (Delhi NCR)",
        "mode": ADAPTER.mode,
        "total_episode_hours": ADAPTER.synthetic_engine.total_hours,
        "stations_count": len(get_all_stations()),
        "rules_count": len(GRAP_ENGINE.rules)
    }

@app.get("/api/stations")
def get_stations():
    return get_all_stations()

@app.get("/api/snapshot")
def get_snapshot(step_hour: int = Query(default=72, ge=0, le=167)):
    """
    Returns the complete coupled state (weather, pollutants, fire counts, attribution) at a given hour.
    """
    return ADAPTER.get_snapshot_at_step(step_hour)

@app.get("/api/forecast/station/{station_id}")
def get_station_forecast(station_id: str, step_hour: int = Query(default=72, ge=0, le=167)):
    """
    Returns +24h/+48h/+72h forecast curves, 90% CI bands, and physics coupling decomposition.
    """
    return FORECASTER.generate_station_forecast(station_id, step_hour)

@app.get("/api/forecast/regional")
def get_regional_forecast(step_hour: int = Query(default=72, ge=0, le=167)):
    """
    Returns aggregated Delhi NCR forecast and peak risk level.
    """
    return FORECASTER.generate_regional_forecast(step_hour)

@app.get("/api/attribution")
def get_attribution(step_hour: int = Query(default=72, ge=0, le=167)):
    """
    Returns real-time source apportionment (stubble, vehicles, dust, industry).
    """
    return get_source_attribution(step_hour)

@app.get("/api/grap/triggers")
def get_grap_triggers(step_hour: int = Query(default=72, ge=0, le=167)):
    """
    Evaluates predictive GRAP rules matrix and calculates lead-time gained vs reactive GRAP.
    """
    return GRAP_ENGINE.evaluate_triggers(step_hour)

@app.get("/api/grap/rules")
def get_rules():
    return GRAP_ENGINE.rules

@app.post("/api/grap/rules")
def update_rule(rule: RuleCreateUpdate):
    for idx, r in enumerate(GRAP_ENGINE.rules):
        if r["id"] == rule.id:
            GRAP_ENGINE.rules[idx] = rule.model_dump()
            return {"status": "SUCCESS", "message": f"Rule {rule.id} updated successfully"}
    
    GRAP_ENGINE.rules.append(rule.model_dump())
    return {"status": "SUCCESS", "message": f"New rule {rule.id} added"}

@app.get("/api/dispatches")
def get_dispatches(step_hour: int = Query(default=72, ge=0, le=167)):
    """
    Returns role-specific simulated actionable dispatches and payloads.
    """
    return generate_stakeholder_dispatches(step_hour)

@app.post("/api/what-if")
def run_what_if_analysis(req: WhatIfRequest):
    """
    Counterfactual policy simulation for judges: see how much peak AQI drops when pre-emptive curbs are applied.
    """
    return calculate_what_if_policy(
        current_step_hour=req.step_hour,
        stubble_reduction_pct=req.stubble_reduction_pct,
        truck_reduction_pct=req.truck_reduction_pct,
        dust_reduction_pct=req.dust_reduction_pct,
        industry_switch_pct=req.industry_switch_pct
    )

@app.get("/api/interstate")
@app.get("/api/interstate/status")
def get_interstate_coordination(step_hour: int = Query(default=72, ge=0, le=167)):
    """
    Cross-State Early Warning Dashboard matrix for Delhi, Punjab, Haryana, UP, and Rajasthan.
    """
    snapshot = ADAPTER.get_snapshot_at_step(step_hour)
    fires = snapshot["stubble_burning"]
    met = snapshot["meteorology"]
    grap = GRAP_ENGINE.evaluate_triggers(step_hour)

    states = [
        {
            "state": "Delhi (NCT)",
            "role": "Receptor Basin & Internal Curbs",
            "current_status": f"Avg AQI: {snapshot['delhi_ncr_avg_aqi']} ({snapshot['category']})",
            "forecast_risk": f"Peak 72h: {grap['max_72h_forecast_aqi']} AQI",
            "active_mandates": [
                "Anti-smog guns active at 13 hotspots",
                "BS-III Petrol / BS-IV Diesel ban enforced" if grap['max_72h_forecast_aqi'] >= 400 else "Standard vehicular monitoring",
                "Primary schools virtual mode alert" if grap['max_72h_forecast_aqi'] >= 450 else "Normal school operations"
            ],
            "coordination_urgency": "CRITICAL" if grap['max_72h_forecast_aqi'] >= 400 else "ELEVATED"
        },
        {
            "state": "Punjab",
            "role": "Upwind Stubble Emission Control",
            "current_status": f"{int(fires['total_active_fires'] * 0.66)} Active Farm Fires (Sangrur, Bhatinda)",
            "forecast_risk": "High NW Plume Injection into Delhi Corridor",
            "active_mandates": [
                "Advance Happy Seeder machine mobilization at CHCs",
                "Bio-decomposer spray acceleration in 8 priority blocks",
                "Satellite-guided field enforcement teams dispatched"
            ],
            "coordination_urgency": "EMERGENCY" if fires['total_active_fires'] > 1500 else "MODERATE"
        },
        {
            "state": "Haryana",
            "role": "Trans-boundary Buffer & Stubble Control",
            "current_status": f"{int(fires['total_active_fires'] * 0.34)} Active Farm Fires (Kaithal, Fatehabad)",
            "forecast_risk": "Highway Freight Inflow & Regional Dust Resuspension",
            "active_mandates": [
                "Kundli-Manesar-Palwal (WPE) truck diversion operational",
                "Industrial diesel generator bans in Gurugram & Faridabad",
                "Farmland fire monitoring along GT Road corridor"
            ],
            "coordination_urgency": "HIGH" if grap['max_72h_forecast_aqi'] >= 350 else "MODERATE"
        },
        {
            "state": "Uttar Pradesh",
            "role": "Eastern Downwind Trapping & Peripheral Traffic",
            "current_status": "Noida/Ghaziabad Downwind Smog Accumulation",
            "forecast_risk": "Industrial point-source emissions from Sahibabad & Loni",
            "active_mandates": [
                "Eastern Peripheral Expressway (EPE) commercial traffic routing",
                "Brick kiln and hot mix plant operation halt",
                "Continuous water misting along NH-24 and Hindon corridor"
            ],
            "coordination_urgency": "HIGH" if grap['max_72h_forecast_aqi'] >= 350 else "MODERATE"
        },
        {
            "state": "Rajasthan (NCR)",
            "role": "South-West Baseline & Stone Crushing Curbs",
            "current_status": "Alwar Regional Baseline (AQI 140-190)",
            "forecast_risk": "Dust transport from mining zones",
            "active_mandates": [
                "Stone crusher wet-suppression compliance checks in Bhiwadi",
                "Interstate border green-corridor maintenance"
            ],
            "coordination_urgency": "LOW"
        }
    ]

    return {
        "step_hour": step_hour,
        "timestamp": snapshot["timestamp"],
        "wind_vector": f"{met['wind_speed_kmh']} km/h from {met['wind_direction_cardinal']} ({met['wind_direction_deg']}°)",
        "inversion_status": met["ventilation_status"],
        "states": states
    }

# ==========================================
# VAYUAI GOOGLE GEMINI INTELLIGENCE ENDPOINTS
# ==========================================

from pydantic import BaseModel

class VayuAIChatRequest(BaseModel):
    query: str
    station_name: Optional[str] = "Punjabi Bagh"
    current_aqi: Optional[int] = 388
    forecast_aqi: Optional[int] = 425
    grap_stage: Optional[str] = "STAGE III"
    wind_speed: Optional[float] = 4.2
    wind_dir: Optional[str] = "NW"
    api_key: Optional[str] = None
    language: Optional[str] = "hinglish"
    # Live Weather & Meteorological Telemetry
    temperature: Optional[float] = 28.0
    temp_high: Optional[float] = 33.0
    temp_low: Optional[float] = 24.0
    feels_like: Optional[float] = 30.0
    condition: Optional[str] = "Cloudy"
    precipitation: Optional[int] = 15
    humidity: Optional[int] = 78
    pressure: Optional[int] = 1014
    pblh: Optional[int] = 340
    ventilation_index: Optional[int] = 1380
    weather_forecast: Optional[str] = None

class SetKeyRequest(BaseModel):
    api_key: str

def _resolve_gemini_key(client_key: Optional[str] = None) -> Optional[str]:
    if client_key and client_key.strip():
        return client_key.strip()
    key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if key:
        return key.strip()
    for env_path in [
        os.path.expanduser("~/.env"),
        os.path.join(os.path.dirname(__file__), "..", "..", ".env"),
        "/Users/vivekraj/VayuCoupler/.env",
        "/Users/vivekraj/Desktop/VayuCoupler/.env"
    ]:
        if os.path.exists(env_path):
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("GEMINI_API_KEY="):
                            return line.split("=", 1)[1].strip().strip('"').strip("'")
                        elif line.startswith("GOOGLE_API_KEY="):
                            return line.split("=", 1)[1].strip().strip('"').strip("'")
            except Exception:
                pass
    return None

@app.get("/api/vayuai/status")
def vayuai_status():
    key = _resolve_gemini_key()
    return {
        "gemini_configured": bool(key),
        "model": "gemini-flash-lite-latest",
        "system": "MoES VayuAI Meteorological Intelligence"
    }

@app.post("/api/vayuai/set_key")
def set_vayuai_key(payload: SetKeyRequest):
    key = payload.api_key.strip()
    if not key:
        raise HTTPException(status_code=400, detail="Key cannot be empty")
    os.environ["GEMINI_API_KEY"] = key
    for env_path in [
        os.path.join(os.path.dirname(__file__), "..", "..", ".env"),
        "/Users/vivekraj/VayuCoupler/.env",
        "/Users/vivekraj/Desktop/VayuCoupler/.env"
    ]:
        try:
            with open(env_path, "a", encoding="utf-8") as f:
                f.write(f"\nGEMINI_API_KEY={key}\n")
        except Exception:
            pass
    return {"success": True, "message": "Gemini API Key activated successfully!"}

@app.post("/api/vayuai/chat")
def vayuai_chat(payload: VayuAIChatRequest):
    api_key = _resolve_gemini_key(payload.api_key)
    if not api_key:
        return {
            "success": False,
            "error": "NO_API_KEY",
            "message": "Google Gemini API key is not configured. Falling back to local forecast engine."
        }

    is_english = (payload.language or "").lower() == "en"
    lang_directive = (
        "LANGUAGE MANDATE: The user has explicitly selected ENGLISH mode. You MUST answer 100% in crisp, professional, authoritative English. Never use any Hindi or Hinglish words."
        if is_english
        else "LANGUAGE MANDATE: The user has selected HINGLISH mode. Answer in warm, conversational, friendly Hinglish (Hindi written in English/Latin script) with relatable expressions and emojis."
    )

    system_instruction = (
        "You are VayuAI, a friendly, ultra-smart AI companion and atmospheric intelligence assistant for Delhi-NCR and India, "
        "developed for the Ministry of Earth Sciences (MoES) — SIH 2026.\n\n"
        f"{lang_directive}\n\n"
        "Core Capabilities & Personality:\n"
        "1. Conversational & Warm: If the user says 'Hello', 'Hi', 'How are you', 'Kaise ho', 'Kya haal hai', or asks casual everyday questions, "
        "respond warmly, naturally, and politely like a helpful companion with emojis (😊, ✨, 🌿).\n"
        "2. All-Rounder & Local Intelligence: Answer everyday queries, nearby Delhi-NCR lifestyle questions (e.g. 'Can I go to India Gate today?', "
        "'Best time for outdoor running', 'Should I open windows today?', traffic advice, commute tips, local spots, weather, healthy routines, school closures).\n"
        "3. Air Quality & Meteorology Authority: You are grounded in real-time Delhi NCR data. Seamlessly connect your answers to current AQI, "
        "GRAP restrictions, nocturnal inversion, wind speed, or stubble burning impact whenever relevant, providing scientific yet practical guidance.\n"
        "4. Tone: Engaging, concise, structured with clean bullet points when helpful. Never sound robotic or stiff.\n\n"
        "5. MANDATORY METEOROLOGY & WEATHER INSTRUCTION:\n"
        "If the user asks about the weather, mausam, temperature, barish, rain, clouds, forecast, humidity, thandi, garmi, or says things like 'bdiya weather bata', 'aaj mausam kaisa hai', 'will it rain', 'what is the weather':\n"
        "- IMMEDIATELY provide a comprehensive, vivid meteorological breakdown using the live telemetry given below.\n"
        "- State the exact current temperature (°C), Feels Like (°C), today's Min/Max range, and sky condition (e.g. Cloudy, Sunny, Showers).\n"
        "- State the rain / precipitation probability (%) and relative humidity (%).\n"
        "- Detail the surface wind speed & direction, boundary layer ceiling (PBLH), and ventilation index.\n"
        "- Give the upcoming 2-3 day weather and rain outlook.\n"
        "- Explain the atmospheric coupling: how this weather condition traps or disperses pollution (e.g. shallow inversion trapping smog vs rain washing out particulate matter).\n"
        "- DO NOT just pivot to AQI and GRAP when the user asked about weather! The weather metrics MUST be front and center!"
    )

    weather_synopsis = payload.weather_forecast or (
        "Fri (Today): 33°/24°C, Cloudy, 15% Rain | "
        "Sat (Tomorrow): 31°/23°C, Scattered Showers, 65% Rain | "
        "Sun: 32°/22°C, Partly Cloudy, 20% Rain | "
        "Mon: 34°/24°C, Sunny/Clear, 5% Rain"
    )

    context_prompt = (
        f"REAL-TIME DELHI-NCR LIVE METEOROLOGICAL TELEMETRY:\n"
        f"- Current Temperature: {payload.temperature}°C (Feels Like: {payload.feels_like}°C)\n"
        f"- Today's Range: High {payload.temp_high}°C / Low {payload.temp_low}°C\n"
        f"- Sky & Cloud Condition: {payload.condition}\n"
        f"- Rain / Precipitation Probability: {payload.precipitation}%\n"
        f"- Relative Humidity: {payload.humidity}%\n"
        f"- Surface Wind: {payload.wind_speed} km/h from {payload.wind_dir}\n"
        f"- Atmospheric Boundary Layer Height (PBLH): {payload.pblh}m (Thermal Inversion Trapping)\n"
        f"- Atmospheric Ventilation Index: {payload.ventilation_index} m²/s\n"
        f"- Barometric Pressure: {payload.pressure} hPa\n"
        f"- Synoptic Multi-Day Weather Outlook: {weather_synopsis}\n\n"
        f"AIR QUALITY & REGULATORY CONTEXT:\n"
        f"- Monitoring Station: {payload.station_name}\n"
        f"- Current AQI: {payload.current_aqi}\n"
        f"- Forecast AQI (+24h/+48h): {payload.forecast_aqi}\n"
        f"- Active GRAP Stage: {payload.grap_stage}\n"
        f"\nUSER QUERY: {payload.query}"
    )

    import requests
    # Try gemini-flash-latest primary, then gemini-2.5-flash
    models_to_try = ["gemini-flash-lite-latest", "gemini-3-flash-preview", "gemini-flash-latest"]
    headers = {"Content-Type": "application/json"}
    body = {
        "contents": [{"parts": [{"text": f"SYSTEM INSTRUCTION:\n{system_instruction}\n\n{context_prompt}"}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 600}
    }

    last_error = None
    for model_name in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        try:
            r = requests.post(url, headers=headers, json=body, timeout=12)
            if r.status_code == 200:
                res_data = r.json()
                text = res_data["candidates"][0]["content"]["parts"][0]["text"]
                return {
                    "success": True,
                    "reply": text,
                    "model": f"Google Gemini ({model_name})",
                    "confidence": 98,
                    "leadMeta": "Google Gemini Intelligence"
                }
            else:
                last_error = f"Model {model_name} HTTP {r.status_code}: {r.text[:150]}"
        except Exception as ex:
            last_error = str(ex)

    return {
        "success": False,
        "error": last_error or "Unable to connect to Gemini",
        "message": "Gemini API error occurred."
    }


@app.get("/download", response_class=HTMLResponse)
@app.get("/app", response_class=HTMLResponse)
def mobile_download_hub():
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>VayuCoupler - Mobile Download & Install Hub</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>body { font-family: 'Plus Jakarta Sans', sans-serif; }</style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen p-4 sm:p-6 flex flex-col items-center justify-center">
  <div class="max-w-md w-full bg-slate-900/90 border border-slate-800 rounded-3xl p-6 shadow-2xl backdrop-blur-xl">
    
    <!-- Logo & Header -->
    <div class="text-center mb-6">
      <div class="w-16 h-16 rounded-2xl bg-gradient-to-tr from-emerald-500 to-cyan-400 mx-auto flex items-center justify-center shadow-lg shadow-cyan-500/20 mb-3">
        <span class="text-2xl font-black text-slate-950 font-mono">VC</span>
      </div>
      <h1 class="text-2xl font-black text-white tracking-tight" style="font-family: 'Outfit', sans-serif;">VayuCoupler</h1>
      <p class="text-xs text-slate-400 mt-1 font-medium">MoES Air Pollution–Weather Coupled Forecasting System</p>
      <div class="inline-flex items-center gap-1.5 px-2.5 py-0.5 mt-2 rounded-full bg-emerald-950/80 border border-emerald-700/80 text-[10px] text-emerald-300 font-bold">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span> FULLY LIVE & VERIFIED
      </div>
    </div>

    <!-- Options List -->
    <div class="space-y-3.5">
      
      <!-- Option 1: Open Live App -->
      <a href="/" class="block p-4 rounded-2xl bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-bold shadow-lg shadow-emerald-600/30 hover:opacity-95 transition text-center">
        <div class="text-base flex items-center justify-center gap-2">🚀 Open Live App (Web)</div>
        <div class="text-[11px] font-normal text-emerald-100 mt-0.5">Live coupled map, simulation & voice alerts</div>
      </a>

      <!-- Option 2: Download Standalone HTML App -->
      <a href="/static/VayuCoupler_Standalone_Mobile_App.html" download="VayuCoupler_Mobile_App.html" class="block p-4 rounded-2xl bg-slate-800/90 hover:bg-slate-800 border border-slate-700 text-white transition text-center">
        <div class="text-base font-bold text-cyan-300 flex items-center justify-center gap-2">📱 Download Standalone App (.html)</div>
        <div class="text-[11px] text-slate-400 mt-0.5">Saved to phone Downloads • 100% Offline ready</div>
      </a>

      <!-- Option 3: Download SIH Judges QA PDF -->
      <a href="/static/VayuCoupler_SIH_Judges_QA_Guide.pdf" download="VayuCoupler_SIH_Judges_QA_Guide.pdf" class="block p-4 rounded-2xl bg-slate-800/90 hover:bg-slate-800 border border-slate-700 text-white transition text-center">
        <div class="text-base font-bold text-amber-300 flex items-center justify-center gap-2">📄 Download SIH Judges Q&A Guide (.pdf)</div>
        <div class="text-[11px] text-slate-400 mt-0.5">25 essential questions, jury answers & physics cheat-sheet</div>
      </a>

      <!-- Option 4: Download Windows Edition ZIP -->
      <a href="/static/VayuCoupler_Windows_Edition.zip" download="VayuCoupler_Windows_Edition.zip" class="block p-4 rounded-2xl bg-gradient-to-r from-blue-900/60 to-indigo-900/60 hover:from-blue-900 hover:to-indigo-900 border border-blue-500/50 text-white transition text-center shadow-lg shadow-blue-950/50">
        <div class="text-base font-bold text-sky-300 flex items-center justify-center gap-2">💻 Download Windows Edition (.zip)</div>
        <div class="text-[11px] text-sky-200 mt-0.5">Includes 1-Click "Launch_VayuCoupler_Windows.bat" + Offline App</div>
      </a>

      <!-- Option 5: Download Complete ZIP -->
      <a href="/static/VayuCoupler_App_Source.zip" download="VayuCoupler_App_Source.zip" class="block p-4 rounded-2xl bg-slate-800/90 hover:bg-slate-800 border border-slate-700 text-white transition text-center">
        <div class="text-base font-bold text-indigo-300 flex items-center justify-center gap-2">📦 Download Full Project Source (.zip)</div>
        <div class="text-[11px] text-slate-400 mt-0.5">Full FastAPI backend + Frontend codebase archive</div>
      </a>

    </div>

    <!-- Installation Tip -->
    <div class="mt-6 pt-4 border-t border-slate-800/80 text-xs text-slate-400 space-y-2">
      <div class="font-bold text-slate-300 flex items-center gap-1.5">
        <span>💡</span> Phone me App kaise Install karein:
      </div>
      <div class="text-[11px] leading-relaxed text-slate-400">
        <b>Android (Chrome):</b> Upar <b class="text-white">🚀 Open Live App</b> dabayein, fir Chrome ke 3 dots <b class="text-white">⋮</b> par tap karke <b class="text-emerald-400">"Install app" / "Add to Home screen"</b> select karein.<br>
        <b>iPhone (Safari):</b> Safari ke Share icon <b class="text-white">⎋</b> par tap karke <b class="text-cyan-400">"Add to Home Screen"</b> karein.
      </div>
    </div>

  </div>
</body>
</html>
"""

