import { initAuth, toggleAuthMode, loginUser } from './modules/auth.js';
import { initPredictionForm } from './modules/predict.js';
import { showPage } from './modules/ui.js';

document.addEventListener('DOMContentLoaded', () => {
    initAuth();
    initPredictionForm();
    showPage('home');
});

// Expose globally for onclick attributes
window.showPage = showPage;
window.toggleAuthMode = () => { /* ... call imported toggleAuthMode ... */ };
window.loginUser = loginUser;
