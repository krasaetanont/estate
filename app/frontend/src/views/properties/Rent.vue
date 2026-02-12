<template>
  <div class="buy-view">
    <!-- Hero Section with Search -->
    <HeroComponent 
      title="Find Your Perfect Home"
      subtitle="Browse thousands of properties for sale from trusted sellers"
      :videoSrc="null"
      imageSrc="https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=1920&q=80"
      :showSearch="true"
      :showStats="true"
      :showScrollIndicator="true"
      :stats="heroStats"
      @search="handleSearch"
    />

    <!-- Main Content -->
    <div class="container">
      <div class="buy-content">
        <!-- Page Header -->
        <div class="page-header">
          <div>
            <h1 class="page-title">Properties for Sale</h1>
            <p class="page-description">
              Discover your dream home from our extensive collection of properties
            </p>
          </div>

          <!-- Active Filters Display -->
          <div v-if="hasActiveFilters" class="active-filters">
            <span class="filter-label">Active Filters:</span>
            <div class="filter-tags">
              <span v-if="filters.location" class="filter-tag">
                📍 {{ filters.location }}
                <button @click="clearFilter('location')" class="filter-remove">×</button>
              </span>
              <span v-if="filters.propertyType" class="filter-tag">
                {{ formatPropertyType(filters.propertyType) }}
                <button @click="clearFilter('propertyType')" class="filter-remove">×</button>
              </span>
              <span v-if="filters.minPrice || filters.maxPrice" class="filter-tag">
                💰 {{ formatPriceRange(filters.minPrice, filters.maxPrice) }}
                <button @click="clearPriceFilter" class="filter-remove">×</button>
              </span>
              <span v-if="filters.bedrooms" class="filter-tag">
                🛏️ {{ filters.bedrooms }}+ Beds
                <button @click="clearFilter('bedrooms')" class="filter-remove">×</button>
              </span>
              <button @click="clearAllFilters" class="btn btn-sm btn-ghost">
                Clear All
              </button>
            </div>
          </div>
        </div>

        <!-- Property List Component -->
        <div v-if="loading && currentPage === 1" class="loading-state">
          <div class="spinner"></div>
          <p>Loading properties...</p>
        </div>

        <div v-else-if="allProperties.length === 0 && !loading" class="empty-state">
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            width="64" 
            height="64" 
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            stroke-width="2" 
            stroke-linecap="round" 
            stroke-linejoin="round"
          >
            <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
            <polyline points="9 22 9 12 15 12 15 22"></polyline>
          </svg>
          <h2>No Properties Found</h2>
          <p>Try adjusting your filters or search criteria</p>
          <button @click="clearAllFilters" class="btn btn-primary">Clear Filters</button>
        </div>

        <div v-else class="properties-section">
          <!-- Results Header -->
          <div class="results-header">
            <p class="results-count">
              Showing <strong>{{ currentDisplayCount }}</strong> of <strong>{{ totalProperties }}</strong> properties
            </p>
            
            <!-- Sort Options -->
            <div class="sort-options">
              <label for="sort">Sort by:</label>
              <select id="sort" v-model="sortBy" @change="handleSort" class="sort-select">
                <option value="newest">Newest First</option>
                <option value="oldest">Oldest First</option>
                <option value="price-low">Price: Low to High</option>
                <option value="price-high">Price: High to Low</option>
              </select>
            </div>
          </div>

          <!-- Property Grid -->
          <div class="property-grid">
            <PropertyCard
              v-for="property in displayedProperties"
              :key="property.id"
              :property="property"
              :location="getLocationForProperty(property)"
              :forRent="false"
              :showDescription="true"
              :showPropertyType="true"
              :showViews="false"
              @favorite-toggled="handleFavoriteToggle"
            />
          </div>
        </div>

        <!-- Load More Section -->
        <div v-if="showLoadMore" class="load-more-section">
          <div class="pagination-info">
            Showing {{ currentDisplayCount }} of {{ totalProperties }} properties
          </div>
          
          <button 
            @click="loadMore" 
            class="btn btn-primary btn-lg"
            :disabled="loading"
          >
            <span v-if="!loading">Load More Properties ({{ nextBatchCount }})</span>
            <span v-else>Loading...</span>
          </button>

          <!-- Page Numbers -->
          <div class="page-numbers">
            <button
              v-for="page in displayedPageNumbers"
              :key="page"
              @click="goToPage(page)"
              :class="['page-number-btn', { active: page === currentPage }]"
            >
              {{ page }}
            </button>
          </div>
        </div>

        <!-- No More Properties Message -->
        <div v-else-if="allPropertiesLoaded && totalProperties > 0" class="all-loaded-message">
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            width="48" 
            height="48" 
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            stroke-width="2" 
            stroke-linecap="round" 
            stroke-linejoin="round"
          >
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
            <polyline points="22 4 12 14.01 9 11.01"></polyline>
          </svg>
          <p>You've reached the end of the listings</p>
          <button @click="scrollToTop" class="btn btn-secondary">
            Back to Top
          </button>
        </div>

        <!-- Quick Links -->
        <div class="quick-links-section">
          <h2 class="section-title">Looking for something else?</h2>
          <div class="quick-links-grid">
            <RouterLink to="/rent" class="quick-link-card">
              <div class="quick-link-icon">🏠</div>
              <h3>Properties for Rent</h3>
              <p>Browse rental listings</p>
            </RouterLink>
            <RouterLink to="/seller" class="quick-link-card">
              <div class="quick-link-icon">💼</div>
              <h3>Sell Your Property</h3>
              <p>List your property with us</p>
            </RouterLink>
            <RouterLink to="/about" class="quick-link-card">
              <div class="quick-link-icon">ℹ️</div>
              <h3>Why Choose Us</h3>
              <p>Learn about our services</p>
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import HeroComponent from '../../components/common/Hero.vue';
import PropertyCard from '../../components/property/PropertyCard.vue';

