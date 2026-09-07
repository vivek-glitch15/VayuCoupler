# 🚀 VayuCoupler Deployment Guide: Render & Vercel

This guide provides instructions for deploying **VayuCoupler** with zero watermarks, zero forced badges, and maximum performance.

---

## 🏛️ Architecture Overview

VayuCoupler is an Air Pollution–Weather Coupled Forecasting System developed for MoES (SIH 2026):
1. **Python FastAPI Backend**: Runs physics models, WRF-Chem simulation playback, predictive GRAP triggers, and Google Gemini 2.5 Flash atmospheric intelligence.
2. **Interactive Command Center Dashboard**: Integrated single-page application with Leaflet spatial wind streamlines, 7-day synoptic weather curves, and dynamic source attribution.

---

## ⚡ Primary Deployment: Render (All-in-One Full-Stack)

Render runs both the **Python Backend** and serves the **Interactive Frontend** directly on the same domain with **zero watermarks, zero badges, and zero CORS issues**.

- **Live URL**: `https://vayucoupler-9sfi.onrender.com`
- **Interactive API Docs**: `https://vayucoupler-9sfi.onrender.com/docs`

### Configuration Files:
- `render.yaml`: Blueprint definition for the web service.
- `requirements.txt`: Python package dependencies.
- `run.py`: Single-command local and server launcher.

---

## 🌐 Optional Alternative: Vercel (Clean Edge CDN)

If you want an independent Global Edge CDN for the frontend without any watermarks or footer badges:

1. Go to [vercel.com](https://vercel.com) and log in with GitHub.
2. Click **Add New...** → **Project** and select `vivek-glitch15/VayuCoupler`.
3. Vercel will automatically detect `vercel.json`:
   - Output Directory: `backend/app/static`
   - API Proxy: Automatically forwards `/api/*` to `https://vayucoupler-9sfi.onrender.com/api/*`.
4. Click **Deploy**.
5. Your clean, badge-free frontend will be live on `https://vayucoupler.vercel.app` in ~20 seconds.
