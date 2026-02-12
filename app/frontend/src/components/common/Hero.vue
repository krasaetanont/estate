<!-- usage
title: String - Main heading
subtitle: String - Subheading
videoSrc: String - Path to video file (e.g., '/welcome.mp4')
imageSrc: String - Fallback image
showSearch: Boolean - Show search bar or CTA buttons
showStats: Boolean - Show statistics
showScrollIndicator: Boolean - Show scroll indicator
ctaButtons: Array - Custom CTA buttons
stats: Array - Custom statistics -->

<template>
  <section class="hero">
    <!-- Video Background -->
    <video 
      v-if="videoSrc"
      class="hero-video" 
      :src="videoSrc"
      autoplay 
      loop 
      muted 
      playsinline
      @error="handleVideoError"
    ></video>

    <!-- Fallback Image Background -->
    <div 
      v-else-if="imageSrc" 
      class="hero-image"
      :style="{ backgroundImage: `url(${imageSrc})` }"
    ></div>

    <!-- Overlay -->
    <div class="hero-overlay"></div>

    <!-- Hero Content -->
    <div class="hero-content">
      <div class="container">
        <!-- Title -->
        <h1 class="hero-title" :class="{ 'fade-in': isLoaded }">
          {{ title }}
        </h1>

        <!-- Subtitle -->
        <p class="hero-subtitle" :class="{ 'fade-in': isLoaded }">
          {{ subtitle }}
        </p>

        <!-- Search Bar (Optional) -->
        <div v-if="showSearch" class="hero-search" :class="{ 'slide-up': isLoaded }">
          <div class="search-bar">
            <!-- Search Type Tabs -->
            <div class="search-tabs">
              <button 
                v-for="tab in searchTabs"
                :key="tab.value"
                @click="activeTab = tab.value"
                :class="['search-tab', { active: activeTab === tab.value }]"
              >
                {{ tab.label }}
              </button>
            </div>

            <!-- Search Inputs -->
            <div class="search-inputs">
              <!-- Location Input -->
              <div class="search-input-group">
                <label for="location" class="sr-only">Location</label>
                <div class="input-with-icon">
                  <svg 
                    class="input-icon"
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
                    <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                    <circle cx="12" cy="10" r="3"></circle>
                  </svg>
                  <input 
                    id="location"
                    v-model="searchQuery.location"
                    type="text" 
                    class="search-input" 
                    placeholder="Enter city, neighborhood..."
                  />
                </div>
              </div>

              <!-- Property Type Select -->
              <div class="search-input-group">
                <label for="property-type" class="sr-only">Property Type</label>
                <select 
                  id="property-type"
                  v-model="searchQuery.propertyType"
                  class="search-select"
                >
                  <option value="">All Property Types</option>
                  <option value="house">House</option>
                  <option value="apartment">Apartment</option>
                  <option value="land">Land</option>
                </select>
              </div>

              <!-- Price Range Select -->
              <div class="search-input-group">
                <label for="price-range" class="sr-only">Price Range</label>
                <select 
                  id="price-range"
                  v-model="searchQuery.priceRange"
                  class="search-select"
                >
                  <option value="">Any Price</option>
                  <option value="0-300000">Under $300k</option>
                  <option value="300000-500000">$300k - $500k</option>
                  <option value="500000-750000">$500k - $750k</option>
                  <option value="750000-1000000">$750k - $1M</option>
                  <option value="1000000-999999999">$1M+</option>
                </select>
              </div>

              <!-- Bedrooms Select -->
              <div class="search-input-group">
                <label for="bedrooms" class="sr-only">Bedrooms</label>
                <select 
                  id="bedrooms"
                  v-model="searchQuery.bedrooms"
                  class="search-select"
                >
                  <option value="">Any Beds</option>
                  <option value="1">1+ Beds</option>
                  <option value="2">2+ Beds</option>
                  <option value="3">3+ Beds</option>
                  <option value="4">4+ Beds</option>
                  <option value="5">5+ Beds</option>
                </select>
              </div>

              <!-- Search Button -->
              <button 
                @click="handleSearch" 
                class="btn btn-primary btn-search"
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
                  <circle cx="11" cy="11" r="8"></circle>
                  <path d="m21 21-4.35-4.35"></path>
                </svg>
                Search
              </button>
            </div>
          </div>
        </div>

        <!-- Call to Action Buttons (Alternative to Search) -->
        <div v-else class="hero-cta">
          <RouterLink 
            v-for="cta in ctaButtons"
            :key="cta.text"
            :to="cta.link"
            :class="['btn', cta.variant || 'btn-primary', cta.size || 'btn-lg']"
          >
            {{ cta.text }}
          </RouterLink>
        </div>

        <!-- Stats (Optional) -->
        <div v-if="showStats" class="hero-stats">
          <div 
            v-for="stat in stats"
            :key="stat.label"
            class="hero-stat"
          >
            <div class="hero-stat-value">{{ stat.value }}</div>
            <div class="hero-stat-label">{{ stat.label }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Scroll Down Indicator -->
    <div v-if="showScrollIndicator" class="scroll-indicator">
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
        <polyline points="6 9 12 15 18 9"></polyline>
      </svg>
    </div>
  </section>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'HeroComponent',
  props: {
    title: {
      type: String,
      default: 'Find Your Dream Home'
    },
    subtitle: {
      type: String,
      default: 'Browse thousands of properties from trusted sellers'
    },
    videoSrc: {
      type: String,
      default: null // e.g., '/welcome.mp4'
    },
    imageSrc: {
      type: String,
      default: null // Fallback image if video fails or not provided
    },
    showSearch: {
      type: Boolean,
      default: true
    },
    showStats: {
      type: Boolean,
      default: false
    },
    showScrollIndicator: {
      type: Boolean,
      default: true
    },
    ctaButtons: {
      type: Array,
      default: () => [
        { text: 'Browse Properties', link: '/buy', variant: 'btn-primary' },
        { text: 'Sell Your Home', link: '/seller', variant: 'btn-outline' }
      ]
    },
    stats: {
      type: Array,
      default: () => [
        { value: '10,000+', label: 'Properties' },
        { value: '5,000+', label: 'Happy Customers' },
        { value: '500+', label: 'Agents' }
      ]
    }
  },
  emits: ['search'],
  setup(props, { emit }) {
    const router = useRouter();
    const isLoaded = ref(false);
    const activeTab = ref('buy');
    const searchQuery = ref({
      location: '',
      propertyType: '',
      priceRange: '',
      bedrooms: ''
    });

    const searchTabs = [
      { label: 'Buy', value: 'buy' },
      { label: 'Rent', value: 'rent' }
    ];

    const handleVideoError = () => {
      console.warn('Video failed to load, falling back to image background');
    };

    const handleSearch = () => {
      // Emit search event with search data
      emit('search', {
        tab: activeTab.value,
        ...searchQuery.value
      });

      // Navigate to appropriate page with query params
      const query = {};
      
      if (searchQuery.value.location) {
        query.location = searchQuery.value.location;
      }
      if (searchQuery.value.propertyType) {
        query.type = searchQuery.value.propertyType;
      }
      if (searchQuery.value.priceRange) {
        const [min, max] = searchQuery.value.priceRange.split('-');
        query.minPrice = min;
        query.maxPrice = max;
      }
      if (searchQuery.value.bedrooms) {
        query.bedrooms = searchQuery.value.bedrooms;
      }

      const route = activeTab.value === 'buy' ? '/buy' : '/rent';
      
      router.push({
        path: route,
        query: Object.keys(query).length > 0 ? query : undefined
      });
    };

    onMounted(() => {
      // Trigger animations after mount
      setTimeout(() => {
        isLoaded.value = true;
      }, 100);
    });

    return {
      isLoaded,
      activeTab,
      searchQuery,
      searchTabs,
      handleVideoError,
      handleSearch
    };
  }
};
</script>

