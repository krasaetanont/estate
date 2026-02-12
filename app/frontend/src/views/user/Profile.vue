<template>
  <main class="profile-view">
    <header class="view-header">
      <div class="container">
        <h1 class="view-title">My Account</h1>
        <nav class="breadcrumb">
          <RouterLink to="/">Home</RouterLink> / <span>Profile</span>
        </nav>
      </div>
    </header>

    <UserProfile 
      :initial-user-data="userData" 
      @update-success="handleUpdateSuccess" 
    />
  </main>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import UserProfile from '../../components/user/UserProfile.vue'

// This could eventually come from your Pinia store (e.g., useAuthStore)
const userData = ref(null)

onMounted(async () => {
  // Logic to fetch user data if not already in store
  // Example: userData.value = await api.getUserProfile()
})

const handleUpdateSuccess = (updatedData: any) => {
  console.log('Profile view notified of update:', updatedData)
  // You might trigger a global toast notification here
}
</script>

<style scoped>
.profile-view {
  background-color: var(--color-background-soft);
  min-height: 100vh;
}

.view-header {
  background-color: var(--color-white);
  padding: var(--spacing-lg) 0;
  border-bottom: 1px solid var(--color-border);
  margin-bottom: var(--spacing-xl);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--spacing-md);
}

.view-title {
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-xs);
}

.breadcrumb {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}

.breadcrumb a {
  color: var(--color-primary);
  text-decoration: none;
}

.breadcrumb a:hover {
  text-decoration: underline;
}

/* Subtle entrance animation */
.profile-view {
  animation: fadeIn 0.4s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>