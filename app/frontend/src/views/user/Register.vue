<template>
  <main class="register-view">
    <div class="container">
      <Register @register-success="onRegisterSuccess" />
    </div>
  </main>
</template>

<script setup lang="ts">
import Register from '../../components/user/Register.vue'
import { useRouter } from 'vue-router'

const router = useRouter()

/**
 * Logic to execute after a successful registration.
 * Usually, you'd redirect to the login page or 
 * automatically log them in and go to the home page.
 */
const onRegisterSuccess = () => {
  // Option A: Send them to login with a success message
  router.push({ name: 'login', query: { registered: 'true' } })
  
  // Option B: Redirect to Home if they are auto-logged in
  // router.push({ name: 'home' })
}
</script>

<style scoped>
.register-view {
  display: flex;
  align-items: center;
  justify-content: center;
  /* Ensures the card is centered even on tall screens */
  min-height: calc(100vh - 80px); 
  background-color: var(--color-background-soft);
  padding: var(--spacing-lg) var(--spacing-md);
}

.container {
  width: 100%;
  display: flex;
  justify-content: center;
}

/* Optional: Add a subtle animation when the page enters */
.register-view {
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>