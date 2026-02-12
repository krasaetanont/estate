<template>
  <div class="property-list-container">
    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p class="loading-text">Loading properties...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-container">
      <div class="alert alert-error">
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
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" y1="8" x2="12" y2="12"></line>
          <line x1="12" y1="16" x2="12.01" y2="16"></line>
        </svg>
        <div>
          <strong>Error loading properties</strong>
          <p>{{ error }}</p>
        </div>
      </div>
      <button @click="fetchProperties" class="btn btn-primary">
        Try Again
      </button>
    </div>

    <!-- Empty State -->
    <div v-else-if="!properties || properties.length === 0" class="empty-container">
      <svg 
        xmlns="http://www.w3.org/2000/svg" 
        width="64" 
        height="64" 
        viewBox="0 0 24 24" 
        fill="none" 
        stroke="currentColor" 
        stroke-width="1.5" 
        stroke-linecap="round" 
        stroke-linejoin="round"
        class="empty-icon"
      >
        <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
        <polyline points="9 22 9 12 15 12 15 22"></polyline>
      </svg>
      <h3 class="empty-title">No Properties Found</h3>
      <p class="empty-description">
        We couldn't find any properties matching your criteria. 
        Try adjusting your filters or check back later.
      </p>
    </div>

    <!-- Property Grid -->
    <div v-else>
      <!-- Results Count -->
      <div class="results-header">
        <h2 class="results-count">
          {{ properties.length }} {{ properties.length === 1 ? 'Property' : 'Properties' }} Found
        </h2>
        
        <!-- Sort Options -->
        <div class="sort-container" v-if="showSort">
          <label for="sort-select" class="sort-label">Sort by:</label>
          <select 
            id="sort-select"
            v-model="sortBy" 
            @change="handleSort"
            class="sort-select"
          >
            <option value="newest">Newest First</option>
            <option value="oldest">Oldest First</option>
            <option value="price-low">Price: Low to High</option>
            <option value="price-high">Price: High to Low</option>
            <option value="views">Most Viewed</option>
          </select>
        </div>
      </div>

      <!-- Property Grid -->
      <div class="property-flex">
        <PropertyCard
          v-for="property in sortedProperties"
          :key="property.id"
          :property="property"
          :location="getLocation(property.location_id)"
          :forRent="forRent"
          :showDescription="showDescription"
          :showPropertyType="showPropertyType"
          :showViews="showViews"
          :initialFavorite="isFavorite(property.id)"
          @favorite-toggled="handleFavoriteToggle"
        />
      </div>

      <!-- Pagination (Optional) -->
      <div v-if="showPagination && totalPages > 1" class="pagination">
        <button 
          @click="goToPage(currentPage - 1)"
          :disabled="currentPage === 1"
          class="pagination-btn"
        >
          Previous
        </button>

        <button
          v-for="page in displayedPages"
          :key="page"
          @click="goToPage(page)"
          :class="['pagination-btn', { active: page === currentPage }]"
        >
          {{ page }}
        </button>

        <button 
          @click="goToPage(currentPage + 1)"
          :disabled="currentPage === totalPages"
          class="pagination-btn"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import PropertyCard from './PropertyCard.vue';

