const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function fetchStations() {
  const res = await fetch(`${BASE_URL}/api/stations`);
  return res.json();
}

export async function fetchSnapshot(stepHour = 72) {
  const res = await fetch(`${BASE_URL}/api/snapshot?step_hour=${stepHour}`);
  return res.json();
}

export async function fetchStationForecast(stationId, stepHour = 72) {
  const res = await fetch(`${BASE_URL}/api/forecast/station/${stationId}?step_hour=${stepHour}`);
  return res.json();
}

export async function fetchRegionalForecast(stepHour = 72) {
  const res = await fetch(`${BASE_URL}/api/forecast/regional?step_hour=${stepHour}`);
  return res.json();
}

export async function fetchGrapTriggers(stepHour = 72) {
  const res = await fetch(`${BASE_URL}/api/grap/triggers?step_hour=${stepHour}`);
  return res.json();
}

export async function fetchDispatches(stepHour = 72) {
  const res = await fetch(`${BASE_URL}/api/dispatches?step_hour=${stepHour}`);
  return res.json();
}

export async function fetchInterstateGrid(stepHour = 72) {
  const res = await fetch(`${BASE_URL}/api/interstate?step_hour=${stepHour}`);
  return res.json();
}

export async function runWhatIfSimulation(params) {
  const res = await fetch(`${BASE_URL}/api/what-if`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(params)
  });
  return res.json();
}