<style scoped>
.hero {
  position: relative;
  min-height: 600px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

/* Video Background */
.hero-video {
  position: absolute;
  top: 50%;
  left: 50%;
  min-width: 100%;
  min-height: 100%;
  width: auto;
  height: auto;
  transform: translate(-50%, -50%);
  object-fit: cover;
  z-index: 0;
}

/* Image Background */
.hero-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  z-index: 0;
}

/* Overlay */
.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    135deg, 
    rgba(228, 169, 93, 0.85) 0%, 
    rgba(255, 195, 96, 0.7) 100%
  );
  z-index: 1;
}

/* Content */
.hero-content {
  position: relative;
  z-index: 10;
  width: 70vw;
  padding: var(--spacing-3xl) var(--spacing-lg);
}

.hero-title {
  font-size: var(--font-size-5xl);
  font-weight: var(--font-weight-bold);
  margin-bottom: var(--spacing-lg);
  color: var(--color-white);
  text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.3);
  text-align: center;
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.6s ease-out;
}

.hero-title.fade-in {
  opacity: 1;
  transform: translateY(0);
}

.hero-subtitle {
  font-size: var(--font-size-xl);
  margin-bottom: var(--spacing-2xl);
  color: var(--color-white);
  opacity: 0.95;
  text-align: center;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
  text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.2);
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.6s ease-out 0.2s;
}

.hero-subtitle.fade-in {
  opacity: 0.95;
  transform: translateY(0);
}

/* Search Bar */
.hero-search {
  max-width: 1000px;
  width: 100%;
  margin: 0 auto;
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.6s ease-out 0.4s;
}

.hero-search.slide-up {
  opacity: 1;
  transform: translateY(0);
}