export default {
  name: 'PropertyList',
  components: {
    PropertyCard
  },
  props: {
    jsonPath: {
      type: String,
      default: '/example.json' // Path to your JSON file in public folder
    },
    filterStatus: {
      type: String,
      default: null // 'available', 'pending', 'sold'
    },
    filterType: {
      type: String,
      default: null // 'house', 'apartment', 'land'
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
      default: true
    },
    showViews: {
      type: Boolean,
      default: false
    },
    showSort: {
      type: Boolean,
      default: true
    },
    showPagination: {
      type: Boolean,
      default: false
    },
    itemsPerPage: {
      type: Number,
      default: 9
    },
    limit: {
      type: Number,
      default: null // Maximum number of properties to display (null = no limit)
    }
  },
  setup(props) {
    const loading = ref(true);
    const error = ref(null);
    const allData = ref(null);
    const properties = ref([]);
    const locations = ref([]);
    const favorites = ref([]);
    const sortBy = ref('newest');
    const currentPage = ref(1);

    // Fetch properties from JSON file
    const fetchProperties = async () => {
      loading.value = true;
      error.value = null;

      try {
        const response = await fetch(props.jsonPath);
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        allData.value = data;
        locations.value = data.locations || [];
        favorites.value = data.favorites || [];
        
        // Filter properties based on props
        let filteredProperties = data.properties || [];
        
        // Filter by status
        if (props.filterStatus) {
          filteredProperties = filteredProperties.filter(
            p => p.status === props.filterStatus
          );
        }
        
        // Filter by type
        if (props.filterType) {
          filteredProperties = filteredProperties.filter(
            p => p.property_type === props.filterType
          );
        }
        
        properties.value = filteredProperties;
        
      } catch (err) {
        console.error('Error fetching properties:', err);
        error.value = err.message || 'Failed to load properties. Please try again.';
      } finally {
        loading.value = false;
      }
    };

    // Get location by ID
    const getLocation = (locationId) => {
      if (!locationId || !locations.value) return null;
      return locations.value.find(loc => loc.id === locationId);
    };

    // Check if property is in favorites
    const isFavorite = (propertyId) => {
      if (!favorites.value) return false;
      return favorites.value.some(fav => fav.property_id === propertyId);
    };

    // Handle favorite toggle
    const handleFavoriteToggle = ({ propertyId, isFavorite }) => {
      console.log(`Property ${propertyId} favorite status: ${isFavorite}`);
      
      // In a real app, you would make an API call here
      // For now, just update local state
      if (isFavorite) {
        favorites.value.push({
          id: Date.now(),
          user_id: 1, // Mock user ID
          property_id: propertyId,
          created_at: new Date().toISOString()
        });
      } else {
        favorites.value = favorites.value.filter(
          fav => fav.property_id !== propertyId
        );
      }
    };

    // Sort properties
    const sortedProperties = computed(() => {
      if (!properties.value) return [];
      
      let sorted = [...properties.value];
      
      switch (sortBy.value) {
        case 'newest':
          sorted.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
          break;
        case 'oldest':
          sorted.sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
          break;
        case 'price-low':
          sorted.sort((a, b) => a.price - b.price);
          break;
        case 'price-high':
          sorted.sort((a, b) => b.price - a.price);
          break;
        case 'views':
          sorted.sort((a, b) => (b.views_count || 0) - (a.views_count || 0));
          break;
        default:
          break;
      }
      
      // Apply limit if specified (before pagination)
      if (props.limit && props.limit > 0) {
        sorted = sorted.slice(0, props.limit);
      }
      
      // Apply pagination if enabled
      if (props.showPagination) {
        const start = (currentPage.value - 1) * props.itemsPerPage;
        const end = start + props.itemsPerPage;
        return sorted.slice(start, end);
      }
      
      return sorted;
    });

    // Handle sort change
    const handleSort = () => {
      currentPage.value = 1; // Reset to first page on sort
    };

    // Pagination computed properties
    const totalPages = computed(() => {
      if (!props.showPagination || !properties.value) return 1;
      
      // Calculate total items considering the limit
      let totalItems = properties.value.length;
      if (props.limit && props.limit > 0) {
        totalItems = Math.min(totalItems, props.limit);
      }
      
      return Math.ceil(totalItems / props.itemsPerPage);
    });

    const displayedPages = computed(() => {
      const pages = [];
      const total = totalPages.value;
      const current = currentPage.value;
      
      // Show max 5 page numbers
      let start = Math.max(1, current - 2);
      let end = Math.min(total, current + 2);
      
      // Adjust if at the beginning or end
      if (current <= 3) {
        end = Math.min(5, total);
      }
      if (current >= total - 2) {
        start = Math.max(1, total - 4);
      }
      
      for (let i = start; i <= end; i++) {
        pages.push(i);
      }
      
      return pages;
    });

    const goToPage = (page) => {
      if (page < 1 || page > totalPages.value) return;
      currentPage.value = page;
      
      // Scroll to top of property list
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    };

    // Fetch on mount
    onMounted(() => {
      fetchProperties();
    });

    return {
      loading,
      error,
      properties,
      locations,
      favorites,
      sortBy,
      currentPage,
      sortedProperties,
      totalPages,
      displayedPages,
      fetchProperties,
      getLocation,
      isFavorite,
      handleFavoriteToggle,
      handleSort,
      goToPage
    };
  }
};
</script>

<style scoped>
.property-list-container {
  width: 100%;
}

/* Loading State */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  gap: var(--spacing-lg);
}

.property-flex {
  display: flex;
  flex-direction: row;
  justify-content: center;
  flex-wrap: wrap;
  gap: var(--spacing-lg);
}

.loading-text {
  color: var(--color-text-secondary);
  font-size: var(--font-size-lg);
}

/* Error State */
.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  gap: var(--spacing-xl);
  padding: var(--spacing-2xl);
}

.alert {
  display: flex;
  gap: var(--spacing-md);
  align-items: flex-start;
  max-width: 600px;
  width: 100%;
}

.alert svg {
  flex-shrink: 0;
  margin-top: 2px;
}

.alert strong {
  display: block;
  margin-bottom: var(--spacing-xs);
}

.alert p {
  margin: 0;
  font-size: var(--font-size-sm);
}

/* Empty State */
.empty-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  text-align: center;
  padding: var(--spacing-3xl) var(--spacing-lg);
}

.empty-icon {
  color: var(--color-gray-400);
  margin-bottom: var(--spacing-lg);
}

.empty-title {
  font-size: var(--font-size-2xl);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-md);
}

.empty-description {
  color: var(--color-text-secondary);
  max-width: 500px;
  line-height: var(--line-height-relaxed);
}

/* Results Header */
.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-xl);
  flex-wrap: wrap;
  gap: var(--spacing-md);
}

.results-count {
  font-size: var(--font-size-2xl);
  color: var(--color-text-primary);
  margin: 0;
}

/* Sort Container */
.sort-container {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.sort-label {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  font-weight: var(--font-weight-medium);
}

.sort-select {
  padding: var(--spacing-sm) var(--spacing-md);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background-color: var(--color-white);
  color: var(--color-text-primary);
  font-size: var(--font-size-sm);
  cursor: pointer;
  transition: border-color var(--transition-base);
}

.sort-select:hover {
  border-color: var(--color-primary);
}

.sort-select:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(255, 195, 96, 0.1);
}

/* Responsive */
@media (max-width: 768px) {
  .results-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .results-count {
    font-size: var(--font-size-xl);
  }

  .sort-container {
    width: 100%;
  }

  .sort-select {
    flex: 1;
  }
}

@media (max-width: 480px) {
  .results-count {
    font-size: var(--font-size-lg);
  }

  .empty-title {
    font-size: var(--font-size-xl);
  }

  .loading-container,
  .error-container,
  .empty-container {
    min-height: 300px;
    padding: var(--spacing-xl) var(--spacing-md);
  }
}
</style>