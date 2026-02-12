<template>
  <header class="header">
    <div class="header-container">
      <!-- Logo -->
      <RouterLink to="/" class="logo">
        <img src="../../assets/logo.svg" alt="Logo" class="logo-image" v-if="hasLogo" />
        <span class="logo-text">EstateMatch</span>
      </RouterLink>

      <!-- Desktop Navigation -->
      <nav>
        <ul class="nav-menu" :class="{ active: isMobileMenuOpen }">
          <li>
            <RouterLink to="/" class="nav-link" @click="closeMobileMenu">
              Home
            </RouterLink>
          </li>
          <li>
            <RouterLink to="/buy" class="nav-link" @click="closeMobileMenu">
              Buy
            </RouterLink>
          </li>
          <li>
            <RouterLink to="/rent" class="nav-link" @click="closeMobileMenu">
              Rent
            </RouterLink>
          </li>
          <li>
            <RouterLink to="/seller" class="nav-link" @click="closeMobileMenu">
              Sell
            </RouterLink>
          </li>
          <li>
            <RouterLink to="/about" class="nav-link" @click="closeMobileMenu">
              About
            </RouterLink>
          </li>
          <li>
            <RouterLink to="/contact" class="nav-link" @click="closeMobileMenu">
              Contact
            </RouterLink>
          </li>
        </ul>
      </nav>

      <!-- User Actions -->
      <div class="header-actions">
        <!-- Favorites (when logged in) -->
        <RouterLink 
          v-if="isLoggedIn" 
          to="/favorites" 
          class="icon-btn" 
          title="My Favorites"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
          </svg>
          <span class="favorite-count" v-if="favoriteCount > 0">{{ favoriteCount }}</span>
        </RouterLink>

        <!-- Login / Profile -->
        <div v-if="!isLoggedIn">
          <RouterLink to="/login" class="btn btn-primary btn-sm">
            Login
          </RouterLink>
        </div>
        <div v-else class="user-menu">
          <button @click="toggleUserMenu" class="user-menu-btn">
            <div class="user-avatar">
              {{ userInitials }}
            </div>
          </button>
          
          <!-- User Dropdown -->
          <div v-if="isUserMenuOpen" class="user-dropdown">
            <div class="user-dropdown-header">
              <div class="user-avatar-lg">{{ userInitials }}</div>
              <div>
                <div class="user-name">{{ userName }}</div>
                <div class="user-email">{{ userEmail }}</div>
              </div>
            </div>
            <div class="user-dropdown-divider"></div>
            <RouterLink to="/profile" class="user-dropdown-item" @click="closeUserMenu">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>
              Profile
            </RouterLink>
            <RouterLink to="/favorites" class="user-dropdown-item" @click="closeUserMenu">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
              </svg>
              Favorites
            </RouterLink>
            <RouterLink 
              v-if="userRole === 'seller' || userRole === 'agent'" 
              to="/seller" 
              class="user-dropdown-item" 
              @click="closeUserMenu"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
              </svg>
              My Listings
            </RouterLink>
            <div class="user-dropdown-divider"></div>
            <button @click="handleLogout" class="user-dropdown-item">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                <polyline points="16 17 21 12 16 7"></polyline>
                <line x1="21" y1="12" x2="9" y2="12"></line>
              </svg>
              Logout
            </button>
          </div>
        </div>

        <!-- Mobile Menu Toggle -->
        <button 
          @click="toggleMobileMenu" 
          class="menu-toggle" 
          aria-label="Toggle menu"
        >
          <span></span>
          <span></span>
          <span></span>
        </button>
      </div>
    </div>
  </header>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'HeaderComponent',
  setup() {
    const router = useRouter();
    const isMobileMenuOpen = ref(false);
    const isUserMenuOpen = ref(false);
    const hasLogo = ref(true);

    // Mock user data - Replace with actual authentication state
    const isLoggedIn = ref(false); // Change to true to test logged-in state
    const userName = ref('John Anderson');
    const userEmail = ref('john.anderson@example.com');
    const userRole = ref('seller'); // 'user', 'seller', 'agent', 'admin'
    const favoriteCount = ref(3);

    const userInitials = computed(() => {
      if (!userName.value) return 'U';
      const names = userName.value.split(' ');
      return names.map(n => n[0]).join('').toUpperCase().substring(0, 2);
    });

    const toggleMobileMenu = () => {
      isMobileMenuOpen.value = !isMobileMenuOpen.value;
    };

    const closeMobileMenu = () => {
      isMobileMenuOpen.value = false;
    };

    const toggleUserMenu = () => {
      isUserMenuOpen.value = !isUserMenuOpen.value;
    };

    const closeUserMenu = () => {
      isUserMenuOpen.value = false;
    };

    const handleLogout = () => {
      // Implement logout logic here
      isLoggedIn.value = false;
      closeUserMenu();
      router.push('/');
    };

    // Close menus when clicking outside
    const handleClickOutside = (event) => {
      if (!event.target.closest('.user-menu')) {
        isUserMenuOpen.value = false;
      }
      if (!event.target.closest('.header-container')) {
        isMobileMenuOpen.value = false;
      }
    };

    onMounted(() => {
      document.addEventListener('click', handleClickOutside);
    });

    onUnmounted(() => {
      document.removeEventListener('click', handleClickOutside);
    });

    return {
      isMobileMenuOpen,
      isUserMenuOpen,
      isLoggedIn,
      userName,
      userEmail,
      userRole,
      userInitials,
      favoriteCount,
      hasLogo,
      toggleMobileMenu,
      closeMobileMenu,
      toggleUserMenu,
      closeUserMenu,
      handleLogout
    };
  }
};
</script>

