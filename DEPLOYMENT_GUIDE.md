# 🚀 VayuCoupler Deployment Guide: Render & Netlify

This guide provides step-by-step instructions to deploy **VayuCoupler** to **Render** (for the Python FastAPI + Gemini AI backend) and **Netlify** (for high-speed global CDN frontend delivery).

---

## 🏗️ Architecture Overview

VayuCoupler consists of:
1. **Python FastAPI Backend**: Serves atmospheric physics models, WRF-Chem simulation playback, predictive GRAP triggers, and Google Gemini 2.5 Flash conversational intelligence.
2. **Interactive Frontend**: Modern dashboard with Leaflet spatial wind streamlines, 7-day synoptic weather curves, source attribution donut charts, and time-travel crisis scrubber.

| Platform | Role | Configuration File |
| :--- | :--- | :--- |
| **Render** | Full-Stack Web Service (Python FastAPI + APIs + Static UI) | `render.yaml` & `requirements.txt` |
| **Netlify** | Global Edge CDN Frontend (with seamless API proxying to Render) | `netlify.toml` |

---

## 📦 Step 1: Push Your Code to GitHub

Make sure all latest changes are committed and pushed to your GitHub repository:

```bash
git add .
git commit -m "feat: complete production setup for Render and Netlify deployment"
git push origin main
```

---

## ⚡ Step 2: Deploy on Render (Python Web Service)

Render runs the FastAPI server on its free cloud tier.

1. Go to [dashboard.render.com](https://dashboard.render.com) and log in.
2. Click **New +** (top right) and select **Web Service**.
3. Connect your GitHub account and select your **VayuCoupler** repository.
4. Fill in the deployment details:
   - **Name**: `vayucoupler` *(or any preferred name)*
   - **Region**: Singapore / Frankfurt / Oregon *(closest to your users)*
   - **Branch**: `main`
   - **Root Directory**: *(Leave blank)*
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free`
5. **Add Environment Variables** (under *Advanced* or *Environment*):
   - Key: `PYTHON_VERSION` → Value: `3.10.12`
   - Key: `GEMINI_API_KEY` → Value: `Your_Google_Gemini_API_Key` *(for live VayuAI AI chat)*
6. Click **Create Web Service**.
7. Render will build dependencies and start the app in ~2 minutes.
8. Once finished, Render will provide your public URL:
   👉 `https://vayucoupler.onrender.com`

> **Note**: Your full app (both dashboard and REST APIs at `/api/...` and `/docs`) is now 100% operational on this Render URL!

---

## 🌐 Step 3: Deploy on Netlify (Global CDN Frontend)

Netlify serves the frontend from edge locations worldwide and proxies API calls to your Render backend.

1. Open `netlify.toml` in your repository.
2. Update the redirect target with your actual Render URL from Step 2:
   ```toml
   [[redirects]]
     from = "/api/*"
     to = "https://vayucoupler-9sfi.onrender.com/api/:splat"
     status = 200
     force = true
   ```
3. Commit and push this change:
   ```bash
   git add netlify.toml
   git commit -m "chore: point Netlify API proxy to Render live backend"
   git push origin main
   ```
4. Go to [app.netlify.com](https://app.netlify.com) and log in.
5. Click **Add new site** → **Import an existing project**.
6. Select **GitHub** and pick the **VayuCoupler** repository.
7. Netlify automatically detects `netlify.toml`:
   - **Base directory**: *(Leave blank)*
   - **Build command**: *(Leave blank)*
   - **Publish directory**: `backend/app/static`
8. Click **Deploy VayuCoupler**.
9. In ~15 seconds, Netlify will assign a live URL:
   👉 `https://vayucoupler.netlify.app` *(you can customize this under Site configuration → Change site name)*.

---

## 🧪 Step 4: Verification Checklist

Once deployed, verify both environments:

- [ ] **Render Direct App**: Open `https://YOUR-RENDER-NAME.onrender.com/` — Command Center, Live Weather, and Source Attribution panels load smoothly.
- [ ] **Render API Docs**: Open `https://YOUR-RENDER-NAME.onrender.com/docs` — Interactive Swagger UI opens with all endpoints (`/api/snapshot`, `/api/forecast`, `/api/vayuai/chat`).
- [ ] **Netlify Frontend**: Open `https://YOUR-SITE-NAME.netlify.app/` — Loads instantaneously via Netlify CDN.
- [ ] **VayuAI Assistant**: Type *"bdiya weather bata"* or *"school closed tomorrow"* — Receives live meteorological breakdowns and actionable insights.
- [ ] **Weather & Attribution Tabs**: Verify that clicking **Weather** and **Attribution** displays full interactive charts and cards.

---

## 💡 Pro Tips

- **Render Free Tier Cold Starts**: Render's free tier spins down after 15 minutes of inactivity. The first request after sleep may take ~30 seconds to spin up.
- **Offline Self-Sufficiency**: If Render is ever waking up or offline, VayuCoupler's frontend automatically falls back to its embedded atmospheric physics engine so users never see a broken screen.
- **Custom Domain**: You can add your custom domain (e.g. `vayucoupler.in` or `vayucoupler.org`) in Netlify under *Domain management* with free automatic SSL.
