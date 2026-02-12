<template>
  <div class="mylist-view">
    <!-- Breadcrumb -->
    <div class="container">
      <nav class="breadcrumb">
        <RouterLink to="/seller">Dashboard</RouterLink>
        <span class="separator">›</span>
        <span class="current">My Listings</span>
      </nav>
    </div>

    <!-- Page Header -->
    <div class="page-header">
      <div class="container">
        <div class="header-content">
          <div>
            <h1 class="page-title">My Listings</h1>
            <p class="page-subtitle">Manage and track all your property listings</p>
          </div>
          <RouterLink to="/seller/add-property" class="btn btn-primary btn-lg">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"
              fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="12" y1="5" x2="12" y2="19"></line>
              <line x1="5" y1="12" x2="19" y2="12"></line>
            </svg>
            Add New Property
          </RouterLink>
        </div>
      </div>
    </div>

    <div class="container">
      <!-- Admin Check -->
      <div v-if="!isAdmin" class="access-denied">
        <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24"
          fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" y1="8" x2="12" y2="12"></line>
          <line x1="12" y1="16" x2="12.01" y2="16"></line>
        </svg>
        <h2>Access Denied</h2>
        <p>Only sellers and administrators can access this page.</p>
        <RouterLink to="/" class="btn btn-primary">Return Home</RouterLink>
      </div>

      <div v-else class="mylist-content">
        <!-- Summary Stats -->
        <div class="summary-bar">
          <div class="summary-stat">
            <span class="summary-value">{{ allProperties.length }}</span>
            <span class="summary-label">Total</span>
          </div>
          <div class="summary-divider"></div>
          <div class="summary-stat">
            <span class="summary-value available">{{ countByStatus('available') }}</span>
            <span class="summary-label">Available</span>
          </div>
          <div class="summary-divider"></div>
          <div class="summary-stat">
            <span class="summary-value pending">{{ countByStatus('pending') }}</span>
            <span class="summary-label">Pending</span>
          </div>
          <div class="summary-divider"></div>
          <div class="summary-stat">
            <span class="summary-value sold">{{ countByStatus('sold') }}</span>
            <span class="summary-label">Sold</span>
          </div>
        </div>

        <!-- Toolbar -->
        <div class="toolbar">
          <!-- Search -->
          <div class="search-wrapper">
            <svg class="search-icon" xmlns="http://www.w3.org/2000/svg" width="18" height="18"
              viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
              stroke-linecap="round" stroke-linejoin="round">
              <circle cx="11" cy="11" r="8"></circle>
              <path d="m21 21-4.35-4.35"></path>
            </svg>
            <input
              v-model="searchQuery"
              type="text"
              class="search-input"
              placeholder="Search by title, city..."
            />
            <button v-if="searchQuery" @click="searchQuery = ''" class="clear-search">×</button>
          </div>

          <!-- Filters -->
          <div class="filters">
            <select v-model="filterStatus" class="filter-select">
              <option value="">All Status</option>
              <option value="available">Available</option>
              <option value="pending">Pending</option>
              <option value="sold">Sold</option>
            </select>

            <select v-model="filterType" class="filter-select">
              <option value="">All Types</option>
              <option value="house">House</option>
              <option value="apartment">Apartment</option>
              <option value="land">Land</option>
            </select>

            <select v-model="sortBy" class="filter-select">
              <option value="newest">Newest First</option>
              <option value="oldest">Oldest First</option>
              <option value="price-high">Price: High to Low</option>
              <option value="price-low">Price: Low to High</option>
              <option value="views">Most Viewed</option>
            </select>
          </div>

          <!-- View Toggle -->
          <div class="view-toggle">
            <button
              @click="viewMode = 'table'"
              :class="['toggle-btn', { active: viewMode === 'table' }]"
              title="Table view"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24"
                fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="3" width="7" height="7"></rect>
                <rect x="14" y="3" width="7" height="7"></rect>
                <rect x="14" y="14" width="7" height="7"></rect>
                <rect x="3" y="14" width="7" height="7"></rect>
              </svg>
            </button>
            <button
              @click="viewMode = 'cards'"
              :class="['toggle-btn', { active: viewMode === 'cards' }]"
              title="Card view"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24"
                fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="8" y1="6" x2="21" y2="6"></line>
                <line x1="8" y1="12" x2="21" y2="12"></line>
                <line x1="8" y1="18" x2="21" y2="18"></line>
                <line x1="3" y1="6" x2="3.01" y2="6"></line>
                <line x1="3" y1="12" x2="3.01" y2="12"></line>
                <line x1="3" y1="18" x2="3.01" y2="18"></line>
              </svg>
            </button>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="loading-state">
          <div class="spinner"></div>
          <p>Loading your properties...</p>
        </div>

        <!-- Empty State -->
        <div v-else-if="filteredProperties.length === 0 && allProperties.length === 0" class="empty-state">
          <svg xmlns="http://www.w3.org/2000/svg" width="72" height="72" viewBox="0 0 24 24"
            fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
            <polyline points="9 22 9 12 15 12 15 22"></polyline>
          </svg>
          <h3>No Properties Yet</h3>
          <p>You haven't listed any properties. Add your first one now!</p>
          <RouterLink to="/seller/add-property" class="btn btn-primary btn-lg">
            Add Your First Property
          </RouterLink>
        </div>

        <!-- No Search Results -->
        <div v-else-if="filteredProperties.length === 0" class="empty-state">
          <svg xmlns="http://www.w3.org/2000/svg" width="72" height="72" viewBox="0 0 24 24"
            fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <path d="m21 21-4.35-4.35"></path>
          </svg>
          <h3>No Results Found</h3>
          <p>No properties match your current search or filters.</p>
          <button @click="clearFilters" class="btn btn-secondary">Clear Filters</button>
        </div>

        <!-- TABLE VIEW -->
        <div v-else-if="viewMode === 'table'" class="table-wrapper">
          <div class="results-info">
            Showing <strong>{{ filteredProperties.length }}</strong> of <strong>{{ allProperties.length }}</strong> properties
          </div>

          <table class="property-table">
            <thead>
              <tr>
                <th class="th-photo">Photo</th>
                <th class="th-title">Title</th>
                <th class="th-type">Type</th>
                <th class="th-price">Price</th>
                <th class="th-location">Location</th>
                <th class="th-details">Details</th>
                <th class="th-views">Views</th>
                <th class="th-status">Status</th>
                <th class="th-actions">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="property in paginatedProperties"
                :key="property.id"
                class="property-row"
                :class="{ 'row-sold': property.status === 'sold' }"
              >
                <!-- Photo -->
                <td class="td-photo">
                  <div class="table-photo">
                    <img
                      :src="property.photo_location?.[0] || 'https://placehold.co/80x60?text=No+Photo'"
                      :alt="property.title"
                      @error="handleImageError"
                    />
                  </div>
                </td>

                <!-- Title -->
                <td class="td-title">
                  <p class="property-title-text">{{ property.title }}</p>
                  <span class="property-id">ID #{{ property.id }}</span>
                </td>

                <!-- Type -->
                <td class="td-type">
                  <span class="type-badge" :class="property.property_type">
                    {{ formatType(property.property_type) }}
                  </span>
                </td>

                <!-- Price -->
                <td class="td-price">
                  <span class="price-text">{{ formatPrice(property.price) }}</span>
                </td>

                <!-- Location -->
                <td class="td-location">
                  <div class="location-cell" v-if="getLocation(property.location_id)">
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24"
                      fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                      <circle cx="12" cy="10" r="3"></circle>
                    </svg>
                    <span>{{ getLocation(property.location_id)?.city }}, {{ getLocation(property.location_id)?.country }}</span>
                  </div>
                  <span v-else class="no-location">—</span>
                </td>

                <!-- Details -->
                <td class="td-details">
                  <div class="details-mini">
                    <span v-if="property.bedrooms">🛏 {{ property.bedrooms }}</span>
                    <span v-if="property.bathrooms">🚿 {{ property.bathrooms }}</span>
                    <span v-if="property.area_sqm">📐 {{ property.area_sqm }}m²</span>
                  </div>
                </td>

                <!-- Views -->
                <td class="td-views">
                  <div class="views-cell">
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24"
                      fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                      <circle cx="12" cy="12" r="3"></circle>
                    </svg>
                    {{ property.views_count || 0 }}
                  </div>
                </td>

                <!-- Status (inline editable) -->
                <td class="td-status">
                  <select
                    :value="property.status"
                    @change="updateStatus(property, $event.target.value)"
                    class="status-select"
                    :class="property.status"
                  >
                    <option value="available">Available</option>
                    <option value="pending">Pending</option>
                    <option value="sold">Sold</option>
                  </select>
                </td>

                <!-- Actions -->
                <td class="td-actions">
                  <div class="action-buttons">
                    <RouterLink
                      :to="`/properties/${property.id}`"
                      class="action-btn view-btn"
                      title="View listing"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"
                        fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                        <circle cx="12" cy="12" r="3"></circle>
                      </svg>
                    </RouterLink>
                    <RouterLink
                      :to="`/seller/edit-property/${property.id}`"
                      class="action-btn edit-btn"
                      title="Edit listing"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"
                        fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                        <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                      </svg>
                    </RouterLink>
                    <button
                      @click="confirmDelete(property)"
                      class="action-btn delete-btn"
                      title="Delete listing"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"
                        fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="3 6 5 6 21 6"></polyline>
                        <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"></path>
                        <path d="M10 11v6"></path>
                        <path d="M14 11v6"></path>
                        <path d="M9 6V4h6v2"></path>
                      </svg>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- CARD VIEW -->
        <div v-else class="cards-view">
          <div class="results-info">
            Showing <strong>{{ filteredProperties.length }}</strong> of <strong>{{ allProperties.length }}</strong> properties
          </div>
          <div class="cards-grid">
            <div
              v-for="property in paginatedProperties"
              :key="property.id"
              class="listing-card"
              :class="{ 'card-sold': property.status === 'sold' }"
            >
              <!-- Card Image -->
              <div class="card-image-wrapper">
                <img
                  :src="property.photo_location?.[0] || 'https://placehold.co/400x220?text=No+Photo'"
                  :alt="property.title"
                  class="card-image"
                  @error="handleImageError"
                />
                <div class="card-photo-count" v-if="property.photo_location?.length > 1">
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24"
                    fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                    <circle cx="8.5" cy="8.5" r="1.5"></circle>
                    <polyline points="21 15 16 10 5 21"></polyline>
                  </svg>
                  {{ property.photo_location.length }}
                </div>
                <span class="card-id">ID #{{ property.id }}</span>
              </div>

              <!-- Card Body -->
              <div class="card-body">
                <div class="card-title-row">
                  <h3 class="card-title">{{ property.title }}</h3>
                  <span class="type-badge" :class="property.property_type">
                    {{ formatType(property.property_type) }}
                  </span>
                </div>

                <p class="card-price">{{ formatPrice(property.price) }}</p>

                <div class="card-location" v-if="getLocation(property.location_id)">
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24"
                    fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                    <circle cx="12" cy="10" r="3"></circle>
                  </svg>
                  {{ getLocation(property.location_id)?.city }}, {{ getLocation(property.location_id)?.country }}
                </div>

                <div class="card-details">
                  <span v-if="property.bedrooms">🛏 {{ property.bedrooms }} Beds</span>
                  <span v-if="property.bathrooms">🚿 {{ property.bathrooms }} Baths</span>
                  <span v-if="property.area_sqm">📐 {{ property.area_sqm }} m²</span>
                </div>

                <div class="card-meta">
                  <div class="card-views">
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24"
                      fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                      <circle cx="12" cy="12" r="3"></circle>
                    </svg>
                    {{ property.views_count || 0 }} views
                  </div>
                  <span class="card-date">{{ formatDate(property.created_at) }}</span>
                </div>
              </div>

              <!-- Card Footer -->
              <div class="card-footer">
                <select
                  :value="property.status"
                  @change="updateStatus(property, $event.target.value)"
                  class="status-select"
                  :class="property.status"
                >
                  <option value="available">Available</option>
                  <option value="pending">Pending</option>
                  <option value="sold">Sold</option>
                </select>

                <div class="card-actions">
                  <RouterLink :to="`/properties/${property.id}`" class="action-btn view-btn" title="View">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"
                      fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                      <circle cx="12" cy="12" r="3"></circle>
                    </svg>
                  </RouterLink>
                  <RouterLink :to="`/seller/edit-property/${property.id}`" class="action-btn edit-btn" title="Edit">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"
                      fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                      <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                    </svg>
                  </RouterLink>
                  <button @click="confirmDelete(property)" class="action-btn delete-btn" title="Delete">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"
                      fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <polyline points="3 6 5 6 21 6"></polyline>
                      <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"></path>
                      <path d="M10 11v6"></path>
                      <path d="M14 11v6"></path>
                      <path d="M9 6V4h6v2"></path>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="pagination">
          <button
            @click="currentPage--"
            :disabled="currentPage === 1"
            class="page-btn"
          >
            ‹ Prev
          </button>

          <button
            v-for="page in pageNumbers"
            :key="page"
            @click="currentPage = page"
            :class="['page-btn', { active: page === currentPage }]"
          >
            {{ page }}
          </button>

          <button
            @click="currentPage++"
            :disabled="currentPage === totalPages"
            class="page-btn"
          >
            Next ›
          </button>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <Transition name="modal">
      <div v-if="deleteModal.show" class="modal-overlay" @click.self="deleteModal.show = false">
        <div class="modal">
          <div class="modal-icon danger">
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24"
              fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="3 6 5 6 21 6"></polyline>
              <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"></path>
              <path d="M10 11v6"></path>
              <path d="M14 11v6"></path>
              <path d="M9 6V4h6v2"></path>
            </svg>
          </div>
          <h3 class="modal-title">Delete Property?</h3>
          <p class="modal-body">
            Are you sure you want to delete <strong>"{{ deleteModal.property?.title }}"</strong>?
            This action cannot be undone.
          </p>
          <div class="modal-actions">
            <button @click="deleteModal.show = false" class="btn btn-secondary">
              Cancel
            </button>
            <button @click="deleteProperty" class="btn btn-danger" :disabled="deleteModal.loading">
              <span v-if="!deleteModal.loading">Delete Property</span>
              <span v-else>Deleting...</span>
            </button>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Status Update Toast -->
    <Transition name="toast">
      <div v-if="toast.show" class="toast" :class="toast.type">
        <svg v-if="toast.type === 'success'" xmlns="http://www.w3.org/2000/svg" width="20" height="20"
          viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
          stroke-linecap="round" stroke-linejoin="round">
          <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
          <polyline points="22 4 12 14.01 9 11.01"></polyline>
        </svg>
        <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20"
          viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
          stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" y1="8" x2="12" y2="12"></line>
          <line x1="12" y1="16" x2="12.01" y2="16"></line>
        </svg>
        <span>{{ toast.message }}</span>
      </div>
    </Transition>
  </div>
