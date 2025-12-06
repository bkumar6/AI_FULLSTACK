import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ChatView from '../views/ChatView.vue'
import SignupView from '../views/SignupView.vue'
import LoginView from '../views/LoginView.vue'
import UsersListView from '../views/UsersListView.vue'
import { useAuth } from '../composables/useAuth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/chat',
      name: 'chat',
      component: ChatView
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/users',
      name: 'users',
      component: UsersListView,
      meta: { requiresAuth: true } // Add meta field to protect the route
    }
  ]
})

// --- Navigation Guard Implementation ---
router.beforeEach((to, from, next) => {
    const { isAuthenticated } = useAuth();
    
    // Check if the route requires authentication and the user is not authenticated
    if (to.meta.requiresAuth && !isAuthenticated.value) {
        // Redirect to login page
        next('/login');
    } else if ((to.name === 'login' || to.name === 'signup') && isAuthenticated.value) {
        // Prevent logged-in users from seeing login/signup pages
        next('/users'); 
    } else {
        next();
    }
})

export default router