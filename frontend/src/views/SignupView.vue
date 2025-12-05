<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

// Base URL for the FastAPI backend
const API_BASE_URL = 'http://127.0.0.1:8000';

const name = ref('');
const email = ref('');
const password = ref('');
const message = ref('');
const isError = ref(false);
const isLoading = ref(false);

const router = useRouter();

const submitSignup = async () => {
    message.value = '';
    isError.value = false;
    isLoading.value = true;

    if (!name.value || !email.value || !password.value) {
        message.value = 'All fields are required.';
        isError.value = true;
        isLoading.value = false;
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/auth/signup`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: name.value,
                email: email.value,
                password: password.value
            })
        });

        const data = await response.json();

        if (!response.ok) {
            message.value = data.detail || 'Signup failed.';
            isError.value = true;
        } else {
            message.value = `Success! User ${data.email} created. Redirecting to login...`;
            isError.value = false;
            // Clear fields on success
            name.value = '';
            email.value = '';
            password.value = '';
            
            // Redirect to login after a brief delay
            setTimeout(() => {
                router.push('/login');
            }, 1500);
        }
    } catch (error) {
        message.value = `Network Error: ${error.message}`;
        isError.value = true;
    } finally {
        isLoading.value = false;
    }
};
</script>

<template>
    <div class="auth-container">
        <h1>👤Sign Up</h1>
        
        <form @submit.prevent="submitSignup" class="auth-form">
            <input v-model="name" type="text" placeholder="Full Name" required :disabled="isLoading" />
            <input v-model="email" type="email" placeholder="Email" required :disabled="isLoading" />
            <input v-model="password" type="password" placeholder="Password" required :disabled="isLoading" />
            
            <button type="submit" :disabled="isLoading">
                {{ isLoading ? 'Registering...' : 'Sign Up' }}
            </button>
        </form>

        <div v-if="message" :class="['message-box', { 'error': isError, 'success': !isError }]">
            {{ message }}
        </div>
        <p class="auth-link">
            Already have an account? <router-link to="/login">Log In</router-link>
        </p>
    </div>
</template>

<style scoped>
.auth-container {
    max-width: 400px;
    margin: 60px auto;
    padding: 30px;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    background-color: #f9f9f9;
    text-align: center;
}

.auth-form {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

input {
    padding: 12px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 16px;
}

button {
    padding: 12px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.2s;
}

button:hover:not(:disabled) {
    background-color: #0056b3;
}

button:disabled {
    background-color: #99cfff;
    cursor: not-allowed;
}

.message-box {
    padding: 10px;
    margin-top: 20px;
    border-radius: 4px;
    font-weight: bold;
}

.error {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
}

.success {
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
}
.auth-link {
    margin-top: 20px;
}
</style>