</template>

<script>
import { ref, computed, reactive, onMounted } from 'vue';

export default {
  name: 'MyListingsView',
  setup() {
    // For testing, admin is always true
    const isAdmin = ref(true); // TODO: Replace with real auth

    const loading = ref(true);
    const allProperties = ref([]);
    const allLocations = ref([]);

    // Toolbar state
    const searchQuery = ref('');
    const filterStatus = ref('');
    const filterType = ref('');
    const sortBy = ref('newest');
    const viewMode = ref('table');

    // Pagination
    const currentPage = ref(1);
    const itemsPerPage = 10;

    // Delete modal
    const deleteModal = reactive({
      show: false,
      property: null,
      loading: false
    });

    // Toast notification
    const toast = reactive({
      show: false,
      message: '',
      type: 'success',
      timer: null
    });

    // ── Computed ───────────────────────────────────────────────

    const filteredProperties = computed(() => {
      let result = [...allProperties.value];

      // Search
      if (searchQuery.value.trim()) {
        const q = searchQuery.value.toLowerCase();
        result = result.filter(p => {
          const location = getLocation(p.location_id);
          return (
            p.title?.toLowerCase().includes(q) ||
            location?.city?.toLowerCase().includes(q) ||
            location?.country?.toLowerCase().includes(q)
          );
        });
      }

      // Status filter
      if (filterStatus.value) {
        result = result.filter(p => p.status === filterStatus.value);
      }

      // Type filter
      if (filterType.value) {
        result = result.filter(p => p.property_type === filterType.value);
      }

      // Sorting
      switch (sortBy.value) {
        case 'newest':
          result.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
          break;
        case 'oldest':
          result.sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
          break;
        case 'price-high':
          result.sort((a, b) => b.price - a.price);
          break;
        case 'price-low':
          result.sort((a, b) => a.price - b.price);
          break;
        case 'views':
          result.sort((a, b) => (b.views_count || 0) - (a.views_count || 0));
          break;
      }

      return result;
    });

    const totalPages = computed(() =>
      Math.ceil(filteredProperties.value.length / itemsPerPage)
    );

    const paginatedProperties = computed(() => {
      const start = (currentPage.value - 1) * itemsPerPage;
      return filteredProperties.value.slice(start, start + itemsPerPage);
    });

    const pageNumbers = computed(() => {
      const pages = [];
      const max = 5;
      let start = Math.max(1, currentPage.value - Math.floor(max / 2));
      let end = Math.min(totalPages.value, start + max - 1);
      if (end - start < max - 1) start = Math.max(1, end - max + 1);
      for (let i = start; i <= end; i++) pages.push(i);
      return pages;
    });

    // ── Helpers ───────────────────────────────────────────────

    const getLocation = (locationId) =>
      allLocations.value.find(l => l.id === locationId) || null;

    const formatPrice = (price) => {
      if (!price) return '—';
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        maximumFractionDigits: 0
      }).format(price);
    };

    const formatType = (type) => {
      if (!type) return '—';
      return type.charAt(0).toUpperCase() + type.slice(1);
    };

    const formatDate = (dateStr) => {
      if (!dateStr) return '—';
      return new Date(dateStr).toLocaleDateString('en-US', {
        year: 'numeric', month: 'short', day: 'numeric'
      });
    };

    const countByStatus = (status) =>
      allProperties.value.filter(p => p.status === status).length;

    const handleImageError = (event) => {
      event.target.src = 'https://placehold.co/80x60?text=No+Photo';
    };

    const clearFilters = () => {
      searchQuery.value = '';
      filterStatus.value = '';
      filterType.value = '';
      sortBy.value = 'newest';
      currentPage.value = 1;
    };

    // ── Toast ─────────────────────────────────────────────────

    const showToast = (message, type = 'success') => {
      if (toast.timer) clearTimeout(toast.timer);
      toast.message = message;
      toast.type = type;
      toast.show = true;
      toast.timer = setTimeout(() => { toast.show = false; }, 3000);
    };

    // ── Status update ─────────────────────────────────────────

    const updateStatus = async (property, newStatus) => {
      const oldStatus = property.status;
      property.status = newStatus;

      try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 500));
        // In real app: await fetch(`/api/properties/${property.id}`, { method: 'PATCH', body: JSON.stringify({ status: newStatus }) })
        showToast(`Status updated to "${newStatus}"`);
      } catch {
        property.status = oldStatus; // rollback
        showToast('Failed to update status. Please try again.', 'error');
      }
    };

    // ── Delete ────────────────────────────────────────────────

    const confirmDelete = (property) => {
      deleteModal.property = property;
      deleteModal.show = true;
    };

    const deleteProperty = async () => {
      deleteModal.loading = true;
      try {
        await new Promise(resolve => setTimeout(resolve, 800));
        // In real app: await fetch(`/api/properties/${deleteModal.property.id}`, { method: 'DELETE' })

        allProperties.value = allProperties.value.filter(
          p => p.id !== deleteModal.property.id
        );

        showToast(`"${deleteModal.property.title}" has been deleted`);
        deleteModal.show = false;
        deleteModal.property = null;

        // Reset to first page if current page is now empty
        if (paginatedProperties.value.length === 0 && currentPage.value > 1) {
          currentPage.value--;
        }
      } catch {
        showToast('Failed to delete property. Please try again.', 'error');
      } finally {
        deleteModal.loading = false;
      }
    };

    // ── Fetch data ────────────────────────────────────────────

    const fetchData = async () => {
      loading.value = true;
      try {
        const res = await fetch('/example.json');
        const data = await res.json();
        allLocations.value = data.locations || [];

        // Filter to only show this seller's properties (owner_id: 1 for testing)
        allProperties.value = (data.properties || []).filter(p => p.owner_id === 1);
      } catch (err) {
        console.error('Error fetching listings:', err);
        showToast('Failed to load listings. Please refresh.', 'error');
      } finally {
        loading.value = false;
      }
    };

    onMounted(fetchData);

    return {
      isAdmin,
      loading,
      allProperties,
      allLocations,
      searchQuery,
      filterStatus,
      filterType,
      sortBy,
      viewMode,
      currentPage,
      filteredProperties,
      paginatedProperties,
      totalPages,
      pageNumbers,
      deleteModal,
      toast,
      getLocation,
      formatPrice,
      formatType,
      formatDate,
      countByStatus,
      handleImageError,
      clearFilters,
      updateStatus,
      confirmDelete,
      deleteProperty
    };
  }
};
</script>

