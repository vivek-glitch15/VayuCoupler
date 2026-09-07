#!/usr/bin/env python3
"""
Update backend/app/static/index.html with the complete VayuCoupler Final Feature Build.
"""

import re
import os

INDEX_PATH = "backend/app/static/index.html"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update <head> fonts and tailwind config
old_fonts = re.search(r'(<!-- Fonts -->.*?<script src="https://cdn\.tailwindcss\.com"></script>.*?tailwind\.config\s*=\s*\{.*?\}\s*</script>)', content, re.DOTALL)

new_fonts = """<!-- Fonts: Source Serif 4 (display/headlines), Inter (UI), IBM Plex Mono (data labels) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Inter:wght@400;500;600;700;800&family=Source+Serif+4:ital,opsz,wght@0,8..60,600;0,8..60,700;0,8..60,900;1,8..60,700&display=swap" rel="stylesheet">
  
  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            bg: "#060706",
            surface: "#0b0c0b",
            "surface-2": "#0f110f",
            border: "#1c1f1c",
            "text-primary": "#f2f5f3",
            "text-secondary": "#8b9390",
            "text-tertiary": "#545a57",
            "accent-green": "#6fe2a3",
            "accent-blue": "#6ec8f2",
            "accent-yellow": "#f2d666",
            "accent-red": "#f2966e",
            earth: {
              950: "#060706",
              900: "#0b0c0b",
              850: "#0f110f",
              800: "#151815",
              750: "#1a1f1a",
              700: "#1c1f1c",
              600: "#2d332d",
              500: "#6fe2a3",
              400: "#6ec8f2",
              300: "#a5f3fc",
              200: "#cfdade",
              100: "#f2f5f3"
            }
          },
          fontFamily: {
            serif: ['Source Serif 4', 'Georgia', 'serif'],
            sans: ['Inter', '-apple-system', 'sans-serif'],
            mono: ['IBM Plex Mono', 'monospace']
          }
        }
      }
    }
  </script>"""

if old_fonts:
    content = content.replace(old_fonts.group(1), new_fonts, 1)
    print("✓ Fonts and Tailwind config updated")
else:
    print("! Could not match fonts block")

