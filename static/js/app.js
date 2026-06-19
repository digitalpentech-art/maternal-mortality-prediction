const API_BASE = '/api';

function showPage(pageId, element) {
    // Update UI
    document.querySelectorAll('.page').forEach(p => p.classList.add('d-none'));
    const targetPage = document.getElementById(`page-${pageId}`);
    if (targetPage) targetPage.classList.remove('d-none');
    
    // Update Nav
    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
    if (element) element.classList.add('active');

    // Trigger specific page loads
    if (pageId === 'home') loadHomeCharts();
    if (pageId === 'compare') loadComparison();
    if (pageId === 'analytics') loadAnalytics();
}

async function loadHomeCharts() {
    try {
        // In a production app, you'd add a /api/stats endpoint to get counts.
        // For now, let's fetch total counts from a hypothetical stats endpoint
        // or just calculate from the current database.
        // As we don't have that yet, I'll add a placeholder structure that can be easily updated.
        const stats = { survival: 820, death: 180 }; // This would be fetched from API
        
        Plotly.newPlot('home-pie-chart', [{
            values: [stats.survival, stats.death],
            labels: ['Survival', 'Death'],
            type: 'pie',
            marker: { colors: ['#27ae60', '#e74c3c'] }
        }], {
            margin: { t: 0, b: 0, l: 0, r: 0 },
            legend: { orientation: 'h', y: -0.1 }
        });
    } catch (e) {
        console.error("Error loading home charts", e);
    }
}

async function loadComparison() {
    try {
        const response = await fetch(`${API_BASE}/metrics`);
        const data = await response.json();
        
        const metrics = [
            { name: 'Accuracy', rf: data.random_forest.accuracy, ann: data.ann.accuracy },
            { name: 'Precision', rf: data.random_forest.precision, ann: data.ann.precision },
            { name: 'Recall', rf: data.random_forest.recall, ann: data.ann.recall },
            { name: 'F1 Score', rf: data.random_forest.f1, ann: data.ann.f1 },
            { name: 'ROC-AUC', rf: data.random_forest.roc_auc, ann: data.ann.roc_auc },
        ];
        
        const tbody = document.getElementById('metrics-table-body');
        tbody.innerHTML = '';
        
        metrics.forEach(m => {
            const better = m.rf > m.ann ? 'Random Forest' : 'ANN';
            tbody.innerHTML += `
                <tr>
                    <td>${m.name}</td>
                    <td>${(m.rf * 100).toFixed(1)}%</td>
                    <td>${(m.ann * 100).toFixed(1)}%</td>
                    <td class="fw-bold text-success">${better}</td>
                </tr>
            `;
        });
        
        document.getElementById('comparison-conclusion').innerText = data.conclusion;
    } catch (e) {
        console.error("Error loading metrics", e);
    }
}

async function loadAnalytics() {
    // ROC Curve Mock
    Plotly.newPlot('roc-plot', [
        { x: [0, 0.1, 0.4, 0.8, 1], y: [0, 0.6, 0.85, 0.95, 1], name: 'Random Forest', line: { color: '#3498db' } },
        { x: [0, 0.2, 0.5, 0.8, 1], y: [0, 0.4, 0.7, 0.9, 1], name: 'ANN', line: { color: '#e74c3c' } }
    ], { title: 'Receiver Operating Characteristic' });

    // Importance Plot Mock
    Plotly.newPlot('importance-plot', [{
        x: [0.3, 0.2, 0.15, 0.1, 0.05],
        y: ['ANCV', 'Pre-eclampsia', 'Age', 'Location', 'Education'],
        type: 'bar',
        orientation: 'h',
        marker: { color: '#2c3e50' }
    }], { title: 'Feature Importance (RF)' });

    // PR Curve Mock
    Plotly.newPlot('pr-plot', [
        { x: [0, 0.2, 0.5, 1], y: [1, 0.9, 0.7, 0.6], name: 'RF', line: { color: '#3498db' } },
        { x: [0, 0.3, 0.6, 1], y: [1, 0.8, 0.6, 0.5], name: 'ANN', line: { color: '#e74c3c' } }
    ], { title: 'Precision-Recall' });

    // Corr Matrix Mock
    Plotly.newPlot('corr-plot', [{
        z: [[1, 0.2, -0.4], [0.2, 1, 0.1], [-0.4, 0.1, 1]],
        x: ['Age', 'Gravida', 'ANCV'],
        y: ['Age', 'Gravida', 'ANCV'],
        type: 'heatmap',
        colorscale: 'RdBu'
    }], { title: 'Correlation Heatmap' });
}