<style scoped>
/* ── Base ──────────────────────────────────────────────────── */
.mylist-view {
  min-height: 100vh;
  background-color: var(--color-background);
  padding-bottom: var(--spacing-5xl);
}

/* Breadcrumb */
.breadcrumb {
  padding: var(--spacing-lg) 0;
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-size: var(--font-size-sm);
}
.breadcrumb a {
  color: var(--color-primary-dark);
  text-decoration: none;
  transition: color var(--transition-base);
}
.breadcrumb a:hover { color: var(--color-primary); text-decoration: underline; }
.breadcrumb .separator { color: var(--color-text-tertiary); }
.breadcrumb .current { color: var(--color-text-secondary); }

/* Page Header */
.page-header {
  background: linear-gradient(135deg, var(--color-primary-dark) 0%, var(--color-primary) 100%);
  padding: var(--spacing-2xl) 0;
  margin-bottom: var(--spacing-3xl);
}
.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--spacing-lg);
}
.page-title {
  font-size: var(--font-size-4xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-white);
  margin-bottom: var(--spacing-xs);
  text-shadow: 2px 2px 8px rgba(0,0,0,.2);
}
.page-subtitle {
  font-size: var(--font-size-base);
  color: var(--color-white);
  opacity: .9;
  margin: 0;
}
.page-header .btn-primary {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  white-space: nowrap;
}