export default {
  name: 'BuyView',
  components: {
    HeroComponent,
    PropertyCard
  },
  setup() {
    const route = useRoute();
    const router = useRouter();
    const propertyList = ref(null);
    const loading = ref(false);
    const currentPage = ref(1);
    const itemsPerPage = 10;
    const allProperties = ref([]);
    const displayedProperties = ref([]);
    const allLocations = ref([]);
    const sortBy = ref('newest');

    // Filters from route query params
    const filters = ref({
      location: route.query.location || '',
      propertyType: route.query.type || '',
      minPrice: route.query.minPrice || '',
      maxPrice: route.query.maxPrice || '',
      bedrooms: route.query.bedrooms || ''
    });

    // Hero stats
    const heroStats = ref([
      { value: '1,250+', label: 'Properties for Sale' },
      { value: '5,000+', label: 'Happy Homeowners' },
      { value: '500+', label: 'Expert Agents' }
    ]);

    // Computed properties
    const hasActiveFilters = computed(() => {
      return filters.value.location || 
             filters.value.propertyType || 
             filters.value.minPrice || 
             filters.value.maxPrice || 
             filters.value.bedrooms;
    });

    const totalProperties = computed(() => {
      return allProperties.value.length;
    });

    const currentDisplayCount = computed(() => {
      return Math.min(currentPage.value * itemsPerPage, totalProperties.value);
    });

    const showLoadMore = computed(() => {
      return currentDisplayCount.value < totalProperties.value;
    });

    const allPropertiesLoaded = computed(() => {
      return currentDisplayCount.value >= totalProperties.value && totalProperties.value > 0;
    });

    const nextBatchCount = computed(() => {
      const remaining = totalProperties.value - currentDisplayCount.value;
      return Math.min(itemsPerPage, remaining);
    });

    const totalPages = computed(() => {
      return Math.ceil(totalProperties.value / itemsPerPage);
    });

    const displayedPageNumbers = computed(() => {
      const pages = [];
      const maxPages = 5;
      let start = Math.max(1, currentPage.value - Math.floor(maxPages / 2));
      let end = Math.min(totalPages.value, start + maxPages - 1);
      
      if (end - start < maxPages - 1) {
        start = Math.max(1, end - maxPages + 1);
      }
      
      for (let i = start; i <= end; i++) {
        pages.push(i);
      }
      
      return pages;
    });

    // Format helpers
    const formatPropertyType = (type) => {
      if (!type) return '';
      return type.charAt(0).toUpperCase() + type.slice(1);
    };

    const formatPriceRange = (min, max) => {
      const formatPrice = (price) => {
        if (!price) return '';
        const num = parseInt(price);
        if (num >= 1000000) return `$${(num / 1000000).toFixed(1)}M`;
        if (num >= 1000) return `$${(num / 1000).toFixed(0)}k`;
        return `$${num}`;
      };

      if (min && max) {
        return `${formatPrice(min)} - ${formatPrice(max)}`;
      } else if (min) {
        return `${formatPrice(min)}+`;
      } else if (max) {
        return `Up to ${formatPrice(max)}`;
      }
      return '';
    };

    // Fetch properties
    const fetchProperties = async () => {
      loading.value = true;
      try {
        const response = await fetch('../src/example.json');
        const data = await response.json();
        
        // Store locations
        allLocations.value = data.locations || [];
        
        let properties = data.properties || [];
        
        // Filter by status (only available)
        properties = properties.filter(p => p.status === 'available');
        
        // Apply filters
        if (filters.value.propertyType) {
          properties = properties.filter(p => p.property_type === filters.value.propertyType);
        }
        
        if (filters.value.minPrice) {
          const minPrice = parseInt(filters.value.minPrice);
          properties = properties.filter(p => p.price >= minPrice);
        }
        
        if (filters.value.maxPrice) {
          const maxPrice = parseInt(filters.value.maxPrice);
          properties = properties.filter(p => p.price <= maxPrice);
        }
        
        if (filters.value.bedrooms) {
          const minBedrooms = parseInt(filters.value.bedrooms);
          properties = properties.filter(p => p.bedrooms && p.bedrooms >= minBedrooms);
        }
        
        // Note: Location filter would require more complex logic with the locations table
        // For now, we'll skip location filtering in this demo
        
        // Apply sorting
        properties = sortProperties(properties, sortBy.value);
        
        allProperties.value = properties;
        updateDisplayedProperties();
        
      } catch (error) {
        console.error('Error fetching properties:', error);
      } finally {
        loading.value = false;
      }
    };

    // Sort properties
    const sortProperties = (properties, sortType) => {
      const sorted = [...properties];
      
      switch(sortType) {
        case 'newest':
          sorted.sort((a, b) => b.id - a.id);
          break;
        case 'oldest':
          sorted.sort((a, b) => a.id - b.id);
          break;
        case 'price-low':
          sorted.sort((a, b) => a.price - b.price);
          break;
        case 'price-high':
          sorted.sort((a, b) => b.price - a.price);
          break;
        default:
          break;
      }
      
      return sorted;
    };

    // Handle sort change
    const handleSort = () => {
      allProperties.value = sortProperties(allProperties.value, sortBy.value);
      updateDisplayedProperties();
    };

    // Get location for property
    const getLocationForProperty = (property) => {
      return allLocations.value.find(loc => loc.id === property.location_id);
    };

    // Handle favorite toggle
    const handleFavoriteToggle = (propertyId) => {
      console.log('Favorite toggled for property:', propertyId);
      // In a real app, this would make an API call to save the favorite
    };

    // Update displayed properties based on current page
    const updateDisplayedProperties = () => {
      const endIndex = currentPage.value * itemsPerPage;
      displayedProperties.value = allProperties.value.slice(0, endIndex);
    };

    // Load more properties
    const loadMore = () => {
      if (currentDisplayCount.value < totalProperties.value) {
        currentPage.value++;
        updateDisplayedProperties();
        
        // Smooth scroll to new content
        setTimeout(() => {
          const propertyGrid = document.querySelector('.property-grid');
          if (propertyGrid) {
            const newItems = propertyGrid.children;
            const scrollTarget = newItems[currentDisplayCount.value - itemsPerPage];
            if (scrollTarget) {
              scrollTarget.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
          }
        }, 100);
      }
    };

    // Go to specific page
    const goToPage = (page) => {
      if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page;
        updateDisplayedProperties();
        scrollToTop();
      }
    };

    // Scroll to top
    const scrollToTop = () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    // Handle search from hero
    const handleSearch = (searchData) => {
      console.log('Search received:', searchData);
      
      // Process price range
      let minPrice = '';
      let maxPrice = '';
      if (searchData.priceRange) {
        const [min, max] = searchData.priceRange.split('-');
        minPrice = min || '';
        maxPrice = max || '';
      }
      
      filters.value = {
        location: searchData.location || '',
        propertyType: searchData.propertyType || '',
        minPrice: minPrice,
        maxPrice: maxPrice,
        bedrooms: searchData.bedrooms || ''
      };
      
      // Reset to first page and fetch
      currentPage.value = 1;
      
      // Update URL query params
      updateRouteQuery();
      
      // Fetch with new filters
      fetchProperties();
    };

    // Clear individual filter
    const clearFilter = (filterName) => {
      filters.value[filterName] = '';
      updateRouteQuery();
      currentPage.value = 1;
      fetchProperties();
    };

    // Clear price filter
    const clearPriceFilter = () => {
      filters.value.minPrice = '';
      filters.value.maxPrice = '';
      updateRouteQuery();
      currentPage.value = 1;
      fetchProperties();
    };

    // Clear all filters
    const clearAllFilters = () => {
      filters.value = {
        location: '',
        propertyType: '',
        minPrice: '',
        maxPrice: '',
        bedrooms: ''
      };
      updateRouteQuery();
      currentPage.value = 1;
      fetchProperties();
    };

    // Update route query params
    const updateRouteQuery = () => {
      const query = {};
      Object.keys(filters.value).forEach(key => {
        if (filters.value[key]) {
          query[key] = filters.value[key];
        }
      });
      
      router.push({ query });
    };

    // Watch route changes
    watch(() => route.query, (newQuery) => {
      filters.value = {
        location: newQuery.location || '',
        propertyType: newQuery.type || '',
        minPrice: newQuery.minPrice || '',
        maxPrice: newQuery.maxPrice || '',
        bedrooms: newQuery.bedrooms || ''
      };
      currentPage.value = 1;
      fetchProperties();
    });

    // Fetch on mount
    onMounted(() => {
      fetchProperties();
    });

    return {
      propertyList,
      loading,
      currentPage,
      filters,
      heroStats,
      sortBy,
      allProperties,
      allLocations,
      displayedProperties,
      hasActiveFilters,
      totalProperties,
      currentDisplayCount,
      showLoadMore,
      allPropertiesLoaded,
      nextBatchCount,
      displayedPageNumbers,
      formatPropertyType,
      formatPriceRange,
      loadMore,
      goToPage,
      scrollToTop,
      handleSearch,
      handleSort,
      getLocationForProperty,
      handleFavoriteToggle,
      clearFilter,
      clearPriceFilter,
      clearAllFilters
    };
  }
};
</script>

