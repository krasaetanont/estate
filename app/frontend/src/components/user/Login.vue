<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <h2>Welcome Back</h2>
        <p>Login to manage your properties and favorites</p>
      </div>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="email" class="form-label">Email Address</label>
          <input 
            id="email" 
            v-model="email" 
            type="email" 
            class="form-input" 
            placeholder="name@example.com" 
            required 
          />
        </div>

        <div class="form-group">
          <label for="password" class="form-label">Password</label>
          <input 
            id="password" 
            v-model="password" 
            type="password" 
            class="form-input" 
            placeholder="••••••••" 
            required 
          />
        </div>

        <div class="form-actions">
          <button type="submit" class="btn btn-primary btn-full" :disabled="isLoading">
            <span v-if="isLoading" class="spinner-small"></span>
            {{ isLoading ? 'Logging in...' : 'Sign In' }}
          </button>
        </div>
      </form>

      <div class="divider">
        <span>or continue with</span>
      </div>

      <div class="social-login">
        <button @click="handleGoogleLogin" class="btn btn-outline btn-full google-btn">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 48 48">
            <path fill="#FFC107" d="M43.611 20.083H42V20H24v8h11.303c-1.649 4.657-6.08 8-11.303 8c-6.627 0-12-5.373-12-12s5.373-12 12-12c3.059 0 5.842 1.154 7.961 3.039l5.657-5.657C34.046 6.053 29.268 4 24 4C12.955 4 4 12.955 4 24s8.955 20 20 20s20-8.955 20-20c0-1.341-.138-2.65-.389-3.917z"/>
            <path fill="#FF3D00" d="m6.306 14.691l6.571 4.819C14.655 15.108 18.961 12 24 12c3.059 0 5.842 1.154 7.961 3.039l5.657-5.657C34.046 6.053 29.268 4 24 4C16.318 4 9.656 8.337 6.306 14.691z"/>
            <path fill="#4CAF50" d="M24 44c5.166 0 9.86-1.977 13.409-5.192l-6.19-5.238A11.91 11.91 0 0 1 24 36c-5.202 0-9.619-3.317-11.283-7.946l-6.522 5.025C9.505 39.556 16.227 44 24 44z"/>
            <path fill="#1976D2" d="M43.611 20.083H42V20H24v8h11.303a12.04 12.04 0 0 1-4.087 5.571l.003-.002l6.19 5.238C36.971 39.205 44 34 44 24c0-1.341-.138-2.65-.389-3.917z"/>
          </svg>
          Sign in with Google
        </button>
      </div>

      <div class="login-footer">
        <p>Don't have an account? <RouterLink to="/register">Register here</RouterLink></p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth.js'

const router = useRouter()
const email = ref('')
const password = ref('')
const isLoading = ref(false)
// In src/components/user/Login.vue
const emit = defineEmits(['login-success'])
const auth = useAuthStore()
const handleLogin = async () => {
  isLoading.value = true
  try {
    await auth.login(email.value, password.value)
    emit('login-success') // Tell the view we are done!
  } catch (error) {
    console.error('Login failed', error)
  } finally {
    isLoading.value = false
  }
}


const handleGoogleLogin = () => {
  // Replace this with your Google OAuth logic
  // Typically redirects to: window.location.href = 'your-backend-api/auth/google'
  console.log('Initiating Google Login...')
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: var(--spacing-2xl) var(--spacing-md);
  min-height: calc(100vh - 200px); /* Adjust based on header/footer height */
  background-color: var(--color-gray-50);
}

.login-card {
  background-color: var(--color-white);
  padding: var(--spacing-2xl);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg);
  max-width: 400px;
  width: 100%;
}

.login-header {
  text-align: center;
  margin-bottom: var(--spacing-xl);
}

.login-header h2 {
  font-size: var(--font-size-2xl);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-xs);
}

.login-header p {
  color: var(--color-text-secondary);
  font-size: var(--font-size-sm);
}

.divider {
  display: flex;
  align-items: center;
  text-align: center;
  margin: var(--spacing-xl) 0;
  color: var(--color-text-disabled);
  font-size: var(--font-size-xs);
  text-transform: uppercase;
  letter-spacing: 1px;
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  border-bottom: 1px solid var(--color-border);
}

.divider span {
  padding: 0 var(--spacing-md);
}

.google-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  background-color: var(--color-white);
  border: 1px solid var(--color-border);
  transition: all var(--transition-base);
}

.google-btn:hover {
  background-color: var(--color-gray-50);
  border-color: var(--color-primary);
}

.login-footer {
  margin-top: var(--spacing-xl);
  text-align: center;
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}

.login-footer a {
  color: var(--color-primary-dark);
  font-weight: var(--font-weight-semibold);
  text-decoration: none;
}

.login-footer a:hover {
  text-decoration: underline;
}
</style>