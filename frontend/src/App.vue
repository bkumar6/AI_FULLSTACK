<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useAuth } from './composables/useAuth';

const { isAuthenticated, userEmail, logout } = useAuth();
</script>

<template>
    <header class="header">
        <div class="wrapper">
            <nav class="nav">
                <div class="left-links">
                    <RouterLink to="/">Home</RouterLink>
                    <RouterLink to="/chat">Chatbot</RouterLink>
                </div>

                <div class="right-links">
                    <template v-if="!isAuthenticated">
                        <RouterLink to="/signup">Sign Up</RouterLink>
                        <RouterLink to="/login">Log In</RouterLink>
                    </template>

                    <template v-else>
                        <RouterLink to="/users">Users List</RouterLink>
                        <span class="auth-status">
                            <span class="email">{{ userEmail }}</span>
                            <a href="#" @click.prevent="logout" class="logout-link">Logout</a>
                        </span>
                    </template>
                </div>
            </nav>
        </div>
    </header>

    <main class="content">
        <RouterView />
    </main>
</template>

<style>
/* GLOBAL */
body {
    margin: 0;
    padding: 0;
    font-family: "Inter", Arial, sans-serif;
    background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
    color: #333;
}

/* HEADER */
.header {
    width: 100%;
    background: linear-gradient(90deg, #7f5af0, #2cb67d, #3a86ff);
    padding: 18px 0;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    position: fixed;
    top: 0;
    left: 0;
    z-index: 1000;
}

/* CENTER WRAPPER */
.wrapper {
    max-width: 1300px;
    margin: 0 auto;
    padding: 0 25px;
}

/* NAV LAYOUT */
.nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.left-links,
.right-links {
    display: flex;
    gap: 20px;
    align-items: center;
}

/* LINK STYLING */
nav a {
    color: #fff;
    text-decoration: none;
    font-weight: 600;
    padding: 10px 18px;
    border-radius: 12px;
    transition: 0.25s ease;
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(6px);
}

nav a:hover {
    transform: translateY(-2px);
    background: rgba(255, 255, 255, 0.30);
}

nav a.router-link-exact-active {
    background: #fff;
    color: #1f2937;
    box-shadow: 0 4px 10px rgba(255, 255, 255, 0.35);
}

/* AUTH STATUS */
.auth-status {
    display: flex;
    align-items: center;
    gap: 10px;
    background: rgba(255, 255, 255, 0.25);
    padding: 8px 12px;
    border-radius: 10px;
    backdrop-filter: blur(6px);
}

.email {
    color: #f2f2f2;
    font-size: 0.95em;
}

.logout-link {
    color: #ff4d6d;
    cursor: pointer;
    font-weight: 700;
    text-decoration: underline;
}

.logout-link:hover {
    color: #ffb3c1;
}

/* MAIN CONTENT */
.content {
    max-width: 1100px;
    margin: 0 auto;
    padding: 130px 20px 35px;
}
</style>