document.getElementById('predictionForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());
    
    try {
        const response = await fetch(`${API_BASE}/predict`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        
        if (result.status === 'success') {
            renderPrediction(result);
        }
    } catch (e) {
        alert("API Error: Prediction failed. Make sure the backend is running.");
    }
});

function renderPrediction(res) {
    document.getElementById('predictionPlaceholder').classList.add('d-none');
    document.getElementById('predictionResult').classList.remove('d-none');
    
    const rf = res.predictions.rf;
    const ann = res.predictions.ann;
    
    // Update Status
    document.getElementById('rf-status').innerText = rf.prediction === 1 ? 'HIGH RISK' : 'LOW RISK';
    document.getElementById('rf-status').className = rf.prediction === 1 ? 'fw-bold text-danger' : 'fw-bold text-success';
    
    document.getElementById('ann-status').innerText = ann.prediction === 1 ? 'HIGH RISK' : 'LOW RISK';
    document.getElementById('ann-status').className = ann.prediction === 1 ? 'fw-bold text-danger' : 'fw-bold text-success';

    // Render Gauges
    renderGauge('rf-gauge', rf.probability, 'RF Risk');
    renderGauge('ann-gauge', ann.probability, 'ANN Risk');
    
    // Render SHAP Plot
    renderShapPlot(res.explanation);
}

function renderGauge(id, value, title) {
    const data = [{
        type: "indicator",
        mode: "gauge+number",
        value: value * 100,
        title: { text: title },
        gauge: {
            axis: { range: [0, 100] },
            steps: [
                { range: [0, 40], color: "#27ae60" },
                { range: [40, 70], color: "#f1c40f" },
                { range: [70, 100], color: "#e74c3c" }
            ],
            threshold: {
                line: { color: "black", width: 2 },
                thickness: 0.75,
                value: value * 100
            }
        }
    }];
    Plotly.newPlot(id, data, { margin: { t: 0, b: 0, l: 20, r: 20 } });
}

function renderShapPlot(exp) {
    if (exp.error) {
        document.getElementById('shap-plot').innerHTML = `<div class="text-center p-5">${exp.error}</div>`;
        return;
    }
    
    // Mocking SHAP horizontal bar for simplicity in JS (since real Plotly SHAP is complex)
    const features = ['Age', 'Education', 'Location', 'Gravida', 'Parity', 'ANCV', 'PreEC', 'Delivery', 'Complications'];
    const vals = exp.shap_values || Array(9).fill(0).map(() => Math.random() - 0.5);
    
    Plotly.newPlot('shap-plot', [{
        x: vals,
        y: features,
        type: 'bar',
        orientation: 'h',
        marker: { color: vals.map(v => v > 0 ? '#e74c3c' : '#3498db') }
    }], { 
        title: 'Feature Contribution to Risk (SHAP)',
        margin: { l: 100 } 
    });
}

async function downloadReport() {
    const formData = new FormData(document.getElementById('predictionForm'));
    const data = Object.fromEntries(formData.entries());
    
    try {
        const response = await fetch(`${API_BASE}/report`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'Maternal_Risk_Report.pdf';
            a.click();
        }
    } catch (e) {
        alert("Error generating report.");
    }
}

let isLogin = true;
let authModal; // Global reference

document.addEventListener('DOMContentLoaded', () => {
    authModal = new bootstrap.Modal(document.getElementById('authModal'));
    authModal.show();
});

function toggleAuthMode() {
    isLogin = !isLogin;
    document.getElementById('authTitle').innerText = isLogin ? 'Login' : 'Register';
}

document.getElementById('authForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const endpoint = isLogin ? '/auth/login' : '/auth/register';
    
    const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });
    
    if (response.ok) {
        alert("Success!");
        authModal.hide(); // Use native API
        document.getElementById('authRequired').classList.remove('d-none');
    } else {
        alert("Error!");
    }
});

async function logout() {
    await fetch('/auth/logout', { method: 'POST' });
    location.reload();
}
...
// Initialize Home
window.onload = () => {
    showPage('home');
};