/* Access Denied */
.access-denied {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-5xl);
  text-align: center;
  background: var(--color-white);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-card);
}
.access-denied svg { color: var(--color-accent); }
.access-denied h2 { font-size: var(--font-size-3xl); color: var(--color-text-primary); }
.access-denied p { font-size: var(--font-size-lg); color: var(--color-text-secondary); margin: 0; }

/* Summary Bar */
.summary-bar {
  display: flex;
  align-items: center;
  gap: var(--spacing-xl);
  background: var(--color-white);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-card);
  padding: var(--spacing-lg) var(--spacing-2xl);
  margin-bottom: var(--spacing-2xl);
}
.summary-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 60px;
}
.summary-value {
  font-size: var(--font-size-3xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-text-primary);
  line-height: 1;
}
.summary-value.available { color: #388e3c; }
.summary-value.pending   { color: #f57c00; }
.summary-value.sold      { color: var(--color-accent); }
.summary-label {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  margin-top: var(--spacing-xs);
}
.summary-divider {
  width: 1px;
  height: 40px;
  background-color: var(--color-border);
}

/* Toolbar */
.toolbar {
  display: flex;
  align-items: center;
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-xl);
  flex-wrap: wrap;
}
.search-wrapper {
  position: relative;
  flex: 1;
  min-width: 200px;
}
.search-icon {
  position: absolute;
  left: var(--spacing-md);
  top: 50%;
  transform: translateY(-50%);
  color: var(--color-text-tertiary);
  pointer-events: none;
}
.search-input {
  width: 100%;
  padding: var(--spacing-md) var(--spacing-md) var(--spacing-md) 44px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  font-size: var(--font-size-base);
  background: var(--color-white);
  transition: all var(--transition-base);
}
.search-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px var(--color-primary-light);
}
.clear-search {
  position: absolute;
  right: var(--spacing-md);
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  font-size: var(--font-size-xl);
  color: var(--color-text-tertiary);
  cursor: pointer;
  line-height: 1;
  padding: 0;
}
.clear-search:hover { color: var(--color-accent); }

