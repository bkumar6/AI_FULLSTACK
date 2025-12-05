import { ref, computed } from 'vue';

// State stored globally, initialized from local storage
const token = ref(localStorage.getItem('access_token') || null);
const userId = ref(localStorage.getItem('user_id') || null);
const userEmail = ref(localStorage.getItem('user_email') || null);

// Base URL for the FastAPI backend
const API_BASE_URL = 'http://127.0.0.1:8000';

export function useAuth() {
    
    // Computed property to check login status easily
    const isAuthenticated = computed(() => !!token.value);

    // --- Core Authentication Actions ---

    const login = async (email, password) => {
        const url = `${API_BASE_URL}/auth/login`;
        
        // FastAPI's login endpoint expects form data, not JSON
        const formData = new URLSearchParams();
        formData.append('username', email); // FastAPI uses 'username' for email
        formData.append('password', password);

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded' // CRITICAL header change
                },
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Login failed due to server error.');
            }

            const data = await response.json();
            
            // Store token and user info globally and locally
            token.value = data.access_token;
            userId.value = data.user_id;
            userEmail.value = data.email;

            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('user_id', data.user_id);
            localStorage.setItem('user_email', data.email);

            return true; // Login successful

        } catch (error) {
            console.error("Login Error:", error);
            throw error;
        }
    };

    const logout = () => {
        token.value = null;
        userId.value = null;
        userEmail.value = null;
        localStorage.removeItem('access_token');
        localStorage.removeItem('user_id');
        localStorage.removeItem('user_email');
    };
    
    // --- Data Fetching Helper (For Protected Routes) ---
    
    const fetchProtected = async (endpoint, method = 'GET', body = null) => {
        const url = `${API_BASE_URL}${endpoint}`;
        
        if (!isAuthenticated.value) {
            throw new Error("User not authenticated.");
        }
        
        const headers = {
            'Authorization': `Bearer ${token.value}`, // Pass JWT in the Authorization header
            'Content-Type': 'application/json'
        };

        try {
            const response = await fetch(url, {
                method,
                headers,
                body: body ? JSON.stringify(body) : null
            });

            if (response.status === 401 || response.status === 403) {
                logout(); // Automatically log out on token expiry/invalidity
                throw new Error("Session expired or invalid. Please log in again.");
            }

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `Server error: ${response.status}`);
            }
            
            // Handle 204 No Content for DELETE requests
            if (response.status === 204) return null;

            return await response.json();

        } catch (error) {
            console.error("Protected Fetch Error:", error);
            throw error;
        }
    };


    return {
        token,
        userId,
        userEmail,
        isAuthenticated,
        login,
        logout,
        fetchProtected
    };
}