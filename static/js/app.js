console.log("app.js loaded");

const API_BASE = '/api';

function showPage(pageId, element) {
    console.log(`Navigating to: ${pageId}`);
    try {
        document.querySelectorAll('.page').forEach(p => p.classList.add('d-none'));
        const targetPage = document.getElementById(`page-${pageId}`);
        if (targetPage) targetPage.classList.remove('d-none');
        
        document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
        if (element) element.classList.add('active');

        if (pageId === 'home') loadHomeCharts();
        if (pageId === 'compare') loadComparison();
        if (pageId === 'analytics') loadAnalytics();
    } catch (e) {
        console.error("Error in showPage:", e);
    }
}

async function loadHomeCharts() {
    console.log("Loading charts...");
    const stats = { survival: 820, death: 180 };
    Plotly.newPlot('home-pie-chart', [{
        values: [stats.survival, stats.death],
        labels: ['Survival', 'Death'],
        type: 'pie',
        marker: { colors: ['#27ae60', '#e74c3c'] }
    }], { margin: { t: 0, b: 0, l: 0, r: 0 } });
}

async function loadComparison() {
    console.log("Loading metrics...");
    try {
        const response = await fetch(`${API_BASE}/metrics`);
        const data = await response.json();
        const tbody = document.getElementById('metrics-table-body');
        tbody.innerHTML = '';
        // ... (rest of the comparison rendering)
    } catch (e) {
        console.error("Error loading metrics", e);
    }
}

// Prediction Form
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('predictionForm');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            console.log("Predicting...");
            // ... (rest of prediction logic)
        });
    }
});

// Authentication
let isLogin = true;
let authModal;

document.addEventListener('DOMContentLoaded', () => {
    console.log("Auth initialized");
    const modalEl = document.getElementById('authModal');
    if (modalEl) {
        authModal = new bootstrap.Modal(modalEl);
        authModal.show();
    }
});

function toggleAuthMode() {
    isLogin = !isLogin;
    document.getElementById('authTitle').innerText = isLogin ? 'Login' : 'Register';
}

document.getElementById('authForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    console.log("Submitting Auth form");
});

async function logout() {
    await fetch('/auth/logout', { method: 'POST' });
    location.reload();
}
