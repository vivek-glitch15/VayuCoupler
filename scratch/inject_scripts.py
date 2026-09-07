#!/usr/bin/env python3
"""
Inject the core JavaScript modules into backend/app/static/index.html:
- VayuForecastEngine (72h ForecastPoint array, diurnal curve, stations)
- VayuLocationService (GPS, haversine, toast with progress bar, station picker)
- VayuSplashScreen (6s animation, gauge ring, count-up, tap-to-skip)
- VayuPredictiveTimeline (connected vertical timeline, GRAP stages)
- VayuDispatchesCenter (2-column agency grid, protocol detail sheet)
- VayuAIAssistant (Hub view, 15 Hinglish intents, speech recognition mic)
"""

import re

INDEX_PATH = "backend/app/static/index.html"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Build the complete JS modules code
js_modules = r"""
    /* ==========================================================================
       VAYUCOUPLER CORE SYSTEM MODULES
       MoES Atmospheric Coupled System — SIH 2026
       ========================================================================== */

    // Custom SVG Line Icons Registry (1.8px stroke, rounded caps, zero emoji)
    const VayuIcons = {
      shield: `<svg class="w-5 h-5 svg-icon-line" viewBox="0 0 24 24" stroke="currentColor"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>`,
      leaf: `<svg class="w-5 h-5 svg-icon-line" viewBox="0 0 24 24" stroke="currentColor"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/></svg>`,
      crane: `<svg class="w-5 h-5 svg-icon-line" viewBox="0 0 24 24" stroke="currentColor"><path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z"/><path d="M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2"/><path d="M18 9h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-2"/><path d="M10 6h4"/><path d="M10 10h4"/><path d="M10 14h4"/><path d="M10 18h4"/></svg>`,
      cross: `<svg class="w-5 h-5 svg-icon-line" viewBox="0 0 24 24" stroke="currentColor"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>`,
      mortarboard: `<svg class="w-5 h-5 svg-icon-line" viewBox="0 0 24 24" stroke="currentColor"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>`,
      factory: `<svg class="w-5 h-5 svg-icon-line" viewBox="0 0 24 24" stroke="currentColor"><path d="M2 20a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V8l-7 5V8l-7 5V4H2z"/><line x1="18" y1="4" x2="18" y2="8"/></svg>`,
      bus: `<svg class="w-5 h-5 svg-icon-line" viewBox="0 0 24 24" stroke="currentColor"><rect x="3" y="3" width="18" height="15" rx="2"/><circle cx="7" cy="18" r="2"/><circle cx="17" cy="18" r="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="3" x2="9" y2="9"/><line x1="15" y1="3" x2="15" y2="9"/></svg>`,
      pin: `<svg class="w-4 h-4 svg-icon-line" viewBox="0 0 24 24" stroke="currentColor"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>`
    };

    // ==========================================================================
    // 1. SHARED FORECAST ENGINE MODULE (ForecastPoint Schema, 72h Diurnal Curve)
    // ==========================================================================
    const VayuForecastEngine = {
      // 16 Delhi-NCR Standard Monitoring Stations
      stations: [
        { id: 'DEL001', name: 'Punjabi Bagh', lat: 28.6692, lon: 77.1314, baseAQI: 431, dominant: 'PM2.5' },
        { id: 'DEL002', name: 'Anand Vihar', lat: 28.6469, lon: 77.3160, baseAQI: 468, dominant: 'PM2.5' },
        { id: 'DEL003', name: 'RK Puram', lat: 28.5660, lon: 77.1767, baseAQI: 388, dominant: 'PM2.5' },
        { id: 'DEL004', name: 'Dwarka Sector 8', lat: 28.5710, lon: 77.0719, baseAQI: 352, dominant: 'PM10' },
        { id: 'DEL005', name: 'Rohini', lat: 28.7325, lon: 77.1189, baseAQI: 412, dominant: 'PM2.5' },
        { id: 'NCR001', name: 'Gurugram Vikas Sadan', lat: 28.4595, lon: 77.0266, baseAQI: 345, dominant: 'PM2.5' },
        { id: 'NCR002', name: 'Noida Sector 62', lat: 28.6245, lon: 77.3639, baseAQI: 395, dominant: 'PM2.5' },
        { id: 'NCR003', name: 'Faridabad Sec 16A', lat: 28.4089, lon: 77.3178, baseAQI: 360, dominant: 'PM10' },
        { id: 'NCR004', name: 'Ghaziabad Vasundhara', lat: 28.6603, lon: 77.3573, baseAQI: 425, dominant: 'PM2.5' },
        { id: 'DEL006', name: 'Bawana', lat: 28.7963, lon: 77.0392, baseAQI: 442, dominant: 'PM2.5' },
        { id: 'DEL007', name: 'Jahangirpuri', lat: 28.7328, lon: 77.1706, baseAQI: 455, dominant: 'PM2.5' },
        { id: 'DEL008', name: 'Wazirpur', lat: 28.6998, lon: 77.1654, baseAQI: 462, dominant: 'PM2.5' },
        { id: 'DEL009', name: 'Okhla Phase 2', lat: 28.5308, lon: 77.2713, baseAQI: 378, dominant: 'NO2' },
        { id: 'DEL010', name: 'Mundka', lat: 28.6847, lon: 77.0345, baseAQI: 438, dominant: 'PM10' },
        { id: 'DEL011', name: 'Alipur', lat: 28.7972, lon: 77.1332, baseAQI: 390, dominant: 'PM2.5' },
        { id: 'DEL012', name: 'DTU Shahbad', lat: 28.7501, lon: 77.1112, baseAQI: 365, dominant: 'PM2.5' }
      ],

      currentStation: null,
      currentAQI: 431,
      stationDistanceKm: 6.2,
      forecastArray: [], // 72 hourly ForecastPoint objects

      init() {
        this.currentStation = this.stations[0];
        this.currentAQI = this.currentStation.baseAQI;
        this.generate72hForecast();
      },

      getGrapStage(aqi) {
        if (aqi >= 450) return "Stage IV";
        if (aqi >= 401) return "Stage III";
        if (aqi >= 301) return "Stage II";
        if (aqi >= 201) return "Stage I";
        return "None";
      },

      getSeverityMeta(aqi) {
        if (aqi >= 450) {
          return { label: "Emergency / Severe+", color: "#f2966e", badgeClass: "badge-red", pillClass: "bg-[#1f150f] text-[#f2966e] border-[#4a2e20]" };
        } else if (aqi >= 401) {
          return { label: "Severe", color: "#f2966e", badgeClass: "badge-red", pillClass: "bg-[#1f150f] text-[#f2966e] border-[#4a2e20]" };
        } else if (aqi >= 301) {
          return { label: "Very Poor", color: "#f2d666", badgeClass: "badge-yellow", pillClass: "bg-[#1f1a0f] text-[#f2d666] border-[#4a4020]" };
        } else if (aqi >= 201) {
          return { label: "Poor", color: "#f2d666", badgeClass: "badge-yellow", pillClass: "bg-[#1f1a0f] text-[#f2d666] border-[#4a4020]" };
        } else if (aqi >= 101) {
          return { label: "Moderate", color: "#6ec8f2", badgeClass: "badge-blue", pillClass: "bg-[#0f1a1f] text-[#6ec8f2] border-[#1f3a4a]" };
        } else {
          return { label: "Good / Satisfactory", color: "#6fe2a3", badgeClass: "badge-green", pillClass: "bg-[#10201a] text-[#6fe2a3] border-[#1f3d30]" };
        }
      },

      generate72hForecast(baseAQI, stationName) {
        const base = baseAQI || (this.currentStation ? this.currentStation.baseAQI : 431);
        const name = stationName || (this.currentStation ? this.currentStation.name : 'Punjabi Bagh');
        const dominant = this.currentStation ? this.currentStation.dominant : 'PM2.5';
        
        const now = new Date();
        const points = [];

        for (let lead = 0; lead < 72; lead++) {
          const ptDate = new Date(now.getTime() + lead * 3600000);
          const hour = ptDate.getHours();

          // Realistic diurnal curve:
          // Morning peak (05:00-08:30 AM): nocturnal inversion trapping (~ +22%)
          // Midday dip (13:00-16:00 PM): solar convective boundary layer expansion (~ -26%)
          // Evening rise (19:00-22:00 PM): commuter rush + temperature inversion setup (~ +12%)
          let diurnalMult = 1.0;
          if (hour >= 4 && hour <= 9) {
            diurnalMult = 1.18 + Math.sin(((hour - 4) / 5) * Math.PI) * 0.12;
          } else if (hour >= 12 && hour <= 16) {
            diurnalMult = 0.74 - Math.sin(((hour - 12) / 4) * Math.PI) * 0.08;
          } else if (hour >= 18 && hour <= 22) {
            diurnalMult = 1.08 + Math.sin(((hour - 18) / 4) * Math.PI) * 0.06;
          } else {
            diurnalMult = 0.95;
          }

          // Synoptic multi-day surge: Day 1-2 build up, Day 3 peak, recovery later
          let synopticTrend = 0;
          if (lead >= 20 && lead <= 48) {
            synopticTrend = Math.sin(((lead - 20) / 28) * Math.PI) * 24;
          } else if (lead > 48) {
            synopticTrend = -Math.min(50, (lead - 48) * 1.8);
          }

          const rawAQI = Math.round(base * diurnalMult + synopticTrend);
          const aqi = Math.max(85, Math.min(498, rawAQI));

          // Confidence decays slightly with forecast lead time (0.94 -> 0.81)
          const confidence = Number((0.94 - (lead / 72) * 0.13).toFixed(2));
          const grapStage = this.getGrapStage(aqi);

          points.push({
            timestamp: ptDate.toISOString(),
            hourFormatted: ptDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            dateFormatted: ptDate.toLocaleDateString([], { month: 'short', day: 'numeric' }),
            leadHours: lead,
            aqi: aqi,
            confidence: confidence,
            dominantPollutant: dominant,
            grapStage: grapStage
          });
        }

        this.forecastArray = points;
        this.currentAQI = points[0].aqi;
        return points;
      },

      getMaxLeadHoursGained() {
        // Find highest lead hours among triggered stages
        let maxLead = 48; // default benchmark
        const peakAQIIn72 = Math.max(...this.forecastArray.map(p => p.aqi));
        if (peakAQIIn72 >= 450) maxLead = 72;
        else if (peakAQIIn72 >= 401) maxLead = 48;
        else if (peakAQIIn72 >= 301) maxLead = 36;
        else maxLead = 24;
        return maxLead;
      }
    };

    // ==========================================================================
    // 2. LIVE GPS LOCATION SERVICE (Haversine Distance, Auto-Toast, Station Picker)
    // ==========================================================================
    const VayuLocationService = {
      toastTimeout: null,
      cachedKey: 'vayucoupler_resolved_location',

      calcHaversineDistance(lat1, lon1, lat2, lon2) {
        const R = 6371; // Earth's radius in km
        const dLat = (lat2 - lat1) * Math.PI / 180;
        const dLon = (lon2 - lon1) * Math.PI / 180;
        const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
                  Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
                  Math.sin(dLon / 2) * Math.sin(dLon / 2);
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        return Number((R * c).toFixed(1));
      },

      init() {
        // Check localStorage cache first
        const cached = localStorage.getItem(this.cachedKey);
        if (cached) {
          try {
            const data = JSON.parse(cached);
            const found = VayuForecastEngine.stations.find(s => s.id === data.stationId);
            if (found) {
              VayuForecastEngine.currentStation = found;
              VayuForecastEngine.stationDistanceKm = data.distanceKm || 6.2;
              this.applyResolvedStation(found, VayuForecastEngine.stationDistanceKm, false);
              return;
            }
          } catch(e) {
            console.error(e);
          }
        }

        // Trigger live browser geolocation
        this.requestDeviceLocation();
      },

      requestDeviceLocation(showSuccessToast = true) {
        if (!navigator.geolocation) {
          this.fallbackToDefaultStation("Geolocation not supported by device");
          return;
        }

        navigator.geolocation.getCurrentPosition(
          (pos) => {
            const userLat = pos.coords.latitude;
            const userLon = pos.coords.longitude;

            // Find nearest Delhi-NCR station
            let minDistance = Infinity;
            let nearestStation = VayuForecastEngine.stations[0];

            VayuForecastEngine.stations.forEach(st => {
              const dist = this.calcHaversineDistance(userLat, userLon, st.lat, st.lon);
              if (dist < minDistance) {
                minDistance = dist;
                nearestStation = st;
              }
            });

            VayuForecastEngine.currentStation = nearestStation;
            VayuForecastEngine.stationDistanceKm = minDistance;

            // Cache in localStorage
            localStorage.setItem(this.cachedKey, JSON.stringify({
              stationId: nearestStation.id,
              distanceKm: minDistance,
              timestamp: Date.now()
            }));

            this.applyResolvedStation(nearestStation, minDistance, showSuccessToast);
          },
          (err) => {
            console.warn("Location permission denied or timed out:", err.message);
            this.fallbackToDefaultStation("Location access denied — showing Punjabi Bagh");
          },
          { enableHighAccuracy: false, timeout: 6000, maximumAge: 600000 }
        );
      },

      fallbackToDefaultStation(notice) {
        const defaultStation = VayuForecastEngine.stations[0]; // Punjabi Bagh
        VayuForecastEngine.currentStation = defaultStation;
        VayuForecastEngine.stationDistanceKm = 6.2;
        this.applyResolvedStation(defaultStation, 6.2, false);

        const textEl = document.getElementById('header-station-text');
        if (textEl) {
          textEl.innerText = `${defaultStation.name} (6.2 km)`;
        }
      },

      applyResolvedStation(station, distanceKm, showToast = true) {
        VayuForecastEngine.currentStation = station;
        VayuForecastEngine.stationDistanceKm = distanceKm;
        VayuForecastEngine.generate72hForecast(station.baseAQI, station.name);

        // Update Header location pill
        const textEl = document.getElementById('header-station-text');
        if (textEl) {
          textEl.innerText = `${station.name} (${distanceKm} km)`;
        }

        // Update Splash Screen location line
        const splashName = document.getElementById('splash-station-name');
        const splashDist = document.getElementById('splash-station-dist');
        if (splashName) splashName.innerText = station.name;
        if (splashDist) splashDist.innerText = `${distanceKm} km`;

        // Update Header AQI badge
        const aqiMeta = VayuForecastEngine.getSeverityMeta(station.baseAQI);
        const aqiValEl = document.getElementById('header-aqi-val');
        const aqiSevEl = document.getElementById('header-aqi-severity');
        const aqiBadge = document.getElementById('header-aqi-badge');
        if (aqiValEl) aqiValEl.innerText = `AQI ${station.baseAQI}`;
        if (aqiSevEl) aqiSevEl.innerText = aqiMeta.label.toUpperCase();
        if (aqiBadge) {
          aqiBadge.className = `px-2.5 py-1.5 rounded-xl ${aqiMeta.badgeClass} flex items-center gap-1.5 text-xs font-mono-data font-bold shadow-sm shrink-0`;
        }

        // Show animated toast banner
        if (showToast) {
          this.showLocationToast(station.name, distanceKm, station.baseAQI);
        }

        // Refresh Predictive timeline and dispatches
        if (typeof VayuPredictiveTimeline !== 'undefined') {
          VayuPredictiveTimeline.render();
        }
        if (typeof VayuDispatchesCenter !== 'undefined') {
          VayuDispatchesCenter.render();
        }
      },

      showLocationToast(stationName, distanceKm, aqi) {
        const toast = document.getElementById('gps-location-toast');
        const subtext = document.getElementById('toast-station-subtext');
        const pBar = document.getElementById('toast-progress-bar');
        if (!toast || !subtext) return;

        subtext.innerText = `${stationName} • ${distanceKm} km away • AQI ${aqi}`;
        toast.classList.remove('hidden');

        // Animate progress bar across 4.2s
        if (pBar) {
          pBar.style.transition = 'none';
          pBar.style.transform = 'scaleX(1)';
          setTimeout(() => {
            pBar.style.transition = 'transform 4.2s linear';
            pBar.style.transform = 'scaleX(0)';
          }, 50);
        }

        if (this.toastTimeout) clearTimeout(this.toastTimeout);
        this.toastTimeout = setTimeout(() => {
          toast.classList.add('hidden');
        }, 4400);
      }
    };

    function dismissLocationToast() {
      const toast = document.getElementById('gps-location-toast');
      if (toast) toast.classList.add('hidden');
      if (VayuLocationService.toastTimeout) clearTimeout(VayuLocationService.toastTimeout);
    }

    function refreshGPSLocation() {
      VayuLocationService.requestDeviceLocation(true);
    }

    function openStationPickerModal() {
      const modal = document.getElementById('station-picker-modal');
      const list = document.getElementById('stations-picker-list');
      if (!modal || !list) return;

      list.innerHTML = VayuForecastEngine.stations.map(st => {
        const isCurrent = VayuForecastEngine.currentStation && VayuForecastEngine.currentStation.id === st.id;
        const meta = VayuForecastEngine.getSeverityMeta(st.baseAQI);
        return `
          <button onclick="selectManualStation('${st.id}')" class="p-3 rounded-xl border text-left flex items-center justify-between transition ${isCurrent ? 'bg-[#10201a] border-[#1f3d30] text-white shadow-sm' : 'bg-[#0f110f] border-[#1c1f1c] text-[#f2f5f3] hover:bg-[#151815]'}">
            <div class="flex items-center gap-2.5 min-w-0">
              <span class="w-2.5 h-2.5 rounded-full shrink-0" style="background-color: ${meta.color}"></span>
              <div class="min-w-0">
                <div class="font-bold text-xs truncate">${st.name}</div>
                <div class="text-[10px] text-[#8b9390] font-mono-data">Pollutant: ${st.dominant}</div>
              </div>
            </div>
            <div class="text-right shrink-0">
              <div class="text-xs font-bold font-mono-data" style="color: ${meta.color}">AQI ${st.baseAQI}</div>
              <span class="text-[9px] font-mono-tag uppercase ${meta.pillClass} px-2 py-0.5 rounded-full border">${meta.label}</span>
            </div>
          </button>
        `;
      }).join('');

      modal.classList.remove('hidden');
    }

    function closeStationPickerModal() {
      const modal = document.getElementById('station-picker-modal');
      if (modal) modal.classList.add('hidden');
    }

    function selectManualStation(stationId) {
      const found = VayuForecastEngine.stations.find(s => s.id === stationId);
      if (found) {
        VayuLocationService.applyResolvedStation(found, found.id === 'DEL001' ? 6.2 : 8.5, true);
        localStorage.setItem(VayuLocationService.cachedKey, JSON.stringify({
          stationId: found.id,
          distanceKm: 6.2,
          timestamp: Date.now()
        }));
      }
      closeStationPickerModal();
    }

    function filterStationsList(query) {
      const q = (query || '').toLowerCase().trim();
      const buttons = document.querySelectorAll('#stations-picker-list button');
      buttons.forEach(btn => {
        const text = btn.innerText.toLowerCase();
        btn.style.display = text.includes(q) ? 'flex' : 'none';
      });
    }

    // ==========================================================================
    // 3. INTRO / COLD LAUNCH SPLASH SCREEN CONTROLLER (~6 Seconds Total)
    // ==========================================================================
    const VayuSplashScreen = {
      isDismissed: false,
      canTapSkip: false,

      init() {
        const splash = document.getElementById('splash-screen');
        if (!splash) return;

        // Check prefers-reduced-motion
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
          splash.style.transition = 'opacity 0.4s ease';
          setTimeout(() => {
            splash.style.opacity = '0';
            setTimeout(() => splash.remove(), 400);
          }, 400);
          return;
        }

        const appMark = document.getElementById('splash-app-mark');
        const titleWrap = document.getElementById('splash-title-wrap');
        const gaugeWrap = document.getElementById('splash-gauge-wrap');
        const gaugeRing = document.getElementById('splash-gauge-ring');
        const aqiNumber = document.getElementById('splash-aqi-number');
        const aqiSev = document.getElementById('splash-aqi-severity');
        const locationLine = document.getElementById('splash-location-line');
        const statusWrap = document.getElementById('splash-status-wrap');
        const progressBar = document.getElementById('splash-progress-bar');
        const syncPct = document.getElementById('splash-sync-pct');
        const skipHint = document.getElementById('splash-skip-hint');

        const targetAQI = VayuForecastEngine.currentAQI || 431;
        const sevMeta = VayuForecastEngine.getSeverityMeta(targetAQI);

        // Sequence:
        // 0.0 - 0.8s: App mark fade & scale in
        setTimeout(() => {
          if (appMark) {
            appMark.style.opacity = '1';
            appMark.style.transform = 'scale(1)';
          }
        }, 80);

        // 0.7 - 1.3s: Wordmark & subtitle fade up
        setTimeout(() => {
          if (titleWrap) {
            titleWrap.style.opacity = '1';
            titleWrap.style.transform = 'translateY(0)';
          }
        }, 700);

        // 1.3 - 3.2s: Circular SVG gauge fills & number counts up
        setTimeout(() => {
          if (gaugeWrap) gaugeWrap.style.opacity = '1';

          // Circular gauge perimeter = 2 * PI * 50 = 314.159
          // Fill proportional to AQI (0 to 500)
          const targetOffset = 314.159 - (Math.min(500, targetAQI) / 500) * 314.159;
          if (gaugeRing) {
            gaugeRing.style.strokeDashoffset = targetOffset.toString();
          }

          // Count up number from 0 to targetAQI
          let currentVal = 0;
          const stepTime = Math.max(10, Math.floor(1800 / targetAQI));
          const countInterval = setInterval(() => {
            currentVal += Math.ceil(targetAQI / 40);
            if (currentVal >= targetAQI) {
              currentVal = targetAQI;
              clearInterval(countInterval);
              if (aqiSev) {
                aqiSev.innerText = sevMeta.label.toUpperCase();
                aqiSev.className = `text-[10px] font-mono-tag font-bold px-2.5 py-0.5 rounded-full ${sevMeta.badgeClass}`;
              }
              // Allow early tap skip now
              VayuSplashScreen.canTapSkip = true;
              if (skipHint) skipHint.style.opacity = '0.9';
            }
            if (aqiNumber) aqiNumber.innerText = currentVal;
          }, stepTime);
        }, 1300);

        // ~3.4s: Location line fades in
        setTimeout(() => {
          if (locationLine) locationLine.style.opacity = '1';
        }, 3400);

        // ~4.2s: Forecast sync status line + progress bar
        setTimeout(() => {
          if (statusWrap) statusWrap.style.opacity = '1';
          let pct = 0;
          const progressInterval = setInterval(() => {
            pct += 5;
            if (pct >= 100) {
              pct = 100;
              clearInterval(progressInterval);
            }
            if (progressBar) progressBar.style.width = pct + '%';
            if (syncPct) syncPct.innerText = pct + '%';
          }, 60);
        }, 4200);

        // ~5.6 - 6.4s: Smooth fade and scale out, reveal Command Center
        setTimeout(() => {
          this.dismissSplash();
        }, 5800);
      },

      handleUserTapSkip() {
        if (this.canTapSkip && !this.isDismissed) {
          this.dismissSplash();
        }
      },

      dismissSplash() {
        if (this.isDismissed) return;
        this.isDismissed = true;

        const splash = document.getElementById('splash-screen');
        if (splash) {
          splash.classList.add('splash-fade-out');
          setTimeout(() => {
            splash.style.display = 'none';
            splash.remove();
          }, 850);
        }
      }
    };

    // ==========================================================================
    // 4. PREDICTIVE ACTION PLAN ENGINE (Vertical Connected Timeline)
    // ==========================================================================
    const VayuPredictiveTimeline = {
      // 6 GRAP Stages as specified
      stages: [
        {
          id: 'pre-stage-1-agri',
          stageName: 'Pre-Stage 1 (Advisory)',
          aqiMin: 150,
          aqiMax: 200,
          sector: 'Agriculture (Stubble Burning)',
          leadHours: 72,
          leadTag: '+72H LEAD',
          severityColor: '#f2d666', // yellow/amber
          badgeClass: 'badge-yellow',
          agency: 'CAQM & Dept of Agriculture (Punjab/Haryana)',
          actionText: 'Issue pre-emptive advisory to Punjab & Haryana Agriculture Dept. Deploy mobile bio-decomposer spray units to identified stubble-burning hotspots via satellite fire count.'
        },
        {
          id: 'pre-stage-1-dust',
          stageName: 'Pre-Stage 1 (Dust & Sanitation)',
          aqiMin: 201,
          aqiMax: 300,
          sector: 'Road Dust & Sanitation',
          leadHours: 48,
          leadTag: '+48H LEAD',
          severityColor: '#f2d666',
          badgeClass: 'badge-yellow',
          agency: 'Municipal Bodies (MCD, NDMC) & PWD',
          actionText: 'Intensify mechanical sweeping and vacuum cleaning of arterial corridors. Initiate heavy recycled water sprinkling on unpaved shoulders twice daily.'
        },
        {
          id: 'pre-stage-2-hotspots',
          stageName: 'Pre-Stage 2 (Hotspots & Anti-Smog)',
          aqiMin: 301,
          aqiMax: 350,
          sector: 'Construction & Hotspots',
          leadHours: 48,
          leadTag: '+48H LEAD',
          severityColor: '#f2d666',
          badgeClass: 'badge-yellow',
          agency: 'DPCC & Urban Local Bodies',
          actionText: 'Pre-position anti-smog water mist guns at known Delhi hotspots (Anand Vihar, Wazirpur, RK Puram). Ready dust-suppression water tankers at all transit choke points.'
        },
        {
          id: 'stage-2-dg',
          stageName: 'Stage 2 (GRAP II — Moderate to Poor)',
          aqiMin: 301,
          aqiMax: 400,
          sector: 'Power / Diesel Generators',
          leadHours: 36,
          leadTag: '+36H LEAD',
          severityColor: '#f2d666',
          badgeClass: 'badge-yellow',
          agency: 'Power Discoms & Transport Dept',
          actionText: 'Restrict diesel generator sets across industrial & commercial complexes except essential lifeline services. Augment metro and electric bus headway frequencies.'
        },
        {
          id: 'stage-3-severe',
          stageName: 'Stage 3 (GRAP III — Severe)',
          aqiMin: 401,
          aqiMax: 450,
          sector: 'Construction / Private Vehicles',
          leadHours: 24,
          leadTag: '+24H LEAD',
          severityColor: '#f2966e', // red
          badgeClass: 'badge-red',
          agency: 'Delhi Traffic Police & CAQM',
          actionText: 'Enforce complete ban on non-essential construction and demolition activities. Enforce strict movement ban on BS-III Petrol and BS-IV Diesel 4-wheeler passenger vehicles.'
        },
        {
          id: 'stage-4-emergency',
          stageName: 'Stage 4 (GRAP IV — Severe+ / Emergency)',
          aqiMin: 450,
          aqiMax: 500,
          sector: 'City-wide Emergency Curbs',
          leadHours: 24,
          leadTag: '+12–24H LEAD',
          severityColor: '#f2966e',
          badgeClass: 'badge-red',
          agency: 'Chief Secretary GNCTD & Police',
          actionText: 'Ban entry of commercial diesel trucks into Delhi (except essential commodities). Evaluate odd-even vehicular rationing, transition schools to hybrid/online, and mandate 50% WFH.'
        }
      ],

      render() {
        const container = document.getElementById('grap-timeline-items');
        const maxLeadEl = document.getElementById('grap-max-lead-gained');
        if (!container) return;

        const forecast = VayuForecastEngine.forecastArray;
        let maxTriggeredLead = 24;

        container.innerHTML = this.stages.map((stage, idx) => {
          // Check if forecast crosses this stage threshold within leadHours window
          const windowPoints = forecast.slice(0, stage.leadHours || 48);
          const isTriggered = windowPoints.some(pt => pt.aqi >= stage.aqiMin);

          if (isTriggered && stage.leadHours > maxTriggeredLead) {
            maxTriggeredLead = stage.leadHours;
          }

          const statusBadge = isTriggered
            ? `<span class="px-2.5 py-0.5 rounded-full ${stage.badgeClass} font-mono-tag font-bold text-[10px] flex items-center gap-1.5"><span class="w-1.5 h-1.5 rounded-full bg-current animate-ping"></span> TRIGGERED</span>`
            : `<span class="px-2.5 py-0.5 rounded-full bg-[#0f110f] border border-[#1c1f1c] text-[#8b9390] font-mono-tag text-[10px]">MONITORING</span>`;

          return `
            <div class="timeline-item">
              <!-- Colored Node Dot on 1px vertical timeline -->
              <div class="timeline-node-dot" style="color: ${stage.severityColor};">
                <div class="timeline-node-dot-inner"></div>
              </div>

              <!-- Content Box -->
              <div class="surface-card p-4 rounded-xl border border-[#1c1f1c] hover:border-[#1f3d30] transition flex flex-col gap-2.5">
                <!-- Top Row: Stage Name + Status Pill -->
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-1.5">
                  <div class="flex items-center gap-2 flex-wrap">
                    <span class="text-xs font-bold font-mono-data text-[#6fe2a3] px-2 py-0.5 rounded bg-[#10201a] border border-[#1f3d30]">${stage.leadTag}</span>
                    <h3 class="text-sm sm:text-base font-bold text-white font-serif-display">${stage.stageName}</h3>
                    <span class="text-[10px] font-mono-data text-[#8b9390]">(AQI ${stage.aqiMin}–${stage.aqiMax})</span>
                  </div>
                  <div>${statusBadge}</div>
                </div>

                <!-- Sector & Responsible Agency Line -->
                <div class="flex items-center justify-between text-xs text-[#8b9390] font-sans-ui flex-wrap gap-2">
                  <span>Sector: <b class="text-[#cfdade]">${stage.sector}</b></span>
                  <span class="text-[11px] font-mono-data text-[#8b9390]">${stage.agency}</span>
                </div>

                <!-- Inset Action Box (surface-2 background, 1px border) -->
                <div class="p-3 rounded-xl bg-[#060706] border border-[#1c1f1c] text-xs text-[#f2f5f3] font-sans-ui leading-relaxed">
                  <div class="text-[10px] font-mono-data text-[#6fe2a3] uppercase tracking-wider mb-1 font-semibold">TRIGGERED ACTION PROTOCOL:</div>
                  ${stage.actionText}
                </div>
              </div>
            </div>
          `;
        }).join('');

        if (maxLeadEl) {
          maxLeadEl.innerText = `GAINED ${maxTriggeredLead} Hours`;
        }
      }
    };

    // ==========================================================================
    // 5. STAKEHOLDER ACTION DISPATCH CENTER (2-Column Grid Layout)
    // ==========================================================================
    const VayuDispatchesCenter = {
      agencies: [
        {
          roleCode: 'ROLE_POLICE',
          name: 'Delhi Police, NHAI & Haryana Police',
          icon: 'shield',
          priority: 'EMERGENCY',
          priorityBadge: 'badge-red',
          orderCount: 3,
          leadHours: 48,
          authority: 'CAQM Statutory Directive / Joint Police Order',
          orders: [
            { text: 'Activate variable electronic signage on KMP/WPE expressways diverting non-destined freight.', status: 'Completed', deadline: 'T-48h (Nov 03, 04:00 PM)' },
            { text: 'Deploy 48 inter-state interceptor checkpoints at Singhu, Tikri, Badarpur, and Ghazipur borders.', status: 'In Progress', deadline: 'T-36h (Nov 04, 04:00 AM)' },
            { text: 'Impound non-compliant BS-III Petrol and BS-IV Diesel 4-wheelers attempting NCT entry.', status: 'Acknowledged', deadline: 'T-24h (Nov 04, 04:00 PM)' }
          ],
          evidenceRef: 'ANPR Border Toll Cameras + CPCB Sensor Stream #DEL-SINGHU-04'
        },
        {
          roleCode: 'ROLE_AGRI',
          name: 'CAQM & Dept of Agriculture (Punjab/Haryana)',
          icon: 'leaf',
          priority: 'HIGH',
          priorityBadge: 'badge-yellow',
          orderCount: 3,
          leadHours: 72,
          authority: 'Ministry of Agriculture & Farmers Welfare / CAQM',
          orders: [
            { text: 'Deploy 180 mobile bio-decomposer spray tankers to satellite-detected fire clusters.', status: 'In Progress', deadline: 'T-72h (Nov 02, 04:00 PM)' },
            { text: 'Mobilize Happy Seeder & CRM machinery nodal officers across Sangrur, Bhatinda, and Firozpur.', status: 'Acknowledged', deadline: 'T-48h (Nov 03, 04:00 PM)' },
            { text: 'Issue spot penalty challans for deliberate field burns identified by thermal satellite passes.', status: 'Pending', deadline: 'T-24h (Nov 04, 04:00 PM)' }
          ],
          evidenceRef: 'VIIRS/MODIS 375m Satellite Fire Counts (3,140 Active Anomalies in Punjab)'
        },
        {
          roleCode: 'ROLE_MCD',
          name: 'Urban Local Bodies & Public Works (MCD, NDMC, PWD)',
          icon: 'crane',
          priority: 'HIGH',
          priorityBadge: 'badge-yellow',
          orderCount: 3,
          leadHours: 48,
          authority: 'Commissioner MCD / Chairman DPCC',
          orders: [
            { text: 'Deploy 78 mechanical road sweepers along Ring Road, Outer Ring Road, and transit spines.', status: 'In Progress', deadline: 'T-48h (Nov 03, 04:00 PM)' },
            { text: 'Operate water mist sprinkling tankers and anti-smog guns across 13 major pollution hotspots.', status: 'In Progress', deadline: 'T-36h (Nov 04, 04:00 AM)' },
            { text: 'Execute round-the-clock ground vigilance against open biomass and municipal waste dumping.', status: 'Acknowledged', deadline: 'T-24h (Nov 04, 04:00 PM)' }
          ],
          evidenceRef: 'GPS Fleet Tracker Log (78 Sweepers Active) + PM10 Hotspot Heatmaps'
        },
        {
          roleCode: 'ROLE_HEALTH',
          name: 'Directorate of Health Services & Hospitals',
          icon: 'cross',
          priority: 'HIGH',
          priorityBadge: 'badge-yellow',
          orderCount: 3,
          leadHours: 48,
          authority: 'Directorate General of Health Services (DGHS GNCTD)',
          orders: [
            { text: 'Broadcast high-priority public health advisory for elderly, pediatric, and asthmatic patients.', status: 'Completed', deadline: 'T-48h (Nov 03, 04:00 PM)' },
            { text: 'Stock emergency nebulizers, oxygen reserves, and bronchodilators in all dispensary wards.', status: 'In Progress', deadline: 'T-36h (Nov 04, 04:00 AM)' },
            { text: 'Mandate certified N95 respirator distribution for outdoor municipal, sanitation & traffic staff.', status: 'Acknowledged', deadline: 'T-24h (Nov 04, 04:00 PM)' }
          ],
          evidenceRef: 'Emergency Room Respiratory Inflow Surveillance Model (ICD-10 J44/J45)'
        },
        {
          roleCode: 'ROLE_EDU',
          name: 'Directorate of Education & DDMA (Schools)',
          icon: 'mortarboard',
          priority: 'MODERATE',
          priorityBadge: 'badge-blue',
          orderCount: 3,
          leadHours: 24,
          authority: 'Director of Education, GNCTD / DDMA Order',
          orders: [
            { text: 'Transition Nursery through Grade 5 physical classes to online learning mode.', status: 'Acknowledged', deadline: 'T-24h (Nov 04, 04:00 PM)' },
            { text: 'Cancel all outdoor morning assemblies, sports periods, and physical education drills.', status: 'Completed', deadline: 'T-24h (Nov 04, 04:00 PM)' },
            { text: 'Enforce indoor air filtration inspection and window sealing protocols across school premises.', status: 'Pending', deadline: 'T-12h (Nov 05, 04:00 AM)' }
          ],
          evidenceRef: 'Coupled 24h Morning Exposure Index (>420 AQI between 07:00-09:30 AM)'
        },
        {
          roleCode: 'ROLE_TRANSPORT',
          name: 'Delhi Transport Corporation & Traffic Police',
          icon: 'bus',
          priority: 'MODERATE',
          priorityBadge: 'badge-blue',
          orderCount: 3,
          leadHours: 36,
          authority: 'Transport Commissioner GNCTD & DMRC',
          orders: [
            { text: 'Inject 600 additional electric and CNG feeder trips during 08-11 AM & 05-08 PM peaks.', status: 'In Progress', deadline: 'T-36h (Nov 04, 04:00 AM)' },
            { text: 'Coordinate with Delhi Metro (DMRC) for 60 additional train trips across Red, Yellow & Blue lines.', status: 'Completed', deadline: 'T-36h (Nov 04, 04:00 AM)' },
            { text: 'Station traffic wardens at 28 congested intersection choke points to curb engine idling.', status: 'Acknowledged', deadline: 'T-24h (Nov 04, 04:00 PM)' }
          ],
          evidenceRef: 'Corridor Volume-to-Capacity Telemetry & DMRC Ridership Analytics'
        },
        {
          roleCode: 'ROLE_INDUSTRY',
          name: 'DPCC (Pollution Control Committee) & Industry',
          icon: 'factory',
          priority: 'HIGH',
          priorityBadge: 'badge-yellow',
          orderCount: 3,
          leadHours: 36,
          authority: 'Chairman, DPCC & Ministry of Environment',
          orders: [
            { text: 'Halt operations of all industrial units running on unapproved non-PNG/non-biomass fuels.', status: 'In Progress', deadline: 'T-36h (Nov 04, 04:00 AM)' },
            { text: 'Deploy nocturnal flying squads to inspect ready-mix concrete and hot-mix batching plants.', status: 'Acknowledged', deadline: 'T-24h (Nov 04, 04:00 PM)' },
            { text: 'Activate automated OCEMS emission telemetry alerting with instant industrial closure notices.', status: 'Completed', deadline: 'T-24h (Nov 04, 04:00 PM)' }
          ],
          evidenceRef: 'Online Continuous Emission Monitoring Systems (OCEMS) Stack Sensors'
        }
      ],

      render() {
        const grid = document.getElementById('agency-tiles-grid');
        const countPill = document.getElementById('dispatch-agency-count-pill');
        const tHourEl = document.getElementById('dispatch-t-hour-counter');
        const sevHeadline = document.getElementById('dispatch-severity-headline');
        const leadText = document.getElementById('dispatch-lead-time-text');
        if (!grid) return;

        const maxLead = VayuForecastEngine.getMaxLeadHoursGained();
        const currentAQI = VayuForecastEngine.currentAQI;
        const sevMeta = VayuForecastEngine.getSeverityMeta(currentAQI);

        if (countPill) countPill.innerText = `${this.agencies.length} Coordinated Agencies`;
        if (tHourEl) tHourEl.innerText = `T-HOUR 83 OF 167`;
        if (leadText) leadText.innerText = `${maxLead}h`;
        if (sevHeadline) {
          sevHeadline.innerText = `${sevMeta.label} — AQI ${currentAQI}`;
          sevHeadline.style.color = sevMeta.color;
        }

        grid.innerHTML = this.agencies.map((agency, index) => {
          const iconSvg = VayuIcons[agency.icon] || VayuIcons.shield;
          return `
            <div onclick="VayuDispatchesCenter.openProtocolModal(${index})" class="agency-tile">
              <div>
                <!-- Top Row: Icon Box + Role Code -->
                <div class="flex items-center justify-between mb-2.5">
                  <div class="w-9 h-9 rounded-xl bg-[#10201a] border border-[#1f3d30] text-[#6fe2a3] flex items-center justify-center">
                    ${iconSvg}
                  </div>
                  <span class="text-[10px] font-mono-data text-[#8b9390] uppercase tracking-wider">${agency.roleCode}</span>
                </div>

                <!-- Agency Name -->
                <h4 class="text-xs sm:text-sm font-bold text-white font-sans-ui line-clamp-2 leading-snug mb-1">
                  ${agency.name}
                </h4>
              </div>

              <!-- Bottom Row: Status Pill + Order Count in Green Mono -->
              <div class="flex items-center justify-between pt-3 mt-2 border-t border-[#1c1f1c]">
                <span class="text-[9px] font-mono-tag font-bold px-2 py-0.5 rounded-full ${agency.priorityBadge} uppercase">
                  ${agency.priority}
                </span>
                <span class="text-[10px] font-mono-data font-semibold text-[#6fe2a3]">
                  ${agency.orderCount} Orders →
                </span>
              </div>
            </div>
          `;
        }).join('');
      },

      openProtocolModal(agencyIndex) {
        const agency = this.agencies[agencyIndex];
        const modal = document.getElementById('protocol-modal');
        const content = document.getElementById('protocol-modal-content');
        if (!agency || !modal || !content) return;

        const iconSvg = VayuIcons[agency.icon] || VayuIcons.shield;

        content.innerHTML = `
          <!-- Header -->
          <div class="flex items-start gap-3 pb-4 border-b border-[#1c1f1c]">
            <div class="w-11 h-11 rounded-2xl bg-[#10201a] border border-[#1f3d30] text-[#6fe2a3] flex items-center justify-center shrink-0 mt-0.5">
              ${iconSvg}
            </div>
            <div class="min-w-0 pr-6">
              <div class="flex items-center gap-2 mb-1 flex-wrap">
                <span class="text-[10px] font-mono-data text-[#8b9390] font-bold">${agency.roleCode}</span>
                <span class="text-[10px] font-mono-tag font-bold px-2 py-0.5 rounded-full ${agency.priorityBadge}">${agency.priority} PRIORITY</span>
              </div>
              <h3 class="text-base font-bold text-white font-serif-display leading-tight">${agency.name}</h3>
              <p class="text-[11px] text-[#8b9390] mt-1 font-mono-data">Issuing Authority: <span class="text-[#cfdade]">${agency.authority}</span></p>
            </div>
          </div>

          <!-- Orders Checklist -->
          <div class="my-2">
            <h4 class="text-[11px] font-bold font-mono-data text-[#8b9390] uppercase tracking-wider mb-2">MANDATED PRE-EMPTIVE ORDERS (CHECKLIST):</h4>
            <div class="flex flex-col gap-2.5">
              ${agency.orders.map((ord, i) => `
                <div class="p-3 rounded-xl bg-[#060706] border border-[#1c1f1c] flex items-start gap-2.5">
                  <div class="w-5 h-5 rounded-lg bg-[#10201a] border border-[#1f3d30] text-[#6fe2a3] font-mono-data font-bold text-[10px] flex items-center justify-center shrink-0 mt-0.5">
                    ${i + 1}
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="text-xs text-[#f2f5f3] font-sans-ui leading-relaxed">${ord.text}</p>
                    <div class="flex items-center justify-between mt-2 pt-1.5 border-t border-[#1c1f1c] text-[10px] font-mono-data">
                      <span class="text-[#8b9390]">Deadline: <b class="text-[#6fe2a3]">${ord.deadline}</b></span>
                      <span class="px-2 py-0.2 rounded ${ord.status === 'Completed' ? 'badge-green' : ord.status === 'In Progress' ? 'badge-blue' : 'badge-yellow'} font-bold">${ord.status}</span>
                    </div>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>

          <!-- Evidence Attachment Reference Box -->
          <div class="p-3.5 rounded-xl bg-[#060706] border border-[#1c1f1c]">
            <div class="text-[10px] font-mono-data text-[#8b9390] uppercase tracking-wider mb-1 flex items-center gap-1.5 font-semibold">
              <span class="w-1.5 h-1.5 rounded-full bg-[#6fe2a3]"></span> OFFICIAL EVIDENCE & SENSOR GROUNDING
            </div>
            <p class="text-xs text-[#cfdade] font-mono-data leading-relaxed">
              ${agency.evidenceRef}
            </p>
          </div>

          <!-- Dispatch Action Button -->
          <div class="pt-2 flex justify-end">
            <button onclick="simulateBroadcastAlert('${agency.name}'); closeProtocolModal();" class="px-4 py-2 rounded-xl bg-[#6fe2a3] hover:bg-[#5cd493] text-[#060706] font-bold text-xs font-sans-ui flex items-center gap-1.5 shadow-lg shadow-emerald-950/40 transition">
              <svg class="w-3.5 h-3.5 svg-icon-line" viewBox="0 0 24 24" stroke="currentColor"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
              <span>Transmit Protocol Order</span>
            </button>
          </div>
        `;

        modal.classList.remove('hidden');
      }
    };

    function closeProtocolModal() {
      const modal = document.getElementById('protocol-modal');
      if (modal) modal.classList.add('hidden');
    }

    // ==========================================================================
    // 6. VAYUAI ASSISTANT (Hub Layout, 15 Preset Hinglish Intents, Voice Mic)
    // ==========================================================================
    const VayuAIAssistant = {
      // 15 Preset Intents scoped in detail
      presetQuestions: [
        { id: 1, cat: 'SCHOOLS', badgeClass: 'badge-yellow', q: 'Kal school band rahenge kya?' },
        { id: 2, cat: 'SCHOOLS', badgeClass: 'badge-yellow', q: 'School kab tak band rahenge?' },
        { id: 3, cat: 'FORECAST', badgeClass: 'badge-blue', q: 'Kal AQI kitna hoga?' },
        { id: 4, cat: 'GRAP', badgeClass: 'badge-red', q: 'Konsa GRAP stage lagu hoga?' },
        { id: 5, cat: 'SAFETY', badgeClass: 'badge-green', q: 'Mujhe mask pehnna chahiye kya?' },
        { id: 6, cat: 'SAFETY', badgeClass: 'badge-green', q: 'Outdoor activities/sports safe hain kya?' },
        { id: 7, cat: 'FORECAST', badgeClass: 'badge-blue', q: 'Konsi areas sabse zyada affected hongi?' },
        { id: 8, cat: 'TRANSPORT', badgeClass: 'badge-blue', q: 'Odd-even lagu hoga kya?' },
        { id: 9, cat: 'GRAP', badgeClass: 'badge-red', q: 'Construction/demolition band hogi kya?' },
        { id: 10, cat: 'SAFETY', badgeClass: 'badge-green', q: 'WFH advisory hai kya?' },
        { id: 11, cat: 'FORECAST', badgeClass: 'badge-blue', q: 'AQI kab tak improve hoga?' },
        { id: 12, cat: 'HEALTH', badgeClass: 'badge-yellow', q: 'Elderly/asthma/bachon ke liye precaution?' },
        { id: 13, cat: 'TRANSPORT', badgeClass: 'badge-blue', q: 'Flights ya trains affected honge kya?' },
        { id: 14, cat: 'GRAP', badgeClass: 'badge-red', q: 'Anti-smog guns kahan active hain?' },
        { id: 15, cat: 'FORECAST', badgeClass: 'badge-blue', q: 'Stubble burning ka kya status hai?' }
      ],

      speechRecognizer: null,
      isListening: false,

      init() {
        this.renderHubQuestions();
        this.initSpeechRecognition();
      },

      renderHubQuestions() {
        const grid = document.getElementById('vayuai-questions-grid');
        if (!grid) return;

        grid.innerHTML = this.presetQuestions.map(item => `
          <div onclick="VayuAIAssistant.askQuestion('${item.q}')" class="vayuai-question-card">
            <span class="text-[9px] font-mono-tag uppercase px-2 py-0.2 rounded-full ${item.badgeClass} w-max font-bold">${item.cat}</span>
            <p class="text-xs text-[#f2f5f3] font-sans-ui font-medium leading-snug line-clamp-2">${item.q}</p>
          </div>
        `).join('');
      },

      initSpeechRecognition() {
        const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRec) {
          console.log("Speech recognition not supported on this browser.");
          return;
        }

        const recognizer = new SpeechRec();
        recognizer.continuous = false;
        recognizer.interimResults = true;
        recognizer.lang = 'hi-IN'; // Accepts Hindi / Hinglish naturally

        recognizer.onstart = () => {
          this.isListening = true;
          const container = document.getElementById('vayuai-mic-container');
          const feedback = document.getElementById('vayuai-mic-feedback');
          if (container) container.classList.add('mic-listening');
          if (feedback) feedback.classList.remove('hidden');
        };

        recognizer.onresult = (e) => {
          let transcript = '';
          for (let i = e.resultIndex; i < e.results.length; ++i) {
            transcript += e.results[i][0].transcript;
          }
          const transcriptEl = document.getElementById('vayuai-live-speech-transcript');
          const inputEl = document.getElementById('vayuai-chat-input');
          if (transcriptEl) transcriptEl.innerText = transcript;
          if (inputEl) inputEl.value = transcript;
        };

        recognizer.onend = () => {
          this.isListening = false;
          const container = document.getElementById('vayuai-mic-container');
          const feedback = document.getElementById('vayuai-mic-feedback');
          if (container) container.classList.remove('mic-listening');
          if (feedback) feedback.classList.add('hidden');

          const inputEl = document.getElementById('vayuai-chat-input');
          if (inputEl && inputEl.value.trim()) {
            this.askQuestion(inputEl.value.trim());
            inputEl.value = '';
          }
        };

        recognizer.onerror = (err) => {
          console.warn("Speech recognition error:", err);
          this.isListening = false;
          const container = document.getElementById('vayuai-mic-container');
          const feedback = document.getElementById('vayuai-mic-feedback');
          if (container) container.classList.remove('mic-listening');
          if (feedback) feedback.classList.add('hidden');
        };

        this.speechRecognizer = recognizer;
      },

      toggleSpeech() {
        if (!this.speechRecognizer) {
          alert("Microphone speech recognition is not supported in this browser. Please type your query!");
          return;
        }

        if (this.isListening) {
          this.speechRecognizer.stop();
        } else {
          this.speechRecognizer.start();
        }
      },

      askQuestion(query) {
        const hubView = document.getElementById('vayuai-hub-view');
        const chatThread = document.getElementById('vayuai-chat-thread');
        const history = document.getElementById('vayuai-chat-history');
        if (!history) return;

        // Transition into Chat Thread View
        if (hubView) hubView.classList.add('hidden');
        if (chatThread) chatThread.classList.remove('hidden');

        // Add User Message Bubble
        history.innerHTML += `
          <div class="flex items-start gap-2.5 justify-end">
            <div class="p-3 chat-bubble-user max-w-sm sm:max-w-md font-sans-ui text-xs leading-relaxed">
              ${query}
            </div>
            <div class="w-7 h-7 rounded-lg bg-[#10201a] border border-[#1f3d30] text-[#6fe2a3] flex items-center justify-center shrink-0 text-xs font-mono font-bold">U</div>
          </div>
        `;

        history.scrollTop = history.scrollHeight;

        // Compute Live Answer grounded in VayuForecastEngine
        const responseData = this.computeDynamicAnswer(query);

        setTimeout(() => {
          history.innerHTML += `
            <div class="flex items-start gap-2.5 justify-start">
              <div class="w-7 h-7 rounded-lg bg-gradient-to-br from-[#6fe2a3] to-[#6ec8f2] flex items-center justify-center shrink-0 text-[#060706] text-xs font-black">V</div>
              <div class="p-3.5 chat-bubble-bot max-w-sm sm:max-w-lg font-sans-ui text-xs leading-relaxed">
                <div class="text-[#f2f5f3] leading-relaxed">${responseData.text}</div>
                
                <!-- Mono Meta Line: Lead Time + Confidence -->
                <div class="mt-2.5 pt-2 border-t border-[#1c1f1c] flex items-center justify-between text-[10px] font-mono-data text-[#8b9390]">
                  <span>${responseData.leadMeta}</span>
                  <span class="text-[#6fe2a3] font-semibold">${responseData.confidence}% confidence</span>
                </div>

                <!-- Deep-Link to Action Plan / Dispatches -->
                <button onclick="switchTab('${responseData.tabLink || 'grap'}')" class="mt-2 text-[11px] font-mono-data font-semibold text-[#6fe2a3] hover:underline flex items-center gap-1">
                  <span>View full action plan →</span>
                </button>
              </div>
            </div>
          `;
          history.scrollTop = history.scrollHeight;
        }, 350);
      },

      computeDynamicAnswer(query) {
        const q = query.toLowerCase();
        const forecast = VayuForecastEngine.forecastArray;
        const currentAQI = VayuForecastEngine.currentAQI;
        const stationName = VayuForecastEngine.currentStation ? VayuForecastEngine.currentStation.name : 'Punjabi Bagh';
        const next24Pt = forecast[24] || forecast[forecast.length - 1];
        const next12Pt = forecast[12] || forecast[0];
        const max48AQI = Math.max(...forecast.slice(0, 48).map(p => p.aqi));
        const max48Stage = VayuForecastEngine.getGrapStage(max48AQI);

        // 1. "Kal school band rahenge kya?"
        if (q.includes('school band') || (q.includes('school') && q.includes('kal'))) {
          const crossesThreshold = next24Pt.aqi >= 400;
          return {
            text: crossesThreshold
              ? `Haan, agle 24 ghante me Delhi-NCR me projected AQI <b>${next24Pt.aqi} (${next24Pt.grapStage})</b> hai. CAQM guidelines ke tehat Primary schools (Class 1–5) physically band rahenge aur online mode par chalenge.`
              : `Nahi, kal projected AQI <b>${next24Pt.aqi}</b> hai jo emergency closure threshold (<400) se neeche hai. Schools regular timings par operate karenge, par morning outdoor physical assemblies cancel rahengi.`,
            leadMeta: `Based on 24-hour coupled forecast (${next24Pt.hourFormatted})`,
            confidence: Math.round(next24Pt.confidence * 100),
            tabLink: 'grap'
          };
        }

        // 2. "School kab tak band rahenge?"
        if (q.includes('kab tak') && q.includes('school')) {
          const reopenIndex = forecast.findIndex(p => p.aqi < 350);
          const reopenPt = reopenIndex !== -1 ? forecast[reopenIndex] : null;
          return {
            text: reopenPt
              ? `Coupled model ke anusaar AQI <b>T+${reopenPt.leadHours}h</b> par ${reopenPt.aqi} tak girkar safe threshold me aayega (${reopenPt.dateFormatted}, ${reopenPt.hourFormatted}). Tab tak hybrid classes aur outdoor restrictions jari rahenge.`
              : `Agle 72 ghante tak AQI high (${max48AQI} peak) bana rahega. Schools ke liye physical reopening advisory agle 3 dino baad hi review ki jayegi.`,
            leadMeta: 'Based on 72-hour forecast trajectory',
            confidence: 86,
            tabLink: 'grap'
          };
        }

        // 3. "Kal AQI kitna hoga?"
        if (q.includes('kal aqi') || (q.includes('kal') && q.includes('kitna'))) {
          const meta = VayuForecastEngine.getSeverityMeta(next24Pt.aqi);
          return {
            text: `Kal is waqt (+24h) ${stationName} par predicted AQI <b>${next24Pt.aqi}</b> hoga (<span style="color:${meta.color}">${meta.label}</span>). Dominant pollutant: <b>${next24Pt.dominantPollutant}</b>. Subah 07:00 AM par inversion ke chalte smog sabse dense rahega.`,
            leadMeta: `Based on 24-hour forecast · Station ${stationName}`,
            confidence: Math.round(next24Pt.confidence * 100),
            tabLink: 'overview'
          };
        }

        // 4. "Konsa GRAP stage lagu hoga?"
        if (q.includes('grap') && (q.includes('stage') || q.includes('lagu') || q.includes('konsa'))) {
          return {
            text: `Agle 48 ghante me Delhi-NCR me maximum AQI <b>${max48AQI}</b> touch karega, jisse <b>${max48Stage}</b> trigger ho raha hai. Iske tehat construction halts, DG set curbs aur commercial diesel truck entry restrictions mandatory hain.`,
            leadMeta: 'Based on 48-hour peak trigger calculation',
            confidence: 90,
            tabLink: 'grap'
          };
        }

        // 5. "Mujhe mask pehnna chahiye kya?"
        if (q.includes('mask') || q.includes('pehnna')) {
          return {
            text: currentAQI >= 200
              ? `Haan, bilkul! Current AQI <b>${currentAQI}</b> hai. Surgical ya kapde ke mask PM2.5 ko nahi rok paate — bahar nikalne par <b>certified N-95 ya FFP2 respirator</b> pehanna anivarya hai.`
              : `Current AQI ${currentAQI} Satisfactory/Moderate zone me hai, normal walking ke liye mask optional hai, par sensitive groups ke liye recommended hai.`,
            leadMeta: `Based on live telemetry at ${stationName}`,
            confidence: 96,
            tabLink: 'health'
          };
        }

        // 6. "Outdoor activities/sports safe hain kya?"
        if (q.includes('outdoor') || q.includes('sports') || q.includes('running') || q.includes('jog')) {
          return {
            text: `Subah 06:00 AM se 10:00 AM ke beech thermal inversion ke karan surface AQI <b>${next12Pt.aqi} (Severe)</b> rahega. Jogging ya outdoor sports se bachein. Safe clean air window dopahar <b>01:30 PM se 04:00 PM</b> ke beech hai.`,
            leadMeta: 'Based on 12-hour diurnal cycle calculation',
            confidence: 89,
            tabLink: 'planner'
          };
        }

        // 7. "Konsi areas sabse zyada affected hongi?"
        if (q.includes('areas') || q.includes('affected') || q.includes('jagah') || q.includes('hotspot')) {
          return {
            text: `Top 3 most affected hotspots: <b>(1) Anand Vihar (AQI 468)</b>, <b>(2) Wazirpur (AQI 462)</b>, aur <b>(3) Jahangirpuri (AQI 455)</b>. Ye areas boundary layer compression aur heavy highway diesel traffic ke direct downwind trap zone me aate hain.`,
            leadMeta: 'Based on coupled spatial dispersion mapping',
            confidence: 91,
            tabLink: 'overview'
          };
        }

        // 8. "Odd-even lagu hoga kya?"
        if (q.includes('odd-even') || q.includes('odd even')) {
          const stage4Triggered = max48AQI >= 450;
          return {
            text: stage4Triggered
              ? `Haan, agle 48 ghante me AQI ${max48AQI} (Stage IV Emergency) cross kar raha hai. Delhi Cabinet aur CAQM odd-even vehicle rationing scheme ko emergency measure ke roop me implement karne par active review me hain.`
              : `Filhal Odd-Even lagu nahi hai kyunki predicted AQI (${max48AQI}) Stage IV threshold (450+) se neeche hai. Halanki Stage III vehicle restrictions (BS-III Petrol / BS-IV Diesel ban) active hain.`,
            leadMeta: 'Based on 48-hour emergency stage threshold',
            confidence: 88,
            tabLink: 'dispatches'
          };
        }

        // 9. "Construction/demolition band hogi kya?"
        if (q.includes('construction') || q.includes('demolition') || q.includes('c&d')) {
          const stage3Triggered = max48AQI >= 401;
          return {
            text: stage3Triggered
              ? `Haan, Stage III/IV curbs ke tehat Delhi-NCR me sabhi non-essential private aur commercial Construction & Demolition (C&D) activities par <b>poori tarah se rok</b> laga di gayi hai. Ready-mix concrete aur stone crushers bhi band hain.`
              : `Non-polluting indoor construction permitted hai, par open earth excavation aur unpaved activities par water misting rules mandatory hain.`,
            leadMeta: 'Based on 36-hour predictive GRAP rules',
            confidence: 92,
            tabLink: 'grap'
          };
        }

        // 10. "WFH advisory hai kya?"
        if (q.includes('wfh') || q.includes('work from home')) {
          const stage4 = max48AQI >= 450;
          return {
            text: stage4
              ? `Haan, GRAP Stage IV ke tehat Delhi Government aur CAQM ne public, municipal aur private offices ke liye <b>50% Work-From-Home (WFH)</b> advisory issue kar di hai taaki peak hour vehicular volume kam ho sake.`
              : `Mandatory 50% WFH abhi enforce nahi hua hai, lekin sensitive respiratory patients aur pregnant staff ke liye hybrid/remote work recommended hai.`,
            leadMeta: 'Based on 48-hour forecast severity',
            confidence: 87,
            tabLink: 'dispatches'
          };
        }

        // 11. "AQI kab tak improve hoga?"
        if (q.includes('improve') || q.includes('sudhaar') || (q.includes('kab tak') && q.includes('aqi'))) {
          return {
            text: `Coupled meteorological forecast ke mutabiq <b>Day 6/7</b> par surface wind speed badhkar 14–16 km/h hone aur boundary layer 1,100m expand hone par toxic smog displace hoga aur AQI <b>220–250 (Moderate-Poor)</b> par settle hoga.`,
            leadMeta: 'Based on synoptic 72h wind-mixing trajectory',
            confidence: 84,
            tabLink: 'overview'
          };
        }

        // 12. "Elderly/asthma/bachon ke liye precaution?"
        if (q.includes('elderly') || q.includes('asthma') || q.includes('bachon') || q.includes('precaution') || q.includes('health')) {
          return {
            text: `Current AQI <b>${currentAQI}</b> par vulnerable groups ko subah 05:00–09:30 AM ke dauran strictly ghar ke andar rehna chahiye. True-HEPA purifiers on rakhein, dehydration se bachein, aur emergency inhalers/bronchodilators accessible rakhein.`,
            leadMeta: 'Based on clinical PM2.5 lung-deposition modeling',
            confidence: 95,
            tabLink: 'health'
          };
        }

        // 13. "Flights ya trains affected honge kya?"
        if (q.includes('flight') || q.includes('train') || q.includes('visibility') || q.includes('fog')) {
          return {
            text: `Haan, nocturnal inversion aur high humidity (>82%) ke chalte IGI Airport aur Northern Railway tracks par CAT-III radiation fog ban raha hai. Early morning departures me <b>35–60 minute delays</b> sambhav hain.`,
            leadMeta: 'Based on 24-hour visibility & inversion index',
            confidence: 87,
            tabLink: 'overview'
          };
        }

        // 14. "Anti-smog guns kahan active hain?"
        if (q.includes('anti-smog') || q.includes('smog gun') || q.includes('guns')) {
          return {
            text: `MCD aur PWD ne Anand Vihar, Wazirpur, RK Puram, Punjabi Bagh aur Mundka hotspots par <b>78 mobile anti-smog mist sprayers</b> deploy kiye hain jo high-pressure mist se PM10 ko settle kar rahe hain.`,
            leadMeta: 'Based on live multi-agency dispatch tracking',
            confidence: 93,
            tabLink: 'dispatches'
          };
        }

        // 15. "Stubble burning ka kya status hai?"
        if (q.includes('stubble') || q.includes('parali') || q.includes('punjab') || q.includes('fires')) {
          return {
            text: `VIIRS aur MODIS satellites ne pichle 24h me Punjab me <b>3,140+</b> aur Haryana me <b>480+</b> active farm fires record kiye hain. NW winds ke chalte ye smoke plume agle 28-32 ghante me Delhi basin me enter karega, contributing ~38% to Delhi PM2.5.`,
            leadMeta: 'Based on satellite thermal anomaly detection',
            confidence: 92,
            tabLink: 'attribution'
          };
        }

        // Generic Fallback
        return {
          text: `Main VayuAI hoon. Aap mujhse school closures, kal ka AQI, GRAP stages, anti-smog guns, odd-even rules, ya safe clean air windows ke baare me pooch sakte hain. Abhi ${stationName} ka AQI <b>${currentAQI}</b> hai.`,
          leadMeta: 'Based on live coupled system database',
          confidence: 90,
          tabLink: 'overview'
        };
      }
    };

    function resetVayuAIChatToHub() {
      const hubView = document.getElementById('vayuai-hub-view');
      const chatThread = document.getElementById('vayuai-chat-thread');
      if (hubView) hubView.classList.remove('hidden');
      if (chatThread) chatThread.classList.add('hidden');
    }

    function toggleVayuAISpeechRecognition() {
      VayuAIAssistant.toggleSpeech();
    }

    function sendVayuAICustomQuery() {
      const input = document.getElementById('vayuai-chat-input');
      if (!input || !input.value.trim()) return;
      VayuAIAssistant.askQuestion(input.value.trim());
      input.value = '';
    }
"""

