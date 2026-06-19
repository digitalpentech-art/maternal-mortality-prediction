const API_BASE = '/api';

export async function fetchMetrics() {
    const response = await fetch(`${API_BASE}/metrics`);
    return await response.json();
}

export async function postPrediction(data) {
    const response = await fetch(`${API_BASE}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    return await response.json();
}
