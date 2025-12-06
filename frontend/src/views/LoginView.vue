<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuth } from '../composables/useAuth';

const email = ref('');
const password = ref('');
const message = ref('');
const isError = ref(false);
const isLoading = ref(false);

const router = useRouter();
const { login } = useAuth(); // Destructure the login function from the store

const submitLogin = async () => {
    message.value = '';
    isError.value = false;
    isLoading.value = true;

    if (!email.value || !password.value) {
        message.value = 'Email and password are required.';
        isError.value = true;
        isLoading.value = false;
        return;
    }

    try {
        await login(email.value, password.value); // Call the store's login function
        
        message.value = 'Login successful! Redirecting...';
        isError.value = false;
        
        // Redirect to protected users page on success
        setTimeout(() => {
            router.push('/users');
        }, 500);

    } catch (error) {
        // The useAuth function throws an error if login or fetch fails
        message.value = error.message || 'Login failed.';
        isError.value = true;
    } finally {
        isLoading.value = false;
    }
};
</script>

<template>
    <div class="auth-container">
        <h1>🔑Log In</h1>
        
        <form @submit.prevent="submitLogin" class="auth-form">
            <input v-model="email" type="email" placeholder="Email" required :disabled="isLoading" />
            <input v-model="password" type="password" placeholder="Password" required :disabled="isLoading" />
            
            <button type="submit" :disabled="isLoading">
                {{ isLoading ? 'Logging In...' : 'Log In' }}
            </button>
        </form>

        <div v-if="message" :class="['message-box', { 'error': isError, 'success': !isError }]">
            {{ message }}
        </div>
        <p class="auth-link">
            Need an account? <router-link to="/signup">Sign Up</router-link>
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