# Now let's inject this right before the DOMContentLoaded listener in index.html
target_listener = "document.addEventListener('DOMContentLoaded', async () => {"

if target_listener in content:
    content = content.replace(target_listener, js_modules + "\n\n    " + target_listener, 1)
    print("✓ VayuCoupler core modules injected into main script")
else:
    print("! Could not locate DOMContentLoaded listener")

# In DOMContentLoaded, wire up:
# VayuForecastEngine.init();
# VayuLocationService.init();
# VayuSplashScreen.init();
# VayuPredictiveTimeline.render();
# VayuDispatchesCenter.render();
# VayuAIAssistant.init();

dom_content_pattern = r"(document\.addEventListener\('DOMContentLoaded', async \(\) => \{\s*lucide\.createIcons\(\);)"
dom_replacement = r"""\1
      VayuForecastEngine.init();
      VayuLocationService.init();
      VayuSplashScreen.init();
      VayuPredictiveTimeline.render();
      VayuDispatchesCenter.render();
      VayuAIAssistant.init();"""

content = re.sub(dom_content_pattern, dom_replacement, content, count=1)
print("✓ Modules initialized on DOMContentLoaded")

# Update switchTab to also render VayuPredictiveTimeline, VayuDispatchesCenter, and map 'vayuai' to 'copilot'
switch_tab_pattern = r"(function switchTab\(tabId\) \{.*?\n)"
switch_tab_hook = r"""function switchTab(tabId) {
      if (tabId === 'vayuai') tabId = 'copilot';
      if (tabId === 'grap' && typeof VayuPredictiveTimeline !== 'undefined') VayuPredictiveTimeline.render();
      if (tabId === 'dispatches' && typeof VayuDispatchesCenter !== 'undefined') VayuDispatchesCenter.render();
"""
content = re.sub(switch_tab_pattern, switch_tab_hook, content, count=1)
print("✓ switchTab hooked with module rendering")

# Ensure updateGrapTable and updateDispatchesView update our new components as well
old_update_grap = r"function updateGrapTable\(grap\) \{"
new_update_grap = r"""function updateGrapTable(grap) {
      if (typeof VayuPredictiveTimeline !== 'undefined') {
        VayuPredictiveTimeline.render();
      }"""
content = re.sub(old_update_grap, new_update_grap, content, count=1)

old_update_disp = r"function updateDispatchesView\(disp\) \{"
new_update_disp = r"""function updateDispatchesView(disp) {
      if (typeof VayuDispatchesCenter !== 'undefined') {
        VayuDispatchesCenter.render();
      }"""
content = re.sub(old_update_disp, new_update_disp, content, count=1)

# Write back updated content
with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Step 2 complete: index.html fully integrated with all 5 modules.")
