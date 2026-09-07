import React, { useState, useEffect } from 'react';
import { 
  Wind, ShieldAlert, Send, Sliders, GitMerge, LayoutDashboard, 
  RotateCcw, Play, Pause, Activity, Gauge, Layers, Thermometer, 
  Compass, Flame, MapPin, TrendingUp, PieChart, CheckCircle, Radio
} from 'lucide-react';
import { 
  fetchStations, fetchSnapshot, fetchStationForecast, 
  fetchGrapTriggers, fetchDispatches, fetchInterstateGrid, runWhatIfSimulation 
} from './services/api';

export default function App() {
  const [currentStep, setCurrentStep] = useState(72);
  const [isPlaying, setIsPlaying] = useState(false);
  const [activeTab, setActiveTab] = useState('overview');
  const [selectedStationId, setSelectedStationId] = useState('DEL001');
  const [selectedRoleId, setSelectedRoleId] = useState('ROLE_AGRI');

  const [snapshot, setSnapshot] = useState(null);
  const [stationFc, setStationFc] = useState(null);
  const [grapData, setGrapData] = useState(null);
  const [dispatches, setDispatches] = useState(null);
  const [interstate, setInterstate] = useState(null);
  const [whatIfData, setWhatIfData] = useState(null);

  const [stubbleVal, setStubbleVal] = useState(50);
  const [truckVal, setTruckVal] = useState(40);
  const [dustVal, setDustVal] = useState(30);
  const [industryVal, setIndustryVal] = useState(20);

  // Load data
  useEffect(() => {
    async function loadData() {
      try {
        const [snap, sFc, grap, disp, inter] = await Promise.all([
          fetchSnapshot(currentStep),
          fetchStationForecast(selectedStationId, currentStep),
          fetchGrapTriggers(currentStep),
          fetchDispatches(currentStep),
          fetchInterstateGrid(currentStep)
        ]);
        setSnapshot(snap);
        setStationFc(sFc);
        setGrapData(grap);
        setDispatches(disp);
        setInterstate(inter);
      } catch (err) {
        console.error("API error", err);
      }
    }
    loadData();
  }, [currentStep, selectedStationId]);

  // Handle Playback
  useEffect(() => {
    let interval = null;
    if (isPlaying) {
      interval = setInterval(() => {
        setCurrentStep((prev) => (prev >= 167 ? 0 : prev + 1));
      }, 700);
    }
    return () => clearInterval(interval);
  }, [isPlaying]);

  const handleWhatIf = async () => {
    try {
      const res = await runWhatIfSimulation({
        step_hour: currentStep,
        stubble_reduction_pct: stubbleVal,
        truck_reduction_pct: truckVal,
        dust_reduction_pct: dustVal,
        industry_switch_pct: industryVal
      });
      setWhatIfData(res);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    handleWhatIf();
  }, [currentStep, stubbleVal, truckVal, dustVal, industryVal]);

  if (!snapshot) {
    return (
      <div className="min-h-screen bg-[#0B0F17] flex items-center justify-center text-cyan-400 font-mono">
        <div className="flex items-center gap-3">
          <div className="w-5 h-5 border-2 border-cyan-400 border-t-transparent rounded-full animate-spin"></div>
          <span>Connecting to MoES Coupled Forecasting Engine...</span>
        </div>
      </div>
    );
  }

  const met = snapshot.meteorology;
  const fires = snapshot.stubble_burning;
  const currSt = snapshot.stations.find(s => s.station_id === selectedStationId) || snapshot.stations[0];

  return (
    <div className="min-h-screen bg-[#0B0F17] text-slate-100 flex flex-col font-sans">
      
      {/* Top Navigation */}
      <header className="sticky top-0 z-50 bg-slate-900/80 backdrop-blur-md border-b border-slate-800 px-6 py-3">
        <div className="max-w-[1720px] mx-auto flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-600 to-blue-600 flex items-center justify-center shadow-lg shadow-cyan-500/20">
              <Wind className="w-5 h-5 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-cyan-950 text-cyan-400 border border-cyan-800 font-mono">SIH26082 • MoES</span>
                <span className="text-xs text-slate-400">Delhi NCR Coupled Forecasting System</span>
              </div>
              <h1 className="text-sm md:text-base font-bold text-white tracking-tight flex items-center gap-2">
                Air Pollution–Weather Coupled Early Warning System
                <span className="text-[11px] font-semibold text-emerald-400 bg-emerald-950/60 px-2 py-0.5 rounded-full border border-emerald-800/50">
                  PREDICTIVE GRAP ACTIVE
                </span>
              </h1>
            </div>
          </div>

          <nav className="flex items-center bg-slate-950 p-1 rounded-xl border border-slate-800 text-xs font-medium">
            <button 
              onClick={() => setActiveTab('overview')} 
              className={`px-3 py-1.5 rounded-lg flex items-center gap-1.5 transition ${activeTab === 'overview' ? 'text-cyan-400 bg-cyan-950 border border-cyan-800' : 'text-slate-400 hover:text-white'}`}>
              <LayoutDashboard className="w-4 h-4" /> Command Center
            </button>
            <button 
              onClick={() => setActiveTab('grap')} 
              className={`px-3 py-1.5 rounded-lg flex items-center gap-1.5 transition ${activeTab === 'grap' ? 'text-cyan-400 bg-cyan-950 border border-cyan-800' : 'text-slate-400 hover:text-white'}`}>
              <ShieldAlert className="w-4 h-4" /> Predictive GRAP
            </button>
            <button 
              onClick={() => setActiveTab('dispatches')} 
              className={`px-3 py-1.5 rounded-lg flex items-center gap-1.5 transition ${activeTab === 'dispatches' ? 'text-cyan-400 bg-cyan-950 border border-cyan-800' : 'text-slate-400 hover:text-white'}`}>
              <Send className="w-4 h-4" /> Dispatches
            </button>
            <button 
              onClick={() => setActiveTab('whatif')} 
              className={`px-3 py-1.5 rounded-lg flex items-center gap-1.5 transition ${activeTab === 'whatif' ? 'text-cyan-400 bg-cyan-950 border border-cyan-800' : 'text-slate-400 hover:text-white'}`}>
              <Sliders className="w-4 h-4" /> What-If Sim
            </button>
            <button 
              onClick={() => setActiveTab('interstate')} 
              className={`px-3 py-1.5 rounded-lg flex items-center gap-1.5 transition ${activeTab === 'interstate' ? 'text-cyan-400 bg-cyan-950 border border-cyan-800' : 'text-slate-400 hover:text-white'}`}>
              <GitMerge className="w-4 h-4" /> Inter-State Grid
            </button>
          </nav>
        </div>
      </header>

      {/* Time Scrubber */}
      <section className="bg-slate-950 border-b border-slate-800 px-6 py-3">
        <div className="max-w-[1720px] mx-auto flex flex-col md:flex-row items-center gap-4">
          <div className="flex items-center gap-2 shrink-0">
            <button 
              onClick={() => setIsPlaying(!isPlaying)}
              className="w-8 h-8 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white flex items-center justify-center">
              {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
            </button>
            <span className="text-xs font-mono font-bold text-cyan-400 bg-slate-900 px-2 py-1 rounded border border-slate-800">
              T-Hour: {currentStep} / 167
            </span>
          </div>

          <div className="flex-1 w-full flex flex-col gap-1">
            <div className="flex items-center justify-between text-[11px] font-mono text-slate-400">
              <span>Day 1: Moderate</span>
              <span className="text-amber-400">Day 3: Inversion Alerts (T-72h)</span>
              <span className="text-rose-400 font-bold">Day 5: Peak Smog Crisis</span>
              <span className="text-emerald-400">Day 7: Dispersal</span>
            </div>
            <input 
              type="range" 
              min="0" 
              max="167" 
              value={currentStep} 
              onChange={(e) => setCurrentStep(parseInt(e.target.value))}
              className="w-full"
            />
          </div>

          <div className="flex items-center gap-1.5 shrink-0 text-xs">
            <button onClick={() => setCurrentStep(24)} className="px-2.5 py-1 rounded bg-slate-900 hover:bg-slate-800 border border-slate-800">T-24h</button>
            <button onClick={() => setCurrentStep(72)} className="px-2.5 py-1 rounded bg-amber-950 text-amber-300 border border-amber-800 font-semibold">T-72h ⚡</button>
            <button onClick={() => setCurrentStep(96)} className="px-2.5 py-1 rounded bg-rose-950 text-rose-300 border border-rose-800 font-bold">T-96h 🚨</button>
            <button onClick={() => setCurrentStep(120)} className="px-2.5 py-1 rounded bg-purple-950 text-purple-300 border border-purple-800 font-bold">Peak</button>
            <button onClick={() => setCurrentStep(156)} className="px-2.5 py-1 rounded bg-emerald-950 text-emerald-300 border border-emerald-800">Recovery</button>
          </div>
        </div>
      </section>

      {/* Telemetry Bar */}
      <main className="flex-1 max-w-[1720px] w-full mx-auto p-6 flex flex-col gap-6">
        <section className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
          
          <div className="bg-slate-900/90 border border-slate-800 p-4 rounded-xl border-l-4" style={{ borderLeftColor: snapshot.category_color }}>
            <div className="text-xs text-slate-400">DELHI NCR AVG AQI</div>
            <div className="my-1.5 flex items-baseline gap-2">
              <span className="text-3xl font-black font-mono">{snapshot.delhi_ncr_avg_aqi}</span>
              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full" style={{ backgroundColor: snapshot.category_color + '33', color: snapshot.category_color }}>
                {snapshot.category}
              </span>
            </div>
            <div className="text-[11px] text-slate-400">PM2.5: {currSt?.pm25} μg/m³</div>
          </div>

          <div className="bg-slate-900/90 border border-slate-800 p-4 rounded-xl border-l-4 border-cyan-500">
            <div className="text-xs text-cyan-400 font-semibold">VENTILATION INDEX</div>
            <div className="my-1.5 text-2xl font-black font-mono text-cyan-300">
              {met.ventilation_index_m2s} <span className="text-xs text-slate-400">m²/s</span>
            </div>
            <div className={`text-[11px] font-medium ${met.ventilation_index_m2s < 2000 ? 'text-rose-400' : 'text-emerald-400'}`}>
              {met.ventilation_status}
            </div>
          </div>

          <div className="bg-slate-900/90 border border-slate-800 p-4 rounded-xl border-l-4 border-indigo-500">
            <div className="text-xs text-slate-400">BOUNDARY LAYER (PBLH)</div>
            <div className="my-1.5 text-2xl font-black font-mono text-indigo-200">
              {met.boundary_layer_height_m} <span className="text-xs text-slate-400">m</span>
            </div>
            <div className="text-[11px] text-slate-400">{met.boundary_layer_height_m < 500 ? "Severe Trapping" : "Normal Dispersion"}</div>
          </div>

          <div className="bg-slate-900/90 border border-slate-800 p-4 rounded-xl border-l-4 border-amber-500">
            <div className="text-xs text-slate-400">THERMAL INVERSION (ΔT)</div>
            <div className="my-1.5 text-2xl font-black font-mono text-amber-300">
              {met.inversion_strength_c} <span className="text-xs text-slate-400">°C</span>
            </div>
            <div className="text-[11px] text-slate-400">Nocturnal Trapping</div>
          </div>

          <div className="bg-slate-900/90 border border-slate-800 p-4 rounded-xl border-l-4 border-blue-500">
            <div className="text-xs text-slate-400">WIND VECTOR</div>
            <div className="my-1.5 text-xl font-bold font-mono text-blue-200">
              {met.wind_speed_kmh} km/h
            </div>
            <div className="text-[11px] text-slate-400">{met.wind_direction_cardinal} ({met.wind_direction_deg}°)</div>
          </div>

          <div className="bg-slate-900/90 border border-slate-800 p-4 rounded-xl border-l-4 border-orange-500">
            <div className="text-xs text-slate-400">UPWIND SATELLITE FIRES</div>
            <div className="my-1.5 text-2xl font-black font-mono text-orange-400">
              {fires.total_active_fires} <span className="text-xs text-slate-400">fires</span>
            </div>
            <div className="text-[11px] text-orange-400 font-mono">Stubble Share: {snapshot.source_attribution.stubble_burning}%</div>
          </div>

        </section>

        {/* Overview Tab Content */}
        {activeTab === 'overview' && (
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            
            {/* Map (7 Cols) */}
            <div className="lg:col-span-7 bg-slate-900/80 border border-slate-800 p-5 rounded-2xl flex flex-col">
              <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-3">
                <h2 className="text-base font-bold text-white flex items-center gap-2">
                  <MapPin className="w-5 h-5 text-cyan-400" /> Delhi NCR Spatial Grid & Stubble Corridor
                </h2>
                <span className="text-xs font-mono text-slate-400">16 Real-time Monitoring Stations</span>
              </div>

              <div className="w-full aspect-[16/10] bg-[#070B11] rounded-xl border border-slate-800 p-4 relative overflow-hidden flex items-center justify-center">
                <svg viewBox="0 0 800 500" className="w-full h-full">
                  <path d="M 40 40 L 320 40 L 340 240 L 40 220 Z" fill="#111B2B" stroke="#1E2E48" strokeWidth="1.5" opacity="0.6"/>
                  <text x="70" y="70" fill="#64748B" fontSize="12" fontWeight="700" fontFamily="JetBrains Mono">PUNJAB & HARYANA UPWIND SECTOR</text>

                  <path d="M 380 180 C 420 160, 560 160, 600 200 C 630 240, 620 360, 580 420 C 520 450, 420 440, 370 380 C 340 320, 350 220, 380 180 Z" fill="#131C2E" stroke="#06B6D4" strokeWidth="2" strokeDasharray="4 4" opacity="0.8"/>
                  <text x="450" y="205" fill="#38BDF8" fontSize="13" fontWeight="800" fontFamily="JetBrains Mono">DELHI NCR BASIN</text>

                  {/* Stations */}
                  {snapshot.stations.map((s) => {
                    const x = 380 + ((s.lon - 76.8) / 0.7) * 200;
                    const y = 180 + ((29.0 - s.lat) / 0.7) * 220;
                    const isSel = s.station_id === selectedStationId;
                    return (
                      <g key={s.station_id} transform={`translate(${x}, ${y})`} onClick={() => setSelectedStationId(s.station_id)} className="cursor-pointer">
                        <circle r={isSel ? 16 : 11} fill={s.category_color} stroke="#FFFFFF" strokeWidth={isSel ? 2.5 : 1.5} opacity="0.95" />
                        <text x="0" y="3.5" textAnchor="middle" fill="#FFFFFF" fontSize={isSel ? 9 : 8} fontWeight="900" fontFamily="JetBrains Mono">{s.aqi}</text>
                        <text x="0" y={isSel ? -19 : -14} textAnchor="middle" fill="#E2E8F0" fontSize="9" fontWeight="700">{s.name.split(' ')[0]}</text>
                      </g>
                    );
                  })}
                </svg>
              </div>

              {/* Station Flyout */}
              <div className="mt-4 p-3 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between text-xs">
                <div>
                  <span className="font-bold text-cyan-400 font-mono">{currSt.station_id}</span> • <span className="font-bold text-white">{currSt.name}</span>
                  <div className="text-slate-400 mt-0.5">{currSt.region} • {currSt.city}</div>
                </div>
                <div className="flex items-center gap-4 font-mono">
                  <div>AQI: <b style={{ color: currSt.category_color }}>{currSt.aqi}</b></div>
                  <div>PM2.5: <b className="text-slate-200">{currSt.pm25}</b></div>
                  <div>Stubble: <b className="text-orange-400">{currSt.stubble_share_ugm3} μg/m³</b></div>
                </div>
              </div>
            </div>

            {/* Forecast & Attribution (5 Cols) */}
            <div className="lg:col-span-5 flex flex-col gap-6">
              
              {/* Forecast Card */}
              <div className="bg-slate-900/80 border border-slate-800 p-5 rounded-2xl flex flex-col">
                <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-3">
                  <h2 className="text-base font-bold text-white flex items-center gap-2">
                    <TrendingUp className="w-5 h-5 text-indigo-400" /> Coupled 72h Forecast
                  </h2>
                  <span className="text-xs font-mono text-cyan-400 bg-cyan-950 px-2 py-0.5 rounded border border-cyan-800">
                    Station: {selectedStationId}
                  </span>
                </div>

                {stationFc && (
                  <div className="grid grid-cols-3 gap-2 my-2">
                    <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 text-center">
                      <div className="text-[10px] text-slate-400 uppercase font-mono">+24h Lead</div>
                      <div className="text-2xl font-black font-mono my-1">{stationFc.milestones["+24h"].forecast_aqi}</div>
                      <div className="text-[10px] px-2 py-0.5 rounded-full font-semibold" style={{ color: stationFc.milestones["+24h"].category_color, backgroundColor: stationFc.milestones["+24h"].category_color + '33' }}>
                        {stationFc.milestones["+24h"].category}
                      </div>
                    </div>
                    <div className="p-3 rounded-xl bg-slate-950 border border-cyan-800 text-center ring-1 ring-cyan-500/30">
                      <div className="text-[10px] text-cyan-400 uppercase font-mono">+48h Lead ⚡</div>
                      <div className="text-2xl font-black font-mono text-cyan-300 my-1">{stationFc.milestones["+48h"].forecast_aqi}</div>
                      <div className="text-[10px] px-2 py-0.5 rounded-full font-semibold" style={{ color: stationFc.milestones["+48h"].category_color, backgroundColor: stationFc.milestones["+48h"].category_color + '33' }}>
                        {stationFc.milestones["+48h"].category}
                      </div>
                    </div>
                    <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 text-center">
                      <div className="text-[10px] text-purple-400 uppercase font-mono">+72h Lead</div>
                      <div className="text-2xl font-black font-mono my-1">{stationFc.milestones["+72h"].forecast_aqi}</div>
                      <div className="text-[10px] px-2 py-0.5 rounded-full font-semibold" style={{ color: stationFc.milestones["+72h"].category_color, backgroundColor: stationFc.milestones["+72h"].category_color + '33' }}>
                        {stationFc.milestones["+72h"].category}
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* Attribution Card */}
              <div className="bg-slate-900/80 border border-slate-800 p-5 rounded-2xl flex flex-col">
                <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-3">
                  <h2 className="text-base font-bold text-white flex items-center gap-2">
                    <PieChart className="w-5 h-5 text-orange-400" /> Source Apportionment
                  </h2>
                </div>

                <div className="flex flex-col gap-2">
                  {[
                    { name: "Stubble Burning", pct: snapshot.source_attribution.stubble_burning, color: "#F97316" },
                    { name: "Vehicular Exhaust", pct: snapshot.source_attribution.vehicular_emissions, color: "#EF4444" },
                    { name: "Road & Construction Dust", pct: snapshot.source_attribution.road_construction_dust, color: "#EAB308" },
                    { name: "Industrial Clusters", pct: snapshot.source_attribution.industrial_energy, color: "#8B5CF6" },
                    { name: "Secondary & Domestic", pct: snapshot.source_attribution.secondary_and_domestic, color: "#06B6D4" },
                  ].map(item => (
                    <div key={item.name} className="p-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs">
                      <div className="flex items-center justify-between mb-1">
                        <span className="font-semibold text-slate-200">{item.name}</span>
                        <span className="font-mono font-bold" style={{ color: item.color }}>{item.pct}%</span>
                      </div>
                      <div className="w-full bg-slate-900 h-1.5 rounded-full overflow-hidden">
                        <div className="h-full rounded-full" style={{ width: `${item.pct}%`, backgroundColor: item.color }} />
                      </div>
                    </div>
                  ))}
                </div>
              </div>

            </div>

          </div>
        )}

        {/* Predictive GRAP Tab */}
        {activeTab === 'grap' && grapData && (
          <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl">
            <div className="flex items-center justify-between pb-4 border-b border-slate-800 mb-4">
              <div>
                <span className="text-xs font-mono font-bold text-cyan-400 bg-cyan-950 px-2.5 py-0.5 rounded border border-cyan-800">THE CORE SIH INNOVATION</span>
                <h2 className="text-xl font-bold text-white mt-1">Predictive Graded Response Action Plan Engine</h2>
                <p className="text-xs text-slate-400 mt-0.5">Forecast-triggered interventions giving 24-72 hours of pre-emptive lead time.</p>
              </div>
              <div className="text-right font-mono">
                <div className="text-xs text-slate-400">MAX LEAD TIME GAINED</div>
                <div className="text-2xl font-black text-cyan-400">{grapData.max_lead_time_gained_hours} Hours</div>
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-950 text-slate-400 font-mono text-[11px]">
                  <tr>
                    <th className="p-3">Stage & Severity</th>
                    <th className="p-3">Target Sector</th>
                    <th className="p-3">Forecast Lead Time</th>
                    <th className="p-3">Triggered Action</th>
                    <th className="p-3">Responsible Agency</th>
                    <th className="p-3">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800">
                  {grapData.rules.map(r => (
                    <tr key={r.id} className={`hover:bg-slate-800/40 ${r.is_triggered ? 'bg-cyan-950/20' : ''}`}>
                      <td className="p-3">
                        <div className="font-bold text-slate-200">{r.stage}</div>
                        <div className="text-[10px] text-slate-400 font-mono">AQI {r.aqi_min}-{r.aqi_max}</div>
                      </td>
                      <td className="p-3 text-slate-300">{r.target_sector}</td>
                      <td className="p-3 font-mono font-bold text-cyan-400">+{r.forecast_lead_time_hours} Hours Lead</td>
                      <td className="p-3 text-slate-300 max-w-md">{r.triggered_action}</td>
                      <td className="p-3 font-semibold text-slate-300">{r.responsible_agency}</td>
                      <td className="p-3">
                        <span className={`px-2.5 py-1 rounded-full text-[10px] font-bold font-mono ${r.status_type === 'PRE_EMPTIVE' ? 'bg-cyan-950 text-cyan-400 border border-cyan-800' : (r.status_type === 'ACTIVE' ? 'bg-rose-950 text-rose-400' : 'bg-slate-800 text-slate-400')}`}>
                          {r.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

      </main>
    </div>
  );
}