# 2. Inject Splash Screen, GPS Location Toast, Station Picker Modal, Protocol Modal right after <body>
splash_and_modals_html = """
  <!-- ================= 0. INTRO / COLD LAUNCH SPLASH SCREEN ================= -->
  <div id="splash-screen" class="pb-safe">
    <!-- Drifting Smog / Haze Particles (CSS Only) -->
    <div class="haze-particle" style="width: 140px; height: 140px; left: 8%; animation-delay: 0s; animation-duration: 9s;"></div>
    <div class="haze-particle" style="width: 90px; height: 90px; left: 32%; animation-delay: 2.2s; animation-duration: 11s;"></div>
    <div class="haze-particle" style="width: 160px; height: 160px; left: 58%; animation-delay: 4.5s; animation-duration: 8.5s;"></div>
    <div class="haze-particle" style="width: 110px; height: 110px; left: 78%; animation-delay: 1.5s; animation-duration: 10s;"></div>
    <div class="haze-particle" style="width: 130px; height: 130px; left: 20%; animation-delay: 6s; animation-duration: 12s;"></div>

    <!-- Central Content Box -->
    <div class="flex flex-col items-center justify-center text-center max-w-sm px-6 z-10 relative cursor-pointer" onclick="VayuSplashScreen.handleUserTapSkip()">
      <!-- App Mark (0.0-0.8s) -->
      <div id="splash-app-mark" class="w-16 h-16 sm:w-20 sm:h-20 rounded-2xl bg-gradient-to-br from-[#6fe2a3] to-[#6ec8f2] p-0.5 shadow-2xl shadow-emerald-950/60 mb-3 transition-all duration-700 transform scale-90 opacity-0 flex items-center justify-center">
        <div class="w-full h-full bg-[#0b0c0b] rounded-[14px] flex items-center justify-center">
          <svg class="w-8 h-8 sm:w-10 sm:h-10 text-[#6fe2a3] svg-icon-line" viewBox="0 0 24 24" stroke="currentColor">
            <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
          </svg>
        </div>
      </div>

      <!-- Wordmark & Subtitle (0.7-1.3s) -->
      <div id="splash-title-wrap" class="opacity-0 transition-all duration-700 transform translate-y-2 mb-4">
        <h1 class="text-2xl sm:text-3xl font-black tracking-tight text-white font-serif-display">VayuCoupler</h1>
        <p class="text-xs text-[#8b9390] mt-1 font-sans-ui">Delhi-NCR Coupled AQI Forecast</p>
      </div>

      <!-- Circular SVG Gauge & Live AQI Count-Up (1.3-3.2s) -->
      <div id="splash-gauge-wrap" class="relative w-44 h-44 sm:w-48 sm:h-48 flex items-center justify-center mb-4 opacity-0 transition-all duration-700">
        <svg class="w-full h-full transform -rotate-90" viewBox="0 0 120 120">
          <circle cx="60" cy="60" r="50" class="splash-gauge-bg"/>
          <defs>
            <linearGradient id="splashGaugeGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#6fe2a3"/>
              <stop offset="50%" stop-color="#f2d666"/>
              <stop offset="100%" stop-color="#f2966e"/>
            </linearGradient>
          </defs>
          <circle id="splash-gauge-ring" cx="60" cy="60" r="50" class="splash-gauge-fill" stroke="url(#splashGaugeGrad)" stroke-dasharray="314.159" stroke-dashoffset="314.159"/>
        </svg>
        <div class="absolute inset-0 flex flex-col items-center justify-center">
          <span class="text-[9px] sm:text-[10px] font-mono-data text-[#8b9390] uppercase tracking-wider">Live Station AQI</span>
          <span id="splash-aqi-number" class="text-4xl sm:text-5xl font-black text-white font-serif-display my-0.5">0</span>
          <span id="splash-aqi-severity" class="text-[10px] font-mono-tag font-bold px-2.5 py-0.5 rounded-full badge-red">INITIALIZING</span>
        </div>
      </div>

      <!-- Live GPS Location Line (~3.4s) -->
      <div id="splash-location-line" class="text-xs text-[#8b9390] opacity-0 transition-all duration-600 mb-4 flex items-center gap-1.5 font-sans-ui">
        <svg class="w-3.5 h-3.5 text-[#6fe2a3] svg-icon-line" viewBox="0 0 24 24" stroke="currentColor"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
        <span>Live at <b class="text-white" id="splash-station-name">Punjabi Bagh</b> · <span id="splash-station-dist">6.2 km</span> away</span>
      </div>

      <!-- Syncing 72-Hour Forecast Status & Progress Bar (~4.2s) -->
      <div id="splash-status-wrap" class="w-full max-w-[210px] opacity-0 transition-all duration-600 flex flex-col items-center gap-1.5">
        <div class="flex items-center justify-between w-full text-[9px] font-mono-data text-[#8b9390] uppercase tracking-wider">
          <span>SYNCING 72-HOUR FORECAST</span>
          <span id="splash-sync-pct">0%</span>
        </div>
        <div class="w-full h-1 bg-[#151815] rounded-full overflow-hidden border border-[#1c1f1c]">
          <div id="splash-progress-bar" class="h-full bg-gradient-to-r from-[#6fe2a3] to-[#6ec8f2] w-0 transition-all duration-100 ease-out"></div>
        </div>
      </div>

      <!-- Tap to skip prompt (activates once AQI finishes count-up) -->
      <div id="splash-skip-hint" class="mt-4 text-[10px] font-mono-data text-[#545a57] opacity-0 transition-opacity duration-300">
        Tap anywhere to enter →
      </div>
    </div>
  </div>

  <!-- ================= GPS LOCATION AUTO-TOAST BANNER ================= -->
  <div id="gps-location-toast" class="hidden">
    <div class="p-3.5 flex items-center justify-between gap-3">
      <div class="flex items-center gap-2.5 min-w-0">
        <div class="w-8 h-8 rounded-xl bg-[#10201a] border border-[#1f3d30] flex items-center justify-center text-[#6fe2a3] shrink-0">
          <svg class="w-4 h-4 svg-icon-line" viewBox="0 0 24 24" stroke="currentColor"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
        </div>
        <div class="min-w-0">
          <div class="text-xs font-bold text-white flex items-center gap-1.5 truncate font-sans-ui">
            <span>Local Air Quality Set to Your Location</span>
          </div>
          <div class="text-[11px] text-[#8b9390] truncate font-mono-data" id="toast-station-subtext">
            Punjabi Bagh • 6.2 km away • AQI 431
          </div>
        </div>
      </div>
      <button onclick="dismissLocationToast()" class="p-1 rounded-lg text-[#8b9390] hover:text-white hover:bg-[#1c1f1c] shrink-0 transition text-sm">
        ✕
      </button>
    </div>
    <div class="toast-progress-bar" id="toast-progress-bar"></div>
  </div>

  <!-- ================= MANUAL STATION PICKER MODAL ================= -->
  <div id="station-picker-modal" class="fixed inset-0 z-50 bg-black/80 backdrop-blur-md hidden flex items-center justify-center p-4">
    <div class="surface-panel p-5 sm:p-6 rounded-2xl max-w-md w-full border border-[#1c1f1c] shadow-2xl relative flex flex-col gap-3.5">
      <div class="flex items-center justify-between pb-3 border-b border-[#1c1f1c]">
        <div>
          <h3 class="text-base font-bold text-white font-serif-display flex items-center gap-2">
            <span>📍 Select Monitoring Station</span>
          </h3>
          <p class="text-xs text-[#8b9390] mt-0.5 font-sans-ui">Choose any Delhi-NCR sensor station to inspect localized AQI</p>
        </div>
        <button onclick="closeStationPickerModal()" class="text-[#8b9390] hover:text-white p-1 rounded-lg hover:bg-[#1c1f1c] text-sm">
          ✕
        </button>
      </div>

      <input type="text" id="station-search-input" placeholder="Search station (e.g. Anand Vihar, Gurugram)..." oninput="filterStationsList(this.value)" class="px-3.5 py-2.5 rounded-xl bg-[#0f110f] border border-[#1c1f1c] text-xs text-white placeholder-[#545a57] focus:outline-none focus:border-[#6fe2a3] font-sans-ui">

      <div id="stations-picker-list" class="flex flex-col gap-2 max-h-[300px] overflow-y-auto no-scrollbar">
        <!-- Generated dynamically via VayuLocationService -->
      </div>
    </div>
  </div>

  <!-- ================= PROTOCOL DETAIL SHEET MODAL (DISPATCHES) ================= -->
  <div id="protocol-modal" class="fixed inset-0 z-50 bg-black/80 backdrop-blur-md hidden flex items-center justify-center p-4">
    <div class="surface-panel p-5 sm:p-6 rounded-2xl max-w-lg w-full border border-[#1c1f1c] shadow-2xl relative flex flex-col gap-4 max-h-[90vh] overflow-y-auto">
      <button onclick="closeProtocolModal()" class="absolute top-4 right-4 text-[#8b9390] hover:text-white p-1.5 rounded-lg hover:bg-[#1c1f1c] text-sm z-10">
        ✕
      </button>
      <div id="protocol-modal-content">
        <!-- Populated dynamically based on tapped agency -->
      </div>
    </div>
  </div>
"""

