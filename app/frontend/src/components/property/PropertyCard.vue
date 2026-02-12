<template>
  <div class="property-card" @click="navigateToProperty">
    <!-- Property Image -->
    <div class="property-card-image-container">
      <img 
        :src="propertyImage" 
        :alt="property.title" 
        class="property-card-image"
        @error="handleImageError"
      />
      
      <!-- Status Badge -->
      <div 
        class="property-badge" 
        :class="property.status"
        v-if="property.status"
      >
        {{ property.status }}
      </div>

      <!-- Property Type Badge (Optional) -->
      <div class="property-type-badge" v-if="showPropertyType">
        {{ formatPropertyType(property.property_type) }}
      </div>
    </div>

    <!-- Property Content -->
    <div class="property-card-content">
      <!-- Price and Favorite Button -->
      <div class="property-header">
        <div class="property-price">
          {{ formatPrice(property.price) }}
          <span class="price-period" v-if="forRent">/month</span>
        </div>
        
        <!-- Favorite Button -->
        <button 
          @click.stop="toggleFavorite" 
          class="favorite-btn"
          :class="{ active: isFavorite }"
          :aria-label="isFavorite ? 'Remove from favorites' : 'Add to favorites'"
        >
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            width="20" 
            height="20" 
            viewBox="0 0 24 24" 
            :fill="isFavorite ? 'currentColor' : 'none'"
            stroke="currentColor" 
            stroke-width="2" 
            stroke-linecap="round" 
            stroke-linejoin="round"
          >
            <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
          </svg>
        </button>
      </div>

      <!-- Title -->
      <h3 class="property-title">{{ property.title }}</h3>

      <!-- Location -->
      <div class="property-location" v-if="location">
        <svg 
          xmlns="http://www.w3.org/2000/svg" 
          width="16" 
          height="16" 
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
        <span>{{ formatLocation(location) }}</span>
      </div>

      <!-- Description (Optional, truncated) -->
      <p class="property-description" v-if="showDescription && property.description">
        {{ truncateText(property.description, 80) }}
      </p>

      <!-- Features -->
      <div class="property-features">
        <!-- Bedrooms -->
        <div class="property-feature" v-if="property.bedrooms">
          <svg 
            class="property-feature-icon"
            xmlns="http://www.w3.org/2000/svg" 
            width="18" 
            height="18" 
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            stroke-width="2" 
            stroke-linecap="round" 
            stroke-linejoin="round"
          >
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
            <polyline points="9 22 9 12 15 12 15 22"></polyline>
          </svg>
          <span>{{ property.bedrooms }} {{ property.bedrooms === 1 ? 'Bed' : 'Beds' }}</span>
        </div>

        <!-- Bathrooms -->
        <div class="property-feature" v-if="property.bathrooms">
          <svg 
            class="property-feature-icon"
            xmlns="http://www.w3.org/2000/svg" 
            width="18" 
            height="18" 
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            stroke-width="2" 
            stroke-linecap="round" 
            stroke-linejoin="round"
          >
            <path d="M9 6 6.5 3.5a1.5 1.5 0 0 0-1 0c-.9.4-1.5 1.2-1.5 2.1v2.9a2 2 0 0 0 .5 1.5L6 12"></path>
            <path d="M6 12h12"></path>
            <path d="M18 12l1.5 1.5a2 2 0 0 0 .5 1.5v2.9c0 .9-.6 1.7-1.5 2.1-.3.1-.7.1-1 0L15 18"></path>
            <path d="M12 12v6"></path>
          </svg>
          <span>{{ property.bathrooms }} {{ property.bathrooms === 1 ? 'Bath' : 'Baths' }}</span>
        </div>

        <!-- Area -->
        <div class="property-feature" v-if="property.area_sqm">
          <svg 
            class="property-feature-icon"
            xmlns="http://www.w3.org/2000/svg" 
            width="18" 
            height="18" 
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            stroke-width="2" 
            stroke-linecap="round" 
            stroke-linejoin="round"
          >
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <line x1="9" y1="3" x2="9" y2="21"></line>
            <line x1="15" y1="3" x2="15" y2="21"></line>
            <line x1="3" y1="9" x2="21" y2="9"></line>
            <line x1="3" y1="15" x2="21" y2="15"></line>
          </svg>
          <span>{{ formatArea(property.area_sqm) }}</span>
        </div>

        <!-- Views Count (Optional) -->
        <div class="property-feature" v-if="showViews && property.views_count">
          <svg 
            class="property-feature-icon"
            xmlns="http://www.w3.org/2000/svg" 
            width="18" 
            height="18" 
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            stroke-width="2" 
            stroke-linecap="round" 
            stroke-linejoin="round"
          >
            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
            <circle cx="12" cy="12" r="3"></circle>
          </svg>
          <span>{{ formatNumber(property.views_count) }} views</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'PropertyCard',
  props: {
    property: {
      type: Object,
      required: true
    },
    location: {
      type: Object,
      default: null
    },
    forRent: {
      type: Boolean,
      default: false
    },
    showDescription: {
      type: Boolean,
      default: false
    },
    showPropertyType: {
      type: Boolean,
      default: false
    },
    showViews: {
      type: Boolean,
      default: false
    },
    initialFavorite: {
      type: Boolean,
      default: false
    }
  },
  emits: ['favorite-toggled'],
  setup(props, { emit }) {
    const router = useRouter();
    const isFavorite = ref(props.initialFavorite);
    const imageError = ref(false);

    // Computed property for image source
    const propertyImage = computed(() => {
      if (imageError.value) {
        return 'https://via.placeholder.com/400x240/e4a95d/ffffff?text=No+Image';
      }
      
      if (props.property.photo_location && props.property.photo_location.length > 0) {
        return props.property.photo_location[0];
      }
      
      return 'https://via.placeholder.com/400x240/e4a95d/ffffff?text=Property+Image';
    });

    // Handle image load error
    const handleImageError = () => {
      imageError.value = true;
    };

    // Format price
    const formatPrice = (price) => {
      if (!price) return 'Price not available';
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
      }).format(price);
    };

    // Format location
    const formatLocation = (location) => {
      if (!location) return '';
      
      const parts = [];
      if (location.city) parts.push(location.city);
      if (location.province) parts.push(location.province);
      
      return parts.join(', ');
    };

    // Format area
    const formatArea = (area) => {
      if (!area) return '';
      return `${area.toLocaleString()} m²`;
    };

    // Format property type
    const formatPropertyType = (type) => {
      if (!type) return '';
      return type.charAt(0).toUpperCase() + type.slice(1);
    };

    // Format number with commas
    const formatNumber = (num) => {
      if (!num) return '0';
      return num.toLocaleString();
    };

    // Truncate text
    const truncateText = (text, maxLength) => {
      if (!text) return '';
      if (text.length <= maxLength) return text;
      return text.substring(0, maxLength) + '...';
    };

    // Toggle favorite
    const toggleFavorite = () => {
      isFavorite.value = !isFavorite.value;
      emit('favorite-toggled', {
        propertyId: props.property.id,
        isFavorite: isFavorite.value
      });
    };

    // Navigate to property detail page
    const navigateToProperty = () => {
      router.push({
        name: 'property-detail',
        params: { id: props.property.id }
      });
    };

    return {
      isFavorite,
      propertyImage,
      handleImageError,
      formatPrice,
      formatLocation,
      formatArea,
      formatPropertyType,
      formatNumber,
      truncateText,
      toggleFavorite,
      navigateToProperty
    };
  }
};
</script>