<style scoped>
.logo-image {
  width: 40px;
  height: 40px;
}

.logo-text {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-primary-dark);
}

.header-actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.icon-btn {
  position: relative;
  width: 40px;
  height: 40px;
  border-radius: var(--radius-full);
  background-color: transparent;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color var(--transition-base);
  color: var(--color-text-primary);
  text-decoration: none;
}

.icon-btn:hover {
  background-color: var(--color-gray-100);
  text-decoration: none;
}

.favorite-count {
  position: absolute;
  top: -4px;
  right: -4px;
  background-color: var(--color-accent);
  color: var(--color-white);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-bold);
  padding: 2px 6px;
  border-radius: var(--radius-full);
  min-width: 18px;
  text-align: center;
}

/* User Menu */
.user-menu {
  position: relative;
}

.user-menu-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-full);
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
  color: var(--color-white);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-sm);
  transition: transform var(--transition-base);
}

.user-menu-btn:hover .user-avatar {
  transform: scale(1.05);
}

.user-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  min-width: 260px;
  background-color: var(--color-white);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xl);
  padding: var(--spacing-sm);
  z-index: var(--z-index-dropdown);
  animation: slideDown 0.2s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.user-dropdown-header {
  display: flex;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
}

.user-avatar-lg {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-full);
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
  color: var(--color-white);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: var(--font-weight-bold);
  font-size: var(--font-size-lg);
  flex-shrink: 0;
}

.user-name {
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  font-size: var(--font-size-base);
}

.user-email {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  margin-top: 2px;
}

.user-dropdown-divider {
  height: 1px;
  background-color: var(--color-border);
  margin: var(--spacing-xs) 0;
}

.user-dropdown-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  width: 100%;
  padding: var(--spacing-sm) var(--spacing-md);
  border: none;
  background: none;
  color: var(--color-text-primary);
  font-size: var(--font-size-sm);
  text-align: left;
  text-decoration: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: background-color var(--transition-base);
}

.user-dropdown-item:hover {
  background-color: var(--color-gray-100);
  text-decoration: none;
}

.user-dropdown-item svg {
  color: var(--color-text-secondary);
}

/* Mobile styles */
@media (max-width: 768px) {
  .header-actions {
    gap: var(--spacing-sm);
  }

  .user-dropdown {
    right: 0;
    left: auto;
  }
}
</style>