body_tag = '<body class="min-h-screen text-slate-100 flex flex-col antialiased selection:bg-cyan-500/30 selection:text-cyan-200 overflow-x-hidden max-w-full w-full">'
if body_tag in content:
    content = content.replace(body_tag, body_tag + splash_and_modals_html, 1)
    print("✓ Splash screen and modals injected after <body>")
else:
    print("! Could not find body tag")

# 3. Update Header location pill & actions
header_top_row_pattern = r'(<!-- Top Row: Identity \+ Quick Actions -->.*?<header.*?>.*?)<div class="max-w-\[1720px\] mx-auto px-3 sm:px-6 py-2 sm:py-2\.5 flex items-center justify-between gap-2 sm:gap-4 w-full">.*?<!-- Actions: Fullscreen, Alert, Pause, Reset -->'
header_top_replacement = """<!-- Top Row: Identity + Location Pill + Quick Actions -->
    <div class="max-w-[1720px] mx-auto px-3 sm:px-6 py-2 sm:py-2.5 flex items-center justify-between gap-2 sm:gap-4 w-full">
      
      <!-- Identity -->
      <div class="flex items-center gap-2 sm:gap-2.5 min-w-0">
        <img src="/static/icon-192.png?v=6" class="w-8 h-8 sm:w-9 sm:h-9 rounded-xl border border-[#1f3d30] shadow-lg object-cover ring-1 ring-[#6fe2a3]/30 shrink-0">
        <div class="min-w-0">
          <h1 class="text-sm sm:text-base font-bold text-white tracking-tight flex items-center gap-1.5 truncate font-serif-display">
            <span>VayuCoupler</span>
            <span class="hidden sm:inline text-xs text-[#8b9390] font-sans-ui font-normal">| Delhi-NCR</span>
            <span class="hidden sm:inline-flex items-center gap-1 text-[10px] font-bold text-[#6fe2a3] bg-[#10201a] px-2 py-0.5 rounded-full border border-[#1f3d30] shrink-0 font-mono-tag">
              <span class="w-1.5 h-1.5 rounded-full bg-[#6fe2a3] animate-pulse"></span> PREDICTIVE GRAP
            </span>
          </h1>
          <div class="text-[10px] text-[#8b9390] font-medium truncate font-mono-data">MoES Atmospheric Coupled System</div>
        </div>
      </div>

      <!-- Center / Location Pill & Live AQI Badge -->
      <div class="flex items-center gap-1.5 sm:gap-2 min-w-0">
        <!-- Clickable Location Pill (Opens Station Picker) -->
        <button onclick="openStationPickerModal()" id="header-location-pill" class="px-2.5 py-1.5 rounded-xl bg-[#0f110f] hover:bg-[#141714] border border-[#1c1f1c] hover:border-[#6fe2a3]/40 text-[#f2f5f3] flex items-center gap-1.5 text-xs font-mono-data transition shadow-sm" title="Tap to select another station or refresh GPS">
          <span class="w-2 h-2 rounded-full bg-[#6fe2a3] animate-pulse shrink-0"></span>
          <span id="header-station-text" class="font-bold truncate max-w-[120px] sm:max-w-[180px]">Punjabi Bagh (6.2 km)</span>
          <svg class="w-3 h-3 text-[#8b9390] svg-icon-line shrink-0" viewBox="0 0 24 24" stroke="currentColor"><path d="M6 9l6 6 6-6"/></svg>
        </button>

        <!-- Live AQI Severity Pill -->
        <div id="header-aqi-badge" class="px-2.5 py-1.5 rounded-xl badge-red flex items-center gap-1.5 text-xs font-mono-data font-bold shadow-sm shrink-0">
          <span id="header-aqi-val">AQI 431</span>
          <span class="text-[9px] uppercase text-[#f2966e] hidden sm:inline" id="header-aqi-severity">SEVERE</span>
        </div>

        <!-- GPS Re-detect Button -->
        <button onclick="refreshGPSLocation()" class="w-8 h-8 rounded-xl bg-[#0f110f] hover:bg-[#141714] text-[#6fe2a3] border border-[#1c1f1c] flex items-center justify-center transition shadow-sm shrink-0" title="Detect Exact GPS Coordinates">
          <svg class="w-3.5 h-3.5 svg-icon-line" viewBox="0 0 24 24" stroke="currentColor"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
        </button>
      </div>

      <!-- Actions: Fullscreen, Alert, Pause, Reset -->"""