<style scoped>
/* Additional specific styles that aren't in main.css */

.property-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-sm);
}

.property-price {
  flex: 1;
}

/* Favorite Button in Content Area */
.favorite-btn {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-full);
  background-color: transparent;
  border: 2px solid var(--color-border);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-base);
  color: var(--color-text-secondary);
  flex-shrink: 0;
}

.favorite-btn:hover {
  background-color: var(--color-primary-light);
  border-color: var(--color-primary);
  color: var(--color-primary-dark);
}

.favorite-btn.active {
  background-color: var(--color-accent-light);
  border-color: var(--color-accent);
  color: var(--color-accent);
}

.property-type-badge {
  position: absolute;
  bottom: var(--spacing-md);
  left: var(--spacing-md);
  padding: var(--spacing-xs) var(--spacing-md);
  background-color: rgba(0, 0, 0, 0.7);
  color: var(--color-white);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-radius: var(--radius-md);
  backdrop-filter: blur(4px);
}

.property-description {
  color: var(--color-text-secondary);
  font-size: var(--font-size-sm);
  line-height: var(--line-height-relaxed);
  margin-bottom: var(--spacing-md);
}

.price-period {
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-normal);
  color: var(--color-text-secondary);
}

/* Favorite button animation */
.favorite-btn svg {
  transition: transform var(--transition-base);
}

.favorite-btn:hover svg {
  transform: scale(1.1);
}

.favorite-btn.active {
  animation: heartBeat 0.3s ease-in-out;
}

@keyframes heartBeat {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.15);
  }
}

/* Loading state for image */
.property-card-image {
  background-color: var(--color-gray-200);
}

/* Feature spacing adjustments */
.property-feature:not(:last-child) {
  position: relative;
}

.property-feature:not(:last-child)::after {
  content: '';
  position: absolute;
  right: calc(-1 * var(--spacing-lg) / 2);
  top: 50%;
  transform: translateY(-50%);
  width: 1px;
  height: 16px;
  background-color: var(--color-border);
}

/* Hover effect for entire card */
.property-card {
  position: relative;
  overflow: hidden;
}

.property-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
  transform: translateX(-100%);
  transition: transform var(--transition-slow);
}

.property-card:hover::before {
  transform: translateX(0);
}

/* Status badge colors - enhanced */
.property-badge.available {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.85;
  }
}

/* Responsive adjustments */
@media (max-width: 480px) {
  .property-price {
    font-size: var(--font-size-xl);
  }

  .property-title {
    font-size: var(--font-size-base);
  }

  .property-features {
    gap: var(--spacing-md);
  }

  .property-feature {
    font-size: var(--font-size-xs);
  }

  .property-feature-icon {
    width: 16px;
    height: 16px;
  }

  .property-feature:not(:last-child)::after {
    display: none;
  }
}

/* Print styles */
@media print {
  .favorite-btn {
    display: none;
  }

  .property-card {
    box-shadow: none;
    border: 1px solid var(--color-border);
  }

  .property-card:hover {
    transform: none;
  }
}
</style>