.filters {
  display: flex;
  gap: var(--spacing-md);
  flex-wrap: wrap;
}
.filter-select {
  padding: var(--spacing-md) var(--spacing-lg);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
  background: var(--color-white);
  cursor: pointer;
  transition: border-color var(--transition-base);
}
.filter-select:focus {
  outline: none;
  border-color: var(--color-primary);
}

/* View Toggle */
.view-toggle {
  display: flex;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  overflow: hidden;
}
.toggle-btn {
  padding: var(--spacing-sm) var(--spacing-md);
  background: var(--color-white);
  border: none;
  cursor: pointer;
  color: var(--color-text-secondary);
  transition: all var(--transition-base);
  display: flex;
  align-items: center;
}
.toggle-btn:hover { background: var(--color-cream); color: var(--color-text-primary); }
.toggle-btn.active { background: var(--color-primary); color: var(--color-gray-900); }

/* Results Info */
.results-info {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  margin-bottom: var(--spacing-lg);
}
.results-info strong { color: var(--color-text-primary); }

/* Loading */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-lg);
  padding: var(--spacing-5xl);
}
.loading-state p { font-size: var(--font-size-lg); color: var(--color-text-secondary); margin: 0; }
.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid var(--color-primary-light);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-lg);
  padding: var(--spacing-5xl);
  text-align: center;
  background: var(--color-white);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-card);
}
.empty-state svg { color: var(--color-text-tertiary); }
.empty-state h3 { font-size: var(--font-size-2xl); color: var(--color-text-primary); margin: 0; }
.empty-state p { font-size: var(--font-size-lg); color: var(--color-text-secondary); margin: 0; }