content = re.sub(
    r'<div class="max-w-\[1720px\] mx-auto px-3 sm:px-6 py-2 sm:py-2\.5 flex items-center justify-between gap-2 sm:gap-4 w-full">.*?<!-- Actions: Fullscreen, Alert, Pause, Reset -->',
    header_top_replacement,
    content,
    flags=re.DOTALL
)
print("✓ Header location pill and AQI badge injected")

# 4. Replace panel-copilot with VayuAI Assistant Hub Layout
old_copilot_pattern = r'<div id="panel-copilot" class="tab-panel hidden flex flex-col gap-4">.*?</div>\s*<!-- === TAB: CLEAN AIR WINDOWS'

new_copilot_html = """<!-- === TAB: VAYU AI ASSISTANT HUB === -->
    <div id="panel-copilot" class="tab-panel hidden flex flex-col gap-4 w-full max-w-full">
      <div class="surface-panel p-4 sm:p-6 rounded-2xl sm:rounded-3xl border border-[#1c1f1c] shadow-xl flex flex-col">
        
        <!-- HUB HOME VIEW (Default state) -->
        <div id="vayuai-hub-view" class="flex flex-col items-center text-center py-2">
          
          <!-- Centered Glowing Orb Hero (Radial gradient green -> blue) -->
          <div class="mb-3 vayuai-glowing-orb">
            <svg class="w-9 h-9 text-[#060706] svg-icon-line" viewBox="0 0 24 24" stroke="currentColor">
              <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/>
            </svg>
          </div>

          <h2 class="text-2xl sm:text-3xl font-black text-white font-serif-display">Poocho VayuAI se</h2>
          <p class="text-xs sm:text-sm text-[#8b9390] mt-1.5 max-w-md font-sans-ui leading-relaxed">
            Delhi-NCR ke 72-hour coupled forecast, meteorology physics aur GRAP rules par aadharit instant answers.
          </p>

          <!-- 2-Column Grid of Question Cards (All 15 Preset Intents) -->
          <div class="w-full mt-6 text-left">
            <div class="flex items-center justify-between mb-2.5 px-1">
              <span class="text-[11px] font-mono-data text-[#8b9390] uppercase tracking-wider">POPULAR QUERIES (15 INTENTS)</span>
              <span class="text-[10px] font-mono-tag text-[#6fe2a3]">TAP TO ASK</span>
            </div>
            <div class="vayuai-questions-grid" id="vayuai-questions-grid">
              <!-- Rendered dynamically via VayuAIAssistant -->
            </div>
          </div>
        </div>

        <!-- CHAT THREAD VIEW (Transitions after query) -->
        <div id="vayuai-chat-thread" class="hidden flex flex-col gap-3 py-1">
          <div class="flex items-center justify-between pb-3 border-b border-[#1c1f1c]">
            <div class="flex items-center gap-2">
              <div class="w-8 h-8 rounded-full bg-gradient-to-br from-[#6fe2a3] to-[#6ec8f2] flex items-center justify-center text-[#060706] font-bold text-xs">V</div>
              <div>
                <div class="text-xs font-bold text-white font-serif-display">VayuAI Assistant</div>
                <div class="text-[10px] text-[#8b9390] font-mono-data">72h Coupled Forecast Grounded</div>
              </div>
            </div>
            <button onclick="resetVayuAIChatToHub()" class="px-2.5 py-1 rounded-lg bg-[#0f110f] hover:bg-[#161a16] border border-[#1c1f1c] text-[#8b9390] hover:text-white text-[11px] font-mono transition flex items-center gap-1">
              <span>← Back to Questions</span>
            </button>
          </div>

          <!-- Chat History -->
          <div id="vayuai-chat-history" class="p-3 sm:p-4 rounded-xl sm:rounded-2xl bg-[#060706] border border-[#1c1f1c] min-h-[260px] max-h-[420px] overflow-y-auto flex flex-col gap-3 text-xs font-sans-ui">
            <!-- Messages populated here -->
          </div>
        </div>

        <!-- Voice Speech Feedback Banner -->
        <div id="vayuai-mic-feedback" class="hidden my-2 p-2.5 rounded-xl bg-[#1f150f] border border-[#4a2e20] text-xs flex items-center justify-between">
          <div class="flex items-center gap-2 min-w-0">
            <span class="w-2 h-2 rounded-full bg-[#f2966e] animate-ping shrink-0"></span>
            <span class="text-[#f2966e] font-mono-tag font-bold text-[10px] uppercase">SUN RAHA HOON...</span>
            <span id="vayuai-live-speech-transcript" class="text-white italic truncate text-[11px]">Boliye...</span>
          </div>
          <span class="text-[9px] font-mono-tag px-2 py-0.5 rounded badge-yellow shrink-0">Hinglish detected</span>
        </div>

        <!-- Pill-Shaped Input Bar with Speech Mic & Circular Send -->
        <div class="mt-4 pt-3 border-t border-[#1c1f1c]">
          <div class="flex items-center gap-2 p-1.5 pl-3.5 rounded-full bg-[#060706] border border-[#1c1f1c] focus-within:border-[#6fe2a3] transition shadow-inner">
            <input type="text" id="vayuai-chat-input" placeholder="Apna sawaal likhein ya mic dabayein..." onkeydown="if(event.key==='Enter') sendVayuAICustomQuery()" class="flex-1 bg-transparent text-xs text-white placeholder-[#545a57] focus:outline-none min-w-0 font-sans-ui">
            
            <!-- Speech Mic Button -->
            <div class="mic-btn-container" id="vayuai-mic-container">
              <span class="mic-pulse-ring"></span>
              <span class="mic-pulse-ring"></span>
              <button onclick="toggleVayuAISpeechRecognition()" id="vayuai-mic-btn" class="w-8 h-8 rounded-full bg-[#0f110f] hover:bg-[#161a16] text-[#6ec8f2] flex items-center justify-center transition border border-[#1c1f1c]" title="Voice input in Hindi / Hinglish">
                <svg class="w-4 h-4 svg-icon-line" viewBox="0 0 24 24" stroke="currentColor"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/></svg>
              </button>
            </div>

            <!-- Send Button -->
            <button onclick="sendVayuAICustomQuery()" class="w-8 h-8 rounded-full bg-[#6fe2a3] hover:bg-[#5cd493] text-[#060706] flex items-center justify-center transition shadow-md shrink-0 active:scale-95" title="Send Question">
              <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
            </button>
          </div>
        </div>

      </div>
    </div>

    <!-- === TAB: CLEAN AIR WINDOWS"""

