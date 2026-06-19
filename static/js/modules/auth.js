let authModal;

export function initAuth() {
    const modalEl = document.getElementById('authModal');
    if (modalEl) {
        authModal = new bootstrap.Modal(modalEl);
        authModal.show();
    }
}

export function toggleAuthMode(isLogin) {
    const title = document.getElementById('authTitle');
    title.innerText = isLogin ? 'Login' : 'Register';
    return !isLogin;
}

export async function loginUser(username, password, isLogin) {
    const endpoint = isLogin ? '/auth/login' : '/auth/register';
    const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });
    
    if (response.ok) {
        authModal.hide();
        document.getElementById('authRequired').classList.remove('d-none');
    }
    return response.ok;
}