<style scoped>
.buy-view {
  min-height: 100vh;
}

.buy-content {
  padding: var(--spacing-3xl) 0;
}

/* Page Header */
.page-header {
  margin-bottom: var(--spacing-3xl);
}

.page-title {
  font-size: var(--font-size-4xl);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-sm);
}

.page-description {
  font-size: var(--font-size-lg);
  color: var(--color-text-secondary);
  margin-bottom: var(--spacing-lg);
}

/* Properties Section */
.properties-section {
  margin-bottom: var(--spacing-3xl);
}

/* Results Header */
.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-xl);
  padding-bottom: var(--spacing-lg);
  border-bottom: 2px solid var(--color-border);
}

.results-count {
  font-size: var(--font-size-lg);
  color: var(--color-text-secondary);
  margin: 0;
}

.results-count strong {
  color: var(--color-text-primary);
  font-weight: var(--font-weight-bold);
}

.sort-options {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.sort-options label {
  font-size: var(--font-size-base);
  color: var(--color-text-secondary);
  font-weight: var(--font-weight-medium);
}

.sort-select {
  padding: var(--spacing-sm) var(--spacing-md);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  font-size: var(--font-size-base);
  background-color: var(--color-white);
  cursor: pointer;
  transition: border-color var(--transition-base);
}

.sort-select:hover {
  border-color: var(--color-primary);
}

.sort-select:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px var(--color-primary-light);
}

