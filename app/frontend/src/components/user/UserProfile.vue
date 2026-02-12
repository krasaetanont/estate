<template>
  <div class="profile-container">
    <div class="profile-grid">
      <aside class="profile-sidebar">
        <div class="user-info-card">
          <div class="avatar-wrapper">
            <img :src="user.avatar || '/default-avatar.png'" alt="User Avatar" class="profile-avatar" />
            <button class="edit-avatar-btn" title="Change Photo">
              <i class="camera-icon">📷</i>
            </button>
          </div>
          <h3 class="user-name">{{ user.name }}</h3>
          <p class="user-role">Premium Member</p>
        </div>

        <nav class="profile-nav">
          <button 
            v-for="tab in tabs" 
            :key="tab.id"
            :class="['nav-item', { active: activeTab === tab.id }]"
            @click="activeTab = tab.id"
          >
            {{ tab.label }}
          </button>
          <button class="nav-item logout-btn" @click="handleLogout">Logout</button>
        </nav>
      </aside>

      <main class="profile-content">
        <section v-if="activeTab === 'settings'" class="content-card">
          <h2 class="section-title">Account Settings</h2>
          <form @submit.prevent="updateProfile" class="profile-form">
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">Full Name</label>
                <input v-model="user.name" type="text" class="form-input" />
              </div>
              <div class="form-group">
                <label class="form-label">Email Address</label>
                <input v-model="user.email" type="email" class="form-input" disabled />
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">Phone Number</label>
              <input v-model="user.phone" type="tel" class="form-input" placeholder="+1 (555) 000-0000" />
            </div>

            <div class="form-group">
              <label class="form-label">Bio</label>
              <textarea v-model="user.bio" class="form-input" rows="4" placeholder="Tell us about yourself..."></textarea>
            </div>

            <div class="form-actions">
              <button type="submit" class="btn btn-primary" :disabled="isUpdating">
                {{ isUpdating ? 'Saving...' : 'Save Changes' }}
              </button>
            </div>
          </form>
        </section>

        <section v-if="activeTab === 'listings'" class="content-card">
          <div class="section-header">
            <h2 class="section-title">My Property Listings</h2>
            <button class="btn btn-outline btn-sm">Add New Property</button>
          </div>
          
          <div v-if="userListings.length === 0" class="empty-state">
            <p>You haven't posted any properties yet.</p>
          </div>
          </section>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'

const activeTab = ref('settings')
const isUpdating = ref(false)

const tabs = [
  { id: 'settings', label: 'Profile Settings' },
  { id: 'listings', label: 'My Listings' },
  { id: 'favorites', label: 'Saved Properties' }
]

// Mock User Data - In a real app, fetch this from Pinia or API
const user = reactive({
  name: 'John Doe',
  email: 'john.doe@example.com',
  phone: '',
  bio: 'Looking for a modern apartment in the city center.',
  avatar: null
})

const userListings = ref([])

const updateProfile = async () => {
  isUpdating.value = true
  // Simulate API call
  setTimeout(() => {
    isUpdating.value = false
    alert('Profile updated successfully!')
  }, 1000)
}

const handleLogout = () => {
  // Logic to clear tokens and redirect to Home
  console.log('Logging out...')
}
</script>

<style scoped>
.profile-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--spacing-xl) var(--spacing-md);
}

.profile-grid {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: var(--spacing-xl);
}

/* Sidebar Styling */
.profile-sidebar {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.user-info-card {
  background: var(--color-white);
  padding: var(--spacing-xl);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  text-align: center;
}

.avatar-wrapper {
  position: relative;
  width: 120px;
  height: 120px;
  margin: 0 auto var(--spacing-md);
}

.profile-avatar {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid var(--color-gray-100);
}

.edit-avatar-btn {
  position: absolute;
  bottom: 0;
  right: 0;
  background: var(--color-primary);
  border: none;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.profile-nav {
  background: var(--color-white);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}

.nav-item {
  width: 100%;
  padding: var(--spacing-md) var(--spacing-lg);
  border: none;
  background: none;
  text-align: left;
  cursor: pointer;
  font-weight: var(--font-weight-medium);
  transition: all var(--transition-base);
  border-left: 4px solid transparent;
}

.nav-item:hover {
  background: var(--color-gray-50);
}

.nav-item.active {
  background: var(--color-gray-50);
  border-left-color: var(--color-primary);
  color: var(--color-primary);
}

.logout-btn {
  color: #dc3545;
  margin-top: var(--spacing-md);
}

/* Content Area */
.content-card {
  background: var(--color-white);
  padding: var(--spacing-2xl);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
}

.section-title {
  font-size: var(--font-size-xl);
  margin-bottom: var(--spacing-xl);
  color: var(--color-text-primary);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-md);
}

.profile-form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.empty-state {
  text-align: center;
  padding: var(--spacing-2xl);
  color: var(--color-text-secondary);
  border: 2px dashed var(--color-border);
  border-radius: var(--radius-md);
}

@media (max-width: 768px) {
  .profile-grid {
    grid-template-columns: 1fr;
  }
}
</style>