/* ── TABLE ─────────────────────────────────────────────────── */
.table-wrapper {
  background: var(--color-white);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-card);
  overflow-x: auto;
}
.property-table {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--font-size-sm);
}
.property-table th {
  background: var(--color-cream);
  padding: var(--spacing-lg) var(--spacing-md);
  text-align: left;
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-secondary);
  font-size: var(--font-size-xs);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  white-space: nowrap;
  border-bottom: 2px solid var(--color-border);
}
.property-table th:first-child { border-radius: var(--radius-xl) 0 0 0; }
.property-table th:last-child  { border-radius: 0 var(--radius-xl) 0 0; }

.property-row {
  border-bottom: 1px solid var(--color-border);
  transition: background-color var(--transition-base);
}
.property-row:last-child { border-bottom: none; }
.property-row:hover { background-color: var(--color-cream); }
.property-row.row-sold { opacity: 0.65; }

.property-table td {
  padding: var(--spacing-lg) var(--spacing-md);
  vertical-align: middle;
}

/* Table cells */
.table-photo {
  width: 80px;
  height: 60px;
  border-radius: var(--radius-sm);
  overflow: hidden;
  flex-shrink: 0;
}
.table-photo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.property-title-text {
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-xs) 0;
  max-width: 220px;
}
.property-id {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
}
.price-text {
  font-weight: var(--font-weight-bold);
  color: var(--color-text-primary);
  white-space: nowrap;
}
.location-cell {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  color: var(--color-text-secondary);
  max-width: 160px;
}
.no-location { color: var(--color-text-tertiary); }
.details-mini {
  display: flex;
  flex-direction: column;
  gap: 2px;
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
}
.views-cell {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  color: var(--color-text-secondary);
  white-space: nowrap;
}

