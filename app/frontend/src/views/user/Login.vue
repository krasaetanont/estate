<template>
  <main class="login-view">
    <div class="container">
      <Login @login-success="onLoginSuccess" />
    </div>
  </main>
</template>

<script setup lang="ts">
import Login from '../../components/user/Login.vue'
import { useRouter } from 'vue-router'

const router = useRouter()

/**
 * Handles the event emitted from the Login component
 * when a user successfully authenticates.
 */
const onLoginSuccess = () => {
  // Redirect to dashboard or home after login
  router.push({ name: 'home' })
}
</script>

<style scoped>
.login-view {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 80px); /* Adjust based on your Header height */
  background-color: var(--color-background-soft);
  padding: var(--spacing-md);
}

.container {
  width: 100%;
  display: flex;
  justify-content: center;
}
</style>