/**
 * Spice Market - API Client Module
 * Communicates with Django REST backend (/api/...)
 */
const API_BASE = (window.location.port === '8000')
    ? ''
    : 'http://127.0.0.1:8000';

const API = {
    // --- Products ---
    async getProducts(params = {}) {
        const query = new URLSearchParams();
        if (params.category) query.append('category', params.category);
        if (params.search) query.append('search', params.search);

        try {
            const res = await fetch(`${API_BASE}/api/products/?${query.toString()}`);
            if (!res.ok) throw new Error(`HTTP error ${res.status}`);
            return await res.json();
        } catch (err) {
            console.warn("Could not fetch products from backend API, using local fallback.", err);
            return null;
        }
    },

    async getProduct(id) {
        try {
            const res = await fetch(`${API_BASE}/api/products/${id}/`);
            if (!res.ok) throw new Error(`HTTP error ${res.status}`);
            return await res.json();
        } catch (err) {
            console.warn("Could not fetch product detail:", err);
            return null;
        }
    },

    // --- Authentication ---
    async register(name, email, password, phone = '') {
        const res = await fetch(`${API_BASE}/api/auth/register/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ name, email, password, phone })
        });
        const data = await res.json();
        if (!res.ok) {
            const msg = typeof data === 'object' ? Object.values(data).flat().join(' ') : 'Registration failed.';
            throw new Error(msg);
        }
        if (data.user) {
            localStorage.setItem('spice_user', JSON.stringify(data.user));
        }
        return data;
    },

    async login(usernameOrEmail, password) {
        const res = await fetch(`${API_BASE}/api/auth/login/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ username_or_email: usernameOrEmail, password })
        });
        const data = await res.json();
        if (!res.ok) {
            const msg = typeof data === 'object' ? Object.values(data).flat().join(' ') : 'Login failed.';
            throw new Error(msg);
        }
        if (data.user) {
            localStorage.setItem('spice_user', JSON.stringify(data.user));
        }
        return data;
    },

    async logout() {
        try {
            await fetch(`${API_BASE}/api/auth/logout/`, {
                method: 'POST',
                credentials: 'include'
            });
        } catch (e) { }
        localStorage.removeItem('spice_user');
    },

    getCurrentUser() {
        const stored = localStorage.getItem('spice_user');
        return stored ? JSON.parse(stored) : null;
    },

    isLoggedIn() {
        return !!this.getCurrentUser();
    },

    // --- Orders & Checkout ---
    async placeOrder(orderData) {
        const res = await fetch(`${API_BASE}/api/orders/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify(orderData)
        });
        let data;
        try {
            data = await res.json();
        } catch (e) {
            data = {};
        }
        if (!res.ok) {
            const errorMsg = data.error || data.detail || (typeof data === 'object' && Object.keys(data).length > 0 ? Object.values(data).flat().join(' ') : `Order request failed (${res.status})`);
            throw new Error(errorMsg);
        }
        return data;
    },

    // --- Contact Messages ---
    async sendContact(name, email, message) {
        const res = await fetch(`${API_BASE}/api/contact/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, message })
        });
        const data = await res.json();
        if (!res.ok) {
            const msg = typeof data === 'object' ? Object.values(data).flat().join(' ') : 'Failed to send message.';
            throw new Error(msg);
        }
        return data;
    },

    // --- Health Check ---
    async checkHealth() {
        try {
            const res = await fetch(`${API_BASE}/api/health/`);
            return await res.json();
        } catch (e) {
            return { status: 'offline', error: e.message };
        }
    }
};

window.SpiceAPI = API;