/* Property Grid */
.property-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: var(--spacing-2xl);
  margin-bottom: var(--spacing-2xl);
}

/* Loading State */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-5xl);
  gap: var(--spacing-lg);
}

.loading-state p {
  font-size: var(--font-size-lg);
  color: var(--color-text-secondary);
  margin: 0;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid var(--color-primary-light);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-5xl);
  gap: var(--spacing-lg);
  text-align: center;
}

.empty-state svg {
  color: var(--color-text-tertiary);
}

.empty-state h2 {
  font-size: var(--font-size-2xl);
  color: var(--color-text-primary);
  margin: 0;
}

.empty-state p {
  font-size: var(--font-size-lg);
  color: var(--color-text-secondary);
  margin: 0;
}


/* Active Filters */
.active-filters {
  margin-top: var(--spacing-lg);
  padding: var(--spacing-lg);
  background-color: var(--color-primary-light);
  border-radius: var(--radius-lg);
  border-left: 4px solid var(--color-primary);
}

.filter-label {
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  margin-right: var(--spacing-md);
}

.filter-tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-sm);
  margin-top: var(--spacing-sm);
  align-items: center;
}

.filter-tag {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-xs) var(--spacing-md);
  background-color: var(--color-white);
  border: 1px solid var(--color-primary);
  border-radius: var(--radius-full);
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
}