content = re.sub(old_copilot_pattern, new_copilot_html, content, flags=re.DOTALL)
print("✓ panel-copilot replaced with VayuAI Hub layout")

# 5. Replace panel-grap and panel-dispatches
grap_and_disp_pattern = r'<!-- === TAB 2: PREDICTIVE GRAP RULES MATRIX === -->.*?<!-- === TAB 4: WHAT-IF POLICY SIMULATOR === -->'

new_grap_and_disp_html = """<!-- === TAB 2: PREDICTIVE GRAP ACTION PLAN ENGINE === -->
    <div id="panel-grap" class="tab-panel hidden flex flex-col gap-4 sm:gap-6 w-full max-w-full">
      <div class="surface-panel p-4 sm:p-6 rounded-2xl sm:rounded-3xl border border-[#1c1f1c] shadow-xl">
        <!-- Hero Section -->
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-3 pb-5 border-b border-[#1c1f1c]">
          <div>
            <div class="flex items-center gap-2 mb-1">
              <span class="text-[10px] font-mono-tag font-bold px-2.5 py-0.5 rounded-full badge-blue uppercase">PREDICTIVE RESPONSE PLAN</span>
              <span class="text-[10px] font-mono-tag text-[#8b9390]">72H COUPLED WRF-CHEM</span>
            </div>
            <h2 class="text-xl sm:text-2xl font-black text-white font-serif-display">Response Action Plan Engine</h2>
            <p class="text-xs sm:text-sm text-[#8b9390] mt-1 max-w-2xl font-sans-ui leading-relaxed">
              Forecast-triggered interventions giving <b>24–72 hours</b> of pre-emptive lead time before meteorological boundary layer compression traps toxic particulates.
            </p>
          </div>
          <div class="p-3.5 rounded-2xl bg-[#0f110f] border border-[#1c1f1c] font-mono-data shrink-0 flex flex-col items-start md:items-end">
            <div class="text-[10px] text-[#8b9390] uppercase tracking-wider">MAX LEAD TIME GAINED</div>
            <div class="text-xl sm:text-2xl font-black text-[#6fe2a3] mt-0.5" id="grap-max-lead-gained">GAINED 48 Hours</div>
          </div>
        </div>

        <!-- Vertical Connected Timeline Container -->
        <div class="mt-6 timeline-track-container" id="grap-timeline-container">
          <div class="timeline-track-line"></div>
          <div id="grap-timeline-items" class="flex flex-col gap-6">
            <!-- Dynamically populated via VayuPredictiveTimeline -->
          </div>
        </div>
      </div>
    </div>

    <!-- === TAB 3: STAKEHOLDER ACTION DISPATCH CENTER === -->
    <div id="panel-dispatches" class="tab-panel hidden flex flex-col gap-4 sm:gap-6 w-full max-w-full">
      <div class="surface-panel p-4 sm:p-6 rounded-2xl sm:rounded-3xl border border-[#1c1f1c] shadow-xl">
        <!-- Top Banner Row -->
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-3 pb-5 border-b border-[#1c1f1c]">
          <div>
            <div class="flex items-center gap-2 mb-1.5 flex-wrap">
              <span class="text-[10px] font-mono-tag font-bold px-2.5 py-0.5 rounded-full badge-red uppercase flex items-center gap-1.5">
                <span class="w-1.5 h-1.5 rounded-full bg-[#f2966e] animate-ping"></span> LIVE MULTI-AGENCY DISPATCH
              </span>
              <span class="text-[10px] font-mono-tag font-bold px-2.5 py-0.5 rounded-full badge-blue uppercase" id="dispatch-agency-count-pill">
                7 Coordinated Agencies
              </span>
              <span class="text-[10px] font-mono-data text-[#8b9390]" id="dispatch-t-hour-counter">
                T-HOUR 83 OF 167
              </span>
            </div>
            <h2 class="text-xl sm:text-2xl font-black text-white font-serif-display">Stakeholder Action Dispatch Center</h2>
            <p class="text-xs sm:text-sm text-[#8b9390] mt-1 max-w-3xl font-sans-ui leading-relaxed">
              Pre-emptive directives dispatched with <span class="text-[#6fe2a3] font-mono-data font-semibold" id="dispatch-lead-time-text">48h</span> lead time. Tap any agency tile below to view the official protocol, mandate checklist &amp; evidence.
            </p>
          </div>
          <!-- Severity Headline -->
          <div class="p-3.5 rounded-2xl bg-[#0f110f] border border-[#1c1f1c] font-mono-data shrink-0">
            <div class="text-[10px] text-[#8b9390] uppercase tracking-wider">CURRENT SEVERITY</div>
            <div class="text-sm sm:text-base font-black text-[#f2966e] font-serif-display mt-0.5" id="dispatch-severity-headline">
              Emergency — AQI 431
            </div>
          </div>
        </div>

        <!-- 2-Column Grid of Agency Tiles -->
        <div class="mt-6 agency-tile-grid" id="agency-tiles-grid">
          <!-- Dynamically populated via VayuDispatchesCenter -->
        </div>
      </div>
    </div>

    <!-- === TAB 4: WHAT-IF POLICY SIMULATOR === -->"""

