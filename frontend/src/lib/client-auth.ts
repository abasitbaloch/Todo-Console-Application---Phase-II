import { User, UserLogin, UserCreate, AuthResponse } from './types';

// Use 127.0.0.1 to avoid IPv6 issues on Windows
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

class AuthService {
    private tokenKey = 'access_token';

    getToken(): string | null {
        if (typeof window === 'undefined') return null;
        return localStorage.getItem(this.tokenKey);
    }

    // --- NEW: Added isAuthenticated method to fix the TypeError ---
    isAuthenticated(): boolean {
        const token = this.getToken();
        // Returns true if token exists and is not empty
        return !!token;
    }

    setToken(token: string) {
        if (typeof window === 'undefined') return;
        localStorage.setItem(this.tokenKey, token);
    }

    logout() {
        if (typeof window === 'undefined') return;
        localStorage.removeItem(this.tokenKey);
        window.location.href = '/';
    }

    // --- REGISTER ---
    async register(data: UserCreate): Promise<AuthResponse> {
        const response = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || 'Registration failed');
        }

        const result = await response.json();
        this.setToken(result.access_token);
        return result;
    }

    // --- LOGIN ---
    async login(data: UserLogin): Promise<AuthResponse> {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email: data.email,
                password: data.password
            }),
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || 'Login failed');
        }

        const result = await response.json();
        this.setToken(result.access_token);
        return result;
    }

    // --- GET CURRENT USER ---
    async getCurrentUser(): Promise<User | null> {
        const token = this.getToken();
        if (!token) return null;

        try {
            const response = await fetch(`${API_URL}/auth/me`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!response.ok) {
                if (response.status === 401) this.logout();
                return null;
            }
            return await response.json();
        } catch (error) {
            console.error("Auth check failed:", error);
            return null;
        }
    }
}

export const authService = new AuthService();