.filter-remove {
  background: none;
  border: none;
  color: var(--color-text-secondary);
  font-size: var(--font-size-lg);
  line-height: 1;
  cursor: pointer;
  padding: 0;
  margin-left: var(--spacing-xs);
  transition: color var(--transition-base);
}

.filter-remove:hover {
  color: var(--color-accent);
}

/* Load More Section */
.load-more-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-lg);
  margin-top: var(--spacing-3xl);
  padding: var(--spacing-2xl);
  background-color: var(--color-cream);
  border-radius: var(--radius-xl);
}

.pagination-info {
  font-size: var(--font-size-lg);
  color: var(--color-text-secondary);
  font-weight: var(--font-weight-medium);
}

.page-numbers {
  display: flex;
  gap: var(--spacing-sm);
  flex-wrap: wrap;
  justify-content: center;
}

.page-number-btn {
  min-width: 44px;
  height: 44px;
  padding: var(--spacing-sm) var(--spacing-md);
  border: 1px solid var(--color-border);
  background-color: var(--color-white);
  color: var(--color-text-primary);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-base);
  font-weight: var(--font-weight-medium);
}

.page-number-btn:hover {
  border-color: var(--color-primary);
  background-color: var(--color-primary-light);
  color: var(--color-primary-dark);
}

.page-number-btn.active {
  background-color: var(--color-primary);
  color: var(--color-gray-900);
  border-color: var(--color-primary);
  font-weight: var(--font-weight-bold);
}

/* All Loaded Message */
.all-loaded-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-lg);
  margin-top: var(--spacing-3xl);
  padding: var(--spacing-3xl);
  text-align: center;
  background-color: var(--color-cream);
  border-radius: var(--radius-xl);
}

.all-loaded-message svg {
  color: var(--color-primary-dark);
}

.all-loaded-message p {
  font-size: var(--font-size-lg);
  color: var(--color-text-secondary);
  margin: 0;
}

/* Quick Links Section */
.quick-links-section {
  margin-top: var(--spacing-3xl);
  padding-top: var(--spacing-3xl);
  border-top: 2px solid var(--color-border);
}

.section-title {
  font-size: var(--font-size-3xl);
  color: var(--color-text-primary);
  text-align: center;
  margin-bottom: var(--spacing-2xl);
}

.quick-links-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--spacing-xl);
}

.quick-link-card {
  padding: var(--spacing-2xl);
  background-color: var(--color-white);
  border: 2px solid var(--color-border);
  border-radius: var(--radius-xl);
  text-align: center;
  text-decoration: none;
  transition: all var(--transition-base);
}

.quick-link-card:hover {
  border-color: var(--color-primary);
  box-shadow: var(--shadow-card-hover);
  transform: translateY(-4px);
  text-decoration: none;
}

.quick-link-icon {
  font-size: var(--font-size-5xl);
  margin-bottom: var(--spacing-md);
}

.quick-link-card h3 {
  font-size: var(--font-size-xl);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-sm);
}

.quick-link-card p {
  font-size: var(--font-size-base);
  color: var(--color-text-secondary);
  margin: 0;
}

/* Responsive */
@media (max-width: 768px) {
  .page-title {
    font-size: var(--font-size-3xl);
  }

  .page-description {
    font-size: var(--font-size-base);
  }

  .filter-tags {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-tag {
    justify-content: space-between;
  }

  .results-header {
    flex-direction: column;
    align-items: stretch;
    gap: var(--spacing-md);
  }

  .sort-options {
    justify-content: space-between;
  }

  .property-grid {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: var(--spacing-lg);
  }

  .quick-links-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .buy-content {
    padding: var(--spacing-2xl) 0;
  }

  .page-title {
    font-size: var(--font-size-2xl);
  }

  .section-title {
    font-size: var(--font-size-2xl);
  }

  .load-more-section {
    padding: var(--spacing-lg);
  }

  .pagination-info {
    font-size: var(--font-size-base);
  }

  .property-grid {
    grid-template-columns: 1fr;
  }
}
</style>