content = re.sub(grap_and_disp_pattern, new_grap_and_disp_html, content, flags=re.DOTALL)
print("✓ panel-grap and panel-dispatches replaced with Timeline and 2-Column Grid")

# 6. Update Mobile Bottom Nav to clearly feature the primary 5 tabs:
# (Command Center · Predictive · VayuAI · What-If Sim · Dispatches)
mob_nav_pattern = r'<nav class="md:hidden mobile-nav-bar pb-safe".*?</nav>'

new_mob_nav_html = """<nav class="md:hidden mobile-nav-bar pb-safe" aria-label="Mobile Navigation">
    <button onclick="switchTab('overview')" id="mob-tab-overview" class="mobile-nav-item active" title="Command Center">
      <svg class="svg-icon-line" viewBox="0 0 24 24" stroke="currentColor"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
      <span>Command</span>
    </button>
    <button onclick="switchTab('grap')" id="mob-tab-grap" class="mobile-nav-item" title="Predictive Action Plan">
      <svg class="svg-icon-line" viewBox="0 0 24 24" stroke="currentColor"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
      <span>Predictive</span>
    </button>
    <button onclick="switchTab('copilot')" id="mob-tab-copilot" class="mobile-nav-item" title="VayuAI Assistant">
      <svg class="svg-icon-line" viewBox="0 0 24 24" stroke="currentColor"><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/></svg>
      <span>VayuAI</span>
    </button>
    <button onclick="switchTab('whatif')" id="mob-tab-whatif" class="mobile-nav-item" title="What-If Sim">
      <svg class="svg-icon-line" viewBox="0 0 24 24" stroke="currentColor"><line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/><line x1="1" y1="14" x2="7" y2="14"/><line x1="9" y1="8" x2="15" y2="8"/><line x1="17" y1="16" x2="23" y2="16"/></svg>
      <span>What-If</span>
    </button>
    <button onclick="switchTab('dispatches')" id="mob-tab-dispatches" class="mobile-nav-item" title="Dispatches Center">
      <svg class="svg-icon-line" viewBox="0 0 24 24" stroke="currentColor"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
      <span>Dispatches</span>
    </button>
    <button onclick="switchTab('commute')" id="mob-tab-commute" class="mobile-nav-item" title="Safe Commute">
      <svg class="svg-icon-line" viewBox="0 0 24 24" stroke="currentColor"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>
      <span>Commute</span>
    </button>
    <button onclick="openMobileAppModal()" id="mob-tab-install" class="mobile-nav-item mobile-nav-install" title="Download App">
      <svg class="svg-icon-line animate-bounce" viewBox="0 0 24 24" stroke="currentColor"><rect x="5" y="2" width="14" height="20" rx="2" ry="2"/><line x1="12" y1="18" x2="12.01" y2="18"/></svg>
      <span>Install</span>
    </button>
  </nav>"""

content = re.sub(mob_nav_pattern, new_mob_nav_html, content, flags=re.DOTALL)
print("✓ Mobile bottom nav updated")

# Write out the updated HTML so far
with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Step 1 complete: index.html markup successfully updated.")
