<template>
  <div id="app">
    <!-- Header Component -->
    <HeaderComponent />

    <!-- Main Content Area -->
    <main class="main-content">
      <RouterView v-slot="{ Component }">
        <Transition name="fade" mode="out-in">
          <component :is="Component" />
        </Transition>
      </RouterView>
    </main>

    <!-- Footer Component -->
    <FooterComponent />

    <!-- Scroll to Top Button -->
    <button
      v-if="showScrollTop"
      @click="scrollToTop"
      class="scroll-to-top"
      aria-label="Scroll to top"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
      >
        <polyline points="18 15 12 9 6 15"></polyline>
      </svg>
    </button>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue';
import HeaderComponent from './components/common/Header.vue';
import FooterComponent from './components/common/Footer.vue';

export default {
  name: 'App',
  components: {
    HeaderComponent,
    FooterComponent
  },
  setup() {
    const showScrollTop = ref(false);

    // Handle scroll to show/hide scroll-to-top button
    const handleScroll = () => {
      showScrollTop.value = window.scrollY > 300;
    };

    // Scroll to top function
    const scrollToTop = () => {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    };

    // Lifecycle hooks
    onMounted(() => {
      window.addEventListener('scroll', handleScroll);
    });

    onUnmounted(() => {
      window.removeEventListener('scroll', handleScroll);
    });

    return {
      showScrollTop,
      scrollToTop
    };
  }
};
</script>

<style>
/* Import global styles */
@import './assets/base.css';
@import './assets/main.css';

/* App specific styles */
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  width: 100%;
}

/* Scroll to Top Button */
.scroll-to-top {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  width: 50px;
  height: 50px;
  border-radius: var(--radius-full);
  background-color: var(--color-primary);
  color: var(--color-gray-900);
  border: none;
  box-shadow: var(--shadow-lg);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-base);
  z-index: var(--z-index-fixed);
  opacity: 0;
  visibility: hidden;
  transform: translateY(10px);
}

.scroll-to-top:hover {
  background-color: var(--color-primary-dark);
  transform: translateY(-2px);
  box-shadow: var(--shadow-xl);
}

.scroll-to-top:active {
  transform: translateY(0);
}

/* Show scroll button when active */
#app[data-scroll-top="true"] .scroll-to-top {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

/* Page Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .scroll-to-top {
    bottom: 1.5rem;
    right: 1.5rem;
    width: 45px;
    height: 45px;
  }
}
</style>