/* Status Select */
.status-select {
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius-full);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  border: 2px solid transparent;
  cursor: pointer;
  appearance: auto;
  transition: all var(--transition-base);
}
.status-select.available {
  background: #e8f5e9;
  color: #2e7d32;
  border-color: #a5d6a7;
}
.status-select.pending {
  background: #fff3e0;
  color: #e65100;
  border-color: #ffcc02;
}
.status-select.sold {
  background: #fce4ec;
  color: #880e4f;
  border-color: #f48fb1;
}

/* Action Buttons */
.action-buttons, .card-actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}
.action-btn {
  width: 34px;
  height: 34px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  cursor: pointer;
  text-decoration: none;
  transition: all var(--transition-base);
}
.view-btn { background: #e3f2fd; color: #1976d2; }
.view-btn:hover { background: #1976d2; color: var(--color-white); }
.edit-btn { background: var(--color-primary-light); color: var(--color-primary-dark); }
.edit-btn:hover { background: var(--color-primary); color: var(--color-gray-900); }
.delete-btn { background: #fce4ec; color: #c62828; }
.delete-btn:hover { background: #c62828; color: var(--color-white); }

/* ── CARDS VIEW ────────────────────────────────────────────── */
.cards-view { /* intentionally no extra wrapper styles */ }
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(310px, 1fr));
  gap: var(--spacing-xl);
}
.listing-card {
  background: var(--color-white);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-card);
  overflow: hidden;
  transition: all var(--transition-base);
  border: 2px solid transparent;
  display: flex;
  flex-direction: column;
}
.listing-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-card-hover);
  border-color: var(--color-primary);
}
.listing-card.card-sold { opacity: 0.65; }

.card-image-wrapper {
  position: relative;
  height: 200px;
  overflow: hidden;
}
.card-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}
.listing-card:hover .card-image { transform: scale(1.04); }

.card-photo-count {
  position: absolute;
  bottom: var(--spacing-sm);
  right: var(--spacing-sm);
  background: rgba(0,0,0,.55);
  color: var(--color-white);
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--radius-sm);
  font-size: var(--font-size-xs);
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
}
.card-id {
  position: absolute;
  top: var(--spacing-sm);
  left: var(--spacing-sm);
  background: rgba(0,0,0,.45);
  color: var(--color-white);
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--radius-sm);
  font-size: var(--font-size-xs);
}

.card-body {
  padding: var(--spacing-lg);
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}
.card-title-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--spacing-sm);
}
.card-title {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  margin: 0;
  flex: 1;
}
.card-price {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-text-primary);
  margin: 0;
}
.card-location {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}
.card-details {
  display: flex;
  gap: var(--spacing-md);
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  flex-wrap: wrap;
}
.card-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
}
.card-views {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}
.card-date {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
}

.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-md) var(--spacing-lg);
  border-top: 1px solid var(--color-border);
  background: var(--color-cream);
}

/* Type Badge */
.type-badge {
  padding: var(--spacing-xs) var(--spacing-md);
  border-radius: var(--radius-full);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  white-space: nowrap;
}
.type-badge.house     { background: #e8eaf6; color: #3949ab; }
.type-badge.apartment { background: #e0f7fa; color: #00838f; }
.type-badge.land      { background: #f1f8e9; color: #558b2f; }

/* Pagination */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: var(--spacing-sm);
  margin-top: var(--spacing-3xl);
  flex-wrap: wrap;
}
.page-btn {
  min-width: 42px;
  height: 42px;
  padding: 0 var(--spacing-md);
  border: 1px solid var(--color-border);
  background: var(--color-white);
  color: var(--color-text-primary);
  border-radius: var(--radius-md);
  cursor: pointer;
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  transition: all var(--transition-base);
}
.page-btn:hover:not(:disabled) {
  border-color: var(--color-primary);
  background: var(--color-primary-light);
}
.page-btn.active {
  background: var(--color-primary);
  border-color: var(--color-primary);
  color: var(--color-gray-900);
  font-weight: var(--font-weight-bold);
}
.page-btn:disabled { opacity: 0.4; cursor: not-allowed; }

/* ── Modal ─────────────────────────────────────────────────── */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: var(--spacing-lg);
}
.modal {
  background: var(--color-white);
  border-radius: var(--radius-xl);
  padding: var(--spacing-3xl);
  max-width: 460px;
  width: 100%;
  text-align: center;
  box-shadow: 0 20px 60px rgba(0,0,0,.3);
}
.modal-icon {
  width: 72px;
  height: 72px;
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto var(--spacing-xl);
}
.modal-icon.danger { background: #fce4ec; color: #c62828; }
.modal-title {
  font-size: var(--font-size-2xl);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-md);
}
.modal-body {
  font-size: var(--font-size-base);
  color: var(--color-text-secondary);
  margin-bottom: var(--spacing-2xl);
  line-height: 1.6;
}
.modal-actions {
  display: flex;
  gap: var(--spacing-md);
  justify-content: center;
}

.btn-danger {
  background-color: #c62828;
  color: var(--color-white);
  border: none;
  padding: var(--spacing-md) var(--spacing-2xl);
  border-radius: var(--radius-md);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-semibold);
  cursor: pointer;
  transition: background-color var(--transition-base);
}
.btn-danger:hover { background-color: #b71c1c; }
.btn-danger:disabled { opacity: .6; cursor: not-allowed; }

/* Modal Transition */
.modal-enter-active, .modal-leave-active { transition: opacity 0.2s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
.modal-enter-active .modal, .modal-leave-active .modal { transition: transform 0.2s ease; }
.modal-enter-from .modal { transform: scale(0.92); }
.modal-leave-to .modal   { transform: scale(0.92); }

/* ── Toast ─────────────────────────────────────────────────── */
.toast {
  position: fixed;
  bottom: var(--spacing-2xl);
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md) var(--spacing-2xl);
  border-radius: var(--radius-full);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  box-shadow: 0 8px 32px rgba(0,0,0,.18);
  z-index: 2000;
  white-space: nowrap;
}
.toast.success { background: #2e7d32; color: var(--color-white); }
.toast.error   { background: #c62828; color: var(--color-white); }

/* Toast Transition */
.toast-enter-active { transition: all 0.3s ease; }
.toast-leave-active { transition: all 0.3s ease; }
.toast-enter-from, .toast-leave-to { opacity: 0; transform: translateX(-50%) translateY(20px); }

/* ── Responsive ────────────────────────────────────────────── */
@media (max-width: 1024px) {
  .th-details, .td-details { display: none; }
}

@media (max-width: 768px) {
  .page-title { font-size: var(--font-size-2xl); }
  .header-content { flex-direction: column; align-items: flex-start; }
  .page-header .btn-primary { width: 100%; justify-content: center; }

  .toolbar { flex-direction: column; align-items: stretch; }
  .filters { flex-direction: column; }
  .filter-select { width: 100%; }

  .summary-bar { flex-wrap: wrap; gap: var(--spacing-lg); justify-content: center; }
  .summary-divider { display: none; }

  /* Hide some table columns on mobile */
  .th-views, .td-views,
  .th-location, .td-location { display: none; }

  .cards-grid { grid-template-columns: 1fr; }
}

@media (max-width: 480px) {
  /* On very small screens, switch to card view automatically */
  .table-wrapper { display: none; }
  .cards-grid { display: grid; }
  .view-toggle { display: none; }
}
</style>