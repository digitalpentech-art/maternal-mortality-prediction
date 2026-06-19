import { postPrediction } from './api.js';

export function initPredictionForm() {
    const form = document.getElementById('predictionForm');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData.entries());
            const result = await postPrediction(data);
            if (result.status === 'success') {
                renderPrediction(result);
            } else {
                alert("Error: " + (result.error || "Unknown"));
            }
        });
    }
}

function renderPrediction(res) {
    document.getElementById('predictionPlaceholder').classList.add('d-none');
    document.getElementById('predictionResult').classList.remove('d-none');
    // ... logic for rendering gauges and plots ...
}