.search-tabs {
  display: flex;
  gap: var(--spacing-xs);
  margin-bottom: var(--spacing-md);
  justify-content: center;
}

.search-tab {
  padding: var(--spacing-sm) var(--spacing-xl);
  background-color: rgba(255, 255, 255, 0.2);
  color: black;
  border: 2px solid transparent;
  border-radius: var(--radius-lg) var(--radius-lg) 0 0;
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-semibold);
  cursor: pointer;
  transition: all var(--transition-base);
  backdrop-filter: blur(4px);
}

.search-tab:hover {
  background-color: rgba(255, 255, 255, 0.3);
}
    
.search-tab.active {
  background-color: var(--color-primary-dark);
  color: var(--color-white);
  border-color: var(--color-white);
}

.search-inputs {
  display: flex;
  gap: var(--spacing-sm);
  align-items: stretch;
}

.search-input-group {
  flex: 1;
  min-width: 100px;
}

.input-with-icon {
  position: relative;
}

.input-icon {
  position: absolute;
  left: var(--spacing-md);
  top: 50%;
  transform: translateY(-50%);
  color: var(--color-text-secondary);
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: var(--spacing-md) var(--spacing-md) var(--spacing-md) 3rem;
  border: 2px solid transparent;
  border-radius: var(--radius-md);
  background-color: var(--color-white);
  font-size: var(--font-size-base);
  transition: all var(--transition-base);
}

.search-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(255, 195, 96, 0.2);
}

.btn-search {
  white-space: nowrap;
  padding: var(--spacing-md) var(--spacing-2xl);
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

/* CTA Buttons */
.hero-cta {
  display: flex;
  gap: var(--spacing-md);
  justify-content: center;
  flex-wrap: wrap;
}

/* Stats */
.hero-stats {
  display: flex;
  justify-content: center;
  gap: var(--spacing-3xl);
  margin-top: var(--spacing-3xl);
  flex-wrap: wrap;
}

.hero-stat {
  text-align: center;
  color: var(--color-white);
}

.hero-stat-value {
  font-size: var(--font-size-4xl);
  font-weight: var(--font-weight-bold);
  margin-bottom: var(--spacing-xs);
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

.hero-stat-label {
  font-size: var(--font-size-base);
  opacity: 0.9;
  text-transform: uppercase;
  letter-spacing: 1px;
}

/* Scroll Indicator */
.scroll-indicator {
  position: absolute;
  bottom: var(--spacing-2xl);
  left: 50%;
  transform: translateX(-50%);
  z-index: 10;
  animation: bounce 2s infinite;
  color: var(--color-white);
  opacity: 0.8;
  cursor: pointer;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateX(-50%) translateY(0);
  }
  40% {
    transform: translateX(-50%) translateY(-10px);
  }
  60% {
    transform: translateX(-50%) translateY(-5px);
  }
}

/* Responsive Design */
@media (max-width: 1024px) {
  .search-inputs {
    flex-wrap: wrap;
  }

  .search-input-group {
    flex: 1 1 calc(50% - var(--spacing-sm));
    min-width: unset;
  }

  .btn-search {
    flex: 1 1 100%;
  }
}

@media (max-width: 768px) {
  .hero {
    min-height: 500px;
  }

  .hero-title {
    font-size: var(--font-size-3xl);
  }

  .hero-subtitle {
    font-size: var(--font-size-lg);
  }

  .search-tabs {
    width: 100%;
  }

  .search-tab {
    flex: 1;
    padding: var(--spacing-sm) var(--spacing-md);
  }

  .search-inputs {
    flex-direction: column;
  }

  .search-input-group {
    flex: 1 1 100%;
    width: 100%;
  }

  .hero-stats {
    gap: var(--spacing-xl);
  }

  .hero-stat-value {
    font-size: var(--font-size-2xl);
  }

  .hero-cta {
    flex-direction: column;
    align-items: stretch;
  }

  .hero-cta .btn {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .hero {
    min-height: 450px;
  }

  .hero-content {
    padding: var(--spacing-2xl) var(--spacing-md);
  }

  .hero-title {
    font-size: var(--font-size-2xl);
  }

  .hero-subtitle {
    font-size: var(--font-size-base);
    margin-bottom: var(--spacing-xl);
  }

  .search-tab {
    font-size: var(--font-size-sm);
    padding: var(--spacing-xs) var(--spacing-sm);
  }

  .hero-stats {
    gap: var(--spacing-lg);
  }

  .hero-stat-value {
    font-size: var(--font-size-xl);
  }

  .hero-stat-label {
    font-size: var(--font-size-sm);
  }
}

/* Performance optimization for video */
@media (prefers-reduced-motion: reduce) {
  .hero-video {
    display: none;
  }

  .scroll-indicator {
    animation: none;
  }
}
</style>