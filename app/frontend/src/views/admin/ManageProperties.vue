<template>
  <div class="manage-properties-view">

    <!-- Breadcrumb -->
    <div class="container">
      <nav class="breadcrumb">
        <RouterLink to="/admin">Admin Dashboard</RouterLink>
        <span class="separator">›</span>
        <span class="current">Manage Properties</span>
      </nav>
    </div>

    <!-- Page Header -->
    <div class="page-header">
      <div class="container">
        <div class="header-content">
          <div>
            <h1 class="page-title">Manage Properties</h1>
            <p class="page-subtitle">View, edit, and moderate all property listings platform-wide</p>
          </div>
          <RouterLink to="/seller/add" class="btn btn-primary">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24"
              fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="12" y1="5" x2="12" y2="19"></line>
              <line x1="5" y1="12" x2="19" y2="12"></line>
            </svg>
            Add Property
          </RouterLink>
        </div>
      </div>
    </div>

    <div class="container">

      <!-- Access Denied -->
      <div v-if="!isAdmin" class="access-denied">
        <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24"
          fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" y1="8" x2="12" y2="12"></line>
          <line x1="12" y1="16" x2="12.01" y2="16"></line>
        </svg>
        <h2>Access Denied</h2>
        <p>Only administrators can access this page.</p>
        <RouterLink to="/" class="btn btn-primary">Return Home</RouterLink>
      </div>

      <!-- Main Content -->
      <div v-else>

        <!-- Summary Bar -->
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
            <span class="summary-label">Sold / Rented</span>
          </div>
          <div class="summary-divider"></div>
          <div class="summary-stat">
            <span class="summary-value">{{ totalViews.toLocaleString() }}</span>
            <span class="summary-label">Total Views</span>
          </div>
        </div>

        <!-- Toolbar -->
        <div class="toolbar">
          <!-- Search -->
          <div class="search-wrapper">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"
              fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
              class="search-icon">
              <circle cx="11" cy="11" r="8"></circle>
              <path d="m21 21-4.35-4.35"></path>
            </svg>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search by title, location, owner…"
              class="search-input"
              @input="currentPage = 1"
            />
            <button v-if="searchQuery" @click="searchQuery = ''; currentPage = 1" class="clear-search">✕</button>
          </div>

          <!-- Filters -->
          <div class="filters">
            <select v-model="filterStatus" class="filter-select" @change="currentPage = 1">
              <option value="">All Statuses</option>
              <option value="available">Available</option>
              <option value="pending">Pending</option>
              <option value="sold">Sold</option>
              <option value="rented">Rented</option>
            </select>

            <select v-model="filterType" class="filter-select" @change="currentPage = 1">
              <option value="">All Types</option>
              <option value="house">House</option>
              <option value="apartment">Apartment</option>
              <option value="land">Land</option>
            </select>

            <select v-model="sortBy" class="filter-select" @change="currentPage = 1">
              <option value="newest">Newest First</option>
              <option value="oldest">Oldest First</option>
              <option value="price-high">Price: High → Low</option>
              <option value="price-low">Price: Low → High</option>
              <option value="views">Most Viewed</option>
            </select>
          </div>

          <!-- View Toggle -->
          <div class="view-toggle">
            <button :class="['toggle-btn', { active: viewMode === 'table' }]" @click="viewMode = 'table'" title="Table view">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"
                fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect>
                <rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect>
              </svg>
            </button>
            <button :class="['toggle-btn', { active: viewMode === 'cards' }]" @click="viewMode = 'cards'" title="Card view">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"
                fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="8" y1="6" x2="21" y2="6"></line><line x1="8" y1="12" x2="21" y2="12"></line>
                <line x1="8" y1="18" x2="21" y2="18"></line><line x1="3" y1="6" x2="3.01" y2="6"></line>
                <line x1="3" y1="12" x2="3.01" y2="12"></line><line x1="3" y1="18" x2="3.01" y2="18"></line>
              </svg>
            </button>
          </div>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="loading-state">
          <div class="spinner"></div>
          <p>Loading properties…</p>
        </div>

        <!-- Empty (no data at all) -->
        <div v-else-if="allProperties.length === 0" class="empty-state">
          <svg xmlns="http://www.w3.org/2000/svg" width="72" height="72" viewBox="0 0 24 24"
            fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
            <polyline points="9 22 9 12 15 12 15 22"></polyline>
          </svg>
          <h3>No Properties Found</h3>
          <p>There are no properties listed on the platform yet.</p>
        </div>

        <!-- No Filter Results -->
        <div v-else-if="filteredProperties.length === 0" class="empty-state">
          <svg xmlns="http://www.w3.org/2000/svg" width="72" height="72" viewBox="0 0 24 24"
            fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle><path d="m21 21-4.35-4.35"></path>
          </svg>
          <h3>No Results Found</h3>
          <p>No properties match your current filters.</p>
          <button @click="clearFilters" class="btn btn-secondary">Clear Filters</button>
        </div>

        <!-- TABLE VIEW -->
        <div v-else-if="viewMode === 'table'" class="table-wrapper">
          <div class="results-info">
            Showing <strong>{{ paginatedProperties.length }}</strong> of <strong>{{ filteredProperties.length }}</strong> properties
          </div>

          <table class="property-table">
            <thead>
              <tr>
                <th class="th-photo">Photo</th>
                <th class="th-title">Title / ID</th>
                <th class="th-owner">Owner</th>
                <th class="th-type">Type</th>
                <th class="th-price">Price</th>
                <th class="th-location th-hide-md">Location</th>
                <th class="th-views th-hide-lg">Views</th>
                <th class="th-status">Status</th>
                <th class="th-actions">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="property in paginatedProperties"
                :key="property.id"
                class="property-row"
                :class="{ 'row-sold': property.status === 'sold' || property.status === 'rented' }"
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
                <td>
                  <p class="property-title-text">{{ property.title }}</p>
                  <span class="property-id">#{{ property.id }}</span>
                </td>

                <!-- Owner -->
                <td>
                  <span class="owner-badge">Owner #{{ property.owner_id }}</span>
                </td>

                <!-- Type -->
                <td>
                  <span :class="['type-badge', property.property_type]">
                    {{ formatType(property.property_type) }}
                  </span>
                </td>

                <!-- Price -->
                <td>
                  <span class="price-text">{{ formatPrice(property.price) }}</span>
                </td>

                <!-- Location -->
                <td class="td-hide-md">
                  <div class="location-cell" v-if="getLocation(property.location_id)">
                    <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24"
                      fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                      <circle cx="12" cy="10" r="3"></circle>
                    </svg>
                    {{ getLocation(property.location_id)?.city }}, {{ getLocation(property.location_id)?.country }}
                  </div>
                  <span v-else class="no-location">—</span>
                </td>

                <!-- Views -->
                <td class="td-hide-lg">
                  <div class="views-cell">
                    <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24"
                      fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                      <circle cx="12" cy="12" r="3"></circle>
                    </svg>
                    {{ property.views_count?.toLocaleString() ?? 0 }}
                  </div>
                </td>

                <!-- Status -->
                <td>
                  <select
                    :value="property.status"
                    @change="updateStatus(property, $event.target.value)"
                    :class="['status-select', `status-${property.status}`]"
                  >
                    <option value="available">Available</option>
                    <option value="pending">Pending</option>
                    <option value="sold">Sold</option>
                    <option value="rented">Rented</option>
                  </select>
                </td>

                <!-- Actions -->
                <td>
                  <div class="action-buttons">
                    <RouterLink :to="`/property/${property.id}`" class="action-btn view-btn" title="View listing">
                      <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24"
                        fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                        <circle cx="12" cy="12" r="3"></circle>
                      </svg>
                    </RouterLink>
                    <RouterLink :to="`/seller/edit/${property.id}`" class="action-btn edit-btn" title="Edit listing">
                      <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24"
                        fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                        <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                      </svg>
                    </RouterLink>
                    <button @click="confirmDelete(property)" class="action-btn delete-btn" title="Delete listing">
                      <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24"
                        fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="3 6 5 6 21 6"></polyline>
                        <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"></path>
                        <path d="M10 11v6"></path><path d="M14 11v6"></path>
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
            Showing <strong>{{ paginatedProperties.length }}</strong> of <strong>{{ filteredProperties.length }}</strong> properties
          </div>
          <div class="cards-grid">
            <div
              v-for="property in paginatedProperties"
              :key="property.id"
              class="listing-card"
              :class="{ 'card-sold': property.status === 'sold' || property.status === 'rented' }"
            >
              <div class="card-image-wrapper">
                <img
                  :src="property.photo_location?.[0] || 'https://placehold.co/400x220?text=No+Photo'"
                  :alt="property.title"
                  class="card-image"
                  @error="handleImageError"
                />
                <span :class="['status-pill', `pill-${property.status}`]">{{ property.status }}</span>
                <span class="card-id">#{{ property.id }}</span>
                <div class="card-views-overlay">
                  <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24"
                    fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                    <circle cx="12" cy="12" r="3"></circle>
                  </svg>
                  {{ property.views_count?.toLocaleString() ?? 0 }}
                </div>
              </div>

              <div class="card-body">
                <div class="card-title-row">
                  <h3 class="card-title">{{ property.title }}</h3>
                  <span :class="['type-badge', property.property_type]">{{ formatType(property.property_type) }}</span>
                </div>
                <p class="card-price">{{ formatPrice(property.price) }}</p>

                <div class="card-location" v-if="getLocation(property.location_id)">
                  <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24"
                    fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                    <circle cx="12" cy="10" r="3"></circle>
                  </svg>
                  {{ getLocation(property.location_id)?.city }}, {{ getLocation(property.location_id)?.country }}
                </div>

                <div class="card-details">
                  <span v-if="property.bedrooms">🛏 {{ property.bedrooms }} bed</span>
                  <span v-if="property.bathrooms">🚿 {{ property.bathrooms }} bath</span>
                  <span v-if="property.area_sqm">📐 {{ property.area_sqm }} m²</span>
                </div>

                <div class="card-owner">
                  <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24"
                    fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                    <circle cx="12" cy="7" r="4"></circle>
                  </svg>
                  Owner #{{ property.owner_id }} &nbsp;·&nbsp; Listed {{ formatDate(property.created_at) }}
                </div>
              </div>

              <div class="card-footer">
                <select
                  :value="property.status"
                  @change="updateStatus(property, $event.target.value)"
                  :class="['status-select', `status-${property.status}`]"
                >
                  <option value="available">Available</option>
                  <option value="pending">Pending</option>
                  <option value="sold">Sold</option>
                  <option value="rented">Rented</option>
                </select>
                <div class="action-buttons">
                  <RouterLink :to="`/property/${property.id}`" class="action-btn view-btn" title="View">
                    <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24"
                      fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                      <circle cx="12" cy="12" r="3"></circle>
                    </svg>
                  </RouterLink>
                  <RouterLink :to="`/seller/edit/${property.id}`" class="action-btn edit-btn" title="Edit">
                    <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24"
                      fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                      <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                    </svg>
                  </RouterLink>
                  <button @click="confirmDelete(property)" class="action-btn delete-btn" title="Delete">
                    <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24"
                      fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <polyline points="3 6 5 6 21 6"></polyline>
                      <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"></path>
                      <path d="M10 11v6"></path><path d="M14 11v6"></path>
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
          <button @click="currentPage--" :disabled="currentPage === 1" class="page-btn">‹ Prev</button>
          <button
            v-for="page in pageNumbers"
            :key="page"
            @click="currentPage = page"
            :class="['page-btn', { active: page === currentPage }]"
          >{{ page }}</button>
          <button @click="currentPage++" :disabled="currentPage === totalPages" class="page-btn">Next ›</button>
        </div>

      </div><!-- /v-else (isAdmin) -->
    </div><!-- /container -->

    <!-- Delete Confirmation Modal -->
    <Transition name="modal">
      <div v-if="deleteModal.show" class="modal-overlay" @click.self="deleteModal.show = false">
        <div class="modal">
          <div class="modal-icon danger">
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24"
              fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="3 6 5 6 21 6"></polyline>
              <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"></path>
              <path d="M10 11v6"></path><path d="M14 11v6"></path>
              <path d="M9 6V4h6v2"></path>
            </svg>
          </div>
          <h3 class="modal-title">Delete Property?</h3>
          <p class="modal-body">
            Are you sure you want to permanently delete
            <strong>"{{ deleteModal.property?.title }}"</strong>?
            This action cannot be undone.
          </p>
          <div class="modal-actions">
            <button @click="deleteModal.show = false" class="btn btn-secondary">Cancel</button>
            <button @click="deleteProperty" class="btn btn-danger" :disabled="deleteModal.loading">
              <span v-if="!deleteModal.loading">Delete Forever</span>
              <span v-else>Deleting…</span>
            </button>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Toast -->
    <Transition name="toast">
      <div v-if="toast.show" :class="['toast', toast.type]">
        <svg v-if="toast.type === 'success'" xmlns="http://www.w3.org/2000/svg" width="18" height="18"
          viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"
          stroke-linecap="round" stroke-linejoin="round">
          <polyline points="20 6 9 17 4 12"></polyline>
        </svg>
        <svg v-else xmlns="http://www.w3.org/2000/svg" width="18" height="18"
          viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"
          stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" y1="8" x2="12" y2="12"></line>
          <line x1="12" y1="16" x2="12.01" y2="16"></line>
        </svg>
        {{ toast.message }}
      </div>
    </Transition>

  </div>
</template>

<script>
import { ref, computed, reactive, onMounted } from 'vue';

export default {
  name: 'ManagePropertiesView',

  setup() {
    // ── Auth ──────────────────────────────────────────────────
    const isAdmin = ref(true); // TODO: replace with real admin auth check

    // ── State ─────────────────────────────────────────────────
    const loading = ref(true);
    const allProperties = ref([]);
    const allLocations = ref([]);

    // Toolbar
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

    // Toast
    const toast = reactive({
      show: false,
      message: '',
      type: 'success',
      timer: null
    });

    // ── Helpers ───────────────────────────────────────────────

    const getLocation = (locationId) =>
      allLocations.value.find(l => l.id === locationId) || null;

    const formatPrice = (price) => {
      if (price == null) return 'Price on request';
      return new Intl.NumberFormat('en-US', {
        style: 'currency', currency: 'USD', maximumFractionDigits: 0
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
      allProperties.value.filter(p => p.status === status || (status === 'sold' && p.status === 'rented')).length;

    const totalViews = computed(() =>
      allProperties.value.reduce((sum, p) => sum + (p.views_count || 0), 0)
    );

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

    // ── Computed: filtered & paginated ────────────────────────

    const filteredProperties = computed(() => {
      let result = [...allProperties.value];

      if (searchQuery.value.trim()) {
        const q = searchQuery.value.toLowerCase();
        result = result.filter(p => {
          const loc = getLocation(p.location_id);
          return (
            p.title?.toLowerCase().includes(q) ||
            loc?.city?.toLowerCase().includes(q) ||
            loc?.country?.toLowerCase().includes(q) ||
            String(p.owner_id).includes(q) ||
            String(p.id).includes(q)
          );
        });
      }

      if (filterStatus.value) {
        result = result.filter(p => p.status === filterStatus.value);
      }

      if (filterType.value) {
        result = result.filter(p => p.property_type === filterType.value);
      }

      switch (sortBy.value) {
        case 'newest':
          result.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
          break;
        case 'oldest':
          result.sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
          break;
        case 'price-high':
          result.sort((a, b) => (b.price || 0) - (a.price || 0));
          break;
        case 'price-low':
          result.sort((a, b) => (a.price || 0) - (b.price || 0));
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
      const total = totalPages.value;
      const current = currentPage.value;
      let start = Math.max(1, current - 2);
      let end = Math.min(total, current + 2);
      if (current <= 3) end = Math.min(5, total);
      if (current >= total - 2) start = Math.max(1, total - 4);
      const pages = [];
      for (let i = start; i <= end; i++) pages.push(i);
      return pages;
    });

    // ── Toast ─────────────────────────────────────────────────

    const showToast = (message, type = 'success') => {
      if (toast.timer) clearTimeout(toast.timer);
      toast.message = message;
      toast.type = type;
      toast.show = true;
      toast.timer = setTimeout(() => { toast.show = false; }, 3000);
    };

    // ── Status Update ─────────────────────────────────────────

    const updateStatus = async (property, newStatus) => {
      const oldStatus = property.status;
      property.status = newStatus;
      try {
        await new Promise(resolve => setTimeout(resolve, 400));
        // Real app: await fetch(`/api/properties/${property.id}`, { method: 'PATCH', body: JSON.stringify({ status: newStatus }) })
        showToast(`Status updated to "${newStatus}"`);
      } catch {
        property.status = oldStatus;
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
        await new Promise(resolve => setTimeout(resolve, 700));
        // Real app: await fetch(`/api/properties/${deleteModal.property.id}`, { method: 'DELETE' })

        allProperties.value = allProperties.value.filter(
          p => p.id !== deleteModal.property.id
        );

        showToast(`"${deleteModal.property.title}" has been deleted`);
        deleteModal.show = false;
        deleteModal.property = null;

        if (paginatedProperties.value.length === 0 && currentPage.value > 1) {
          currentPage.value--;
        }
      } catch {
        showToast('Failed to delete property. Please try again.', 'error');
      } finally {
        deleteModal.loading = false;
      }
    };

    // ── Fetch ─────────────────────────────────────────────────

    const fetchData = async () => {
      loading.value = true;
      try {
        const res = await fetch('/example.json');
        const data = await res.json();
        allLocations.value = data.locations || [];
        allProperties.value = data.properties || []; // all properties, not filtered by owner
      } catch (err) {
        console.error('Error fetching properties:', err);
        showToast('Failed to load properties. Please refresh.', 'error');
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
      totalViews,
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
.manage-properties-view {
  min-height: 100vh;
  background-color: var(--color-background);
  padding-bottom: var(--spacing-5xl);
}

/* ── Breadcrumb ────────────────────────────────────────────── */
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
.breadcrumb .current  { color: var(--color-text-secondary); }

/* ── Page Header ───────────────────────────────────────────── */
.page-header {
  background: linear-gradient(135deg, #1a237e 0%, #283593 50%, #3949ab 100%);
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
  text-shadow: 2px 2px 8px rgba(0,0,0,.25);
}
.page-subtitle {
  font-size: var(--font-size-base);
  color: rgba(255,255,255,.85);
  margin: 0;
}
.page-header .btn-primary {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  white-space: nowrap;
  background: rgba(255,255,255,.15);
  border: 1.5px solid rgba(255,255,255,.4);
  color: var(--color-white);
  backdrop-filter: blur(4px);
}
.page-header .btn-primary:hover {
  background: rgba(255,255,255,.28);
}

/* ── Access Denied ─────────────────────────────────────────── */
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

/* ── Summary Bar ───────────────────────────────────────────── */
.summary-bar {
  display: flex;
  align-items: center;
  gap: var(--spacing-2xl);
  padding: var(--spacing-xl) var(--spacing-2xl);
  background: var(--color-white);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-card);
  margin-bottom: var(--spacing-2xl);
  flex-wrap: wrap;
}
.summary-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}
.summary-value {
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-text-primary);
  line-height: 1;
}
.summary-value.available { color: #2e7d32; }
.summary-value.pending   { color: #e65100; }
.summary-value.sold      { color: #c62828; }
.summary-label {
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  white-space: nowrap;
}
.summary-divider {
  width: 1px;
  height: 40px;
  background: var(--color-border);
}

/* ── Toolbar ───────────────────────────────────────────────── */
.toolbar {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
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
  padding: var(--spacing-md) var(--spacing-md) var(--spacing-md) calc(var(--spacing-md) * 2 + 16px);
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-lg);
  font-size: var(--font-size-sm);
  background: var(--color-white);
  color: var(--color-text-primary);
  transition: border-color var(--transition-base);
}
.search-input:focus { outline: none; border-color: var(--color-primary); }
.clear-search {
  position: absolute;
  right: var(--spacing-md);
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  color: var(--color-text-tertiary);
  font-size: var(--font-size-sm);
  padding: 2px 4px;
}
.clear-search:hover { color: var(--color-text-primary); }

.filters {
  display: flex;
  gap: var(--spacing-md);
  flex-wrap: wrap;
}
.filter-select {
  padding: var(--spacing-md) var(--spacing-lg);
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-lg);
  font-size: var(--font-size-sm);
  background: var(--color-white);
  color: var(--color-text-primary);
  cursor: pointer;
  transition: border-color var(--transition-base);
}
.filter-select:focus { outline: none; border-color: var(--color-primary); }

.view-toggle {
  display: flex;
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
}
.toggle-btn {
  padding: var(--spacing-md) var(--spacing-lg);
  background: var(--color-white);
  border: none;
  cursor: pointer;
  color: var(--color-text-tertiary);
  transition: all var(--transition-base);
  display: flex;
  align-items: center;
}
.toggle-btn:hover { background: var(--color-cream); color: var(--color-text-primary); }
.toggle-btn.active { background: var(--color-primary); color: var(--color-white); }

/* ── Loading / Empty ───────────────────────────────────────── */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-lg);
  padding: var(--spacing-5xl);
  color: var(--color-text-secondary);
}
.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--color-border);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-5xl);
  text-align: center;
  background: var(--color-white);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-card);
  color: var(--color-text-tertiary);
}
.empty-state h3 { color: var(--color-text-primary); margin: 0; }
.empty-state p  { margin: 0; }

.results-info {
  padding: var(--spacing-md) var(--spacing-lg);
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  border-bottom: 1px solid var(--color-border);
}

/* ── Table ─────────────────────────────────────────────────── */
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
  max-width: 240px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.property-id {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
}

.owner-badge {
  display: inline-block;
  padding: 2px 8px;
  background: #e8eaf6;
  color: #3949ab;
  border-radius: var(--radius-full);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  white-space: nowrap;
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
  max-width: 180px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.no-location { color: var(--color-text-tertiary); }

.views-cell {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  color: var(--color-text-secondary);
  white-space: nowrap;
}

/* Responsive table column hiding */
@media (max-width: 1100px) {
  .th-hide-lg, .td-hide-lg { display: none; }
}
@media (max-width: 800px) {
  .th-hide-md, .td-hide-md { display: none; }
}

/* ── Status Select ─────────────────────────────────────────── */
.status-select {
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius-full);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  border: 2px solid transparent;
  cursor: pointer;
  transition: all var(--transition-base);
}
.status-available { background: #e8f5e9; color: #2e7d32; border-color: #c8e6c9; }
.status-pending   { background: #fff3e0; color: #e65100; border-color: #ffe0b2; }
.status-sold      { background: #fce4ec; color: #c62828; border-color: #f8bbd0; }
.status-rented    { background: #e3f2fd; color: #1565c0; border-color: #bbdefb; }

/* ── Action Buttons ────────────────────────────────────────── */
.action-buttons {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}
.action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: var(--radius-md);
  border: none;
  cursor: pointer;
  transition: all var(--transition-base);
  text-decoration: none;
}
.view-btn   { background: #e3f2fd; color: #1565c0; }
.view-btn:hover { background: #1565c0; color: #fff; }
.edit-btn   { background: #e8f5e9; color: #2e7d32; }
.edit-btn:hover { background: #2e7d32; color: #fff; }
.delete-btn { background: #fce4ec; color: #c62828; }
.delete-btn:hover { background: #c62828; color: #fff; }

/* ── Card View ─────────────────────────────────────────────── */
.cards-view { }
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--spacing-xl);
  margin-top: var(--spacing-lg);
}

.listing-card {
  background: var(--color-white);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-card);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: box-shadow var(--transition-base), transform var(--transition-base);
}
.listing-card:hover {
  box-shadow: var(--shadow-card-hover);
  transform: translateY(-2px);
}
.listing-card.card-sold { opacity: 0.7; }

.card-image-wrapper {
  position: relative;
  height: 190px;
  overflow: hidden;
  background: var(--color-cream);
}
.card-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}
.listing-card:hover .card-image { transform: scale(1.04); }

.status-pill {
  position: absolute;
  top: var(--spacing-sm);
  right: var(--spacing-sm);
  padding: 3px 10px;
  border-radius: var(--radius-full);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  text-transform: capitalize;
}
.pill-available { background: #2e7d32; color: #fff; }
.pill-pending   { background: #e65100; color: #fff; }
.pill-sold      { background: #c62828; color: #fff; }
.pill-rented    { background: #1565c0; color: #fff; }

.card-id {
  position: absolute;
  top: var(--spacing-sm);
  left: var(--spacing-sm);
  background: rgba(0,0,0,.45);
  color: #fff;
  padding: 2px 8px;
  border-radius: var(--radius-sm);
  font-size: var(--font-size-xs);
}
.card-views-overlay {
  position: absolute;
  bottom: var(--spacing-sm);
  right: var(--spacing-sm);
  background: rgba(0,0,0,.5);
  color: #fff;
  padding: 2px 8px;
  border-radius: var(--radius-sm);
  font-size: var(--font-size-xs);
  display: flex;
  align-items: center;
  gap: 4px;
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
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  margin: 0;
  flex: 1;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
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
.card-owner {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
  margin-top: auto;
  padding-top: var(--spacing-xs);
  border-top: 1px solid var(--color-border);
}

.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-md) var(--spacing-lg);
  border-top: 1px solid var(--color-border);
  background: var(--color-cream);
  gap: var(--spacing-md);
}

/* ── Type Badge ────────────────────────────────────────────── */
.type-badge {
  padding: 2px 10px;
  border-radius: var(--radius-full);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  white-space: nowrap;
  flex-shrink: 0;
}
.type-badge.house     { background: #e8eaf6; color: #3949ab; }
.type-badge.apartment { background: #e0f7fa; color: #00838f; }
.type-badge.land      { background: #f1f8e9; color: #558b2f; }

/* ── Pagination ────────────────────────────────────────────── */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: var(--spacing-sm);
  margin-top: var(--spacing-2xl);
  flex-wrap: wrap;
}
.page-btn {
  padding: var(--spacing-sm) var(--spacing-lg);
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-white);
  color: var(--color-text-primary);
  cursor: pointer;
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  transition: all var(--transition-base);
}
.page-btn:hover:not(:disabled) {
  border-color: var(--color-primary);
  color: var(--color-primary);
}
.page-btn.active {
  background: var(--color-primary);
  border-color: var(--color-primary);
  color: var(--color-white);
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
  max-width: 440px;
  width: 100%;
  box-shadow: 0 24px 64px rgba(0,0,0,.2);
  text-align: center;
}
.modal-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  border-radius: 50%;
  margin-bottom: var(--spacing-lg);
}
.modal-icon.danger { background: #fce4ec; color: #c62828; }
.modal-title { font-size: var(--font-size-xl); font-weight: var(--font-weight-bold); margin-bottom: var(--spacing-md); }
.modal-body  { color: var(--color-text-secondary); margin-bottom: var(--spacing-xl); line-height: 1.6; }
.modal-actions {
  display: flex;
  gap: var(--spacing-md);
  justify-content: center;
}

/* ── Buttons ───────────────────────────────────────────────── */
.btn {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-md) var(--spacing-xl);
  border-radius: var(--radius-lg);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  border: none;
  text-decoration: none;
  transition: all var(--transition-base);
}
.btn-primary  { background: var(--color-primary); color: var(--color-white); }
.btn-primary:hover { background: var(--color-primary-dark); }
.btn-secondary { background: var(--color-cream); color: var(--color-text-primary); border: 1.5px solid var(--color-border); }
.btn-secondary:hover { background: var(--color-border); }
.btn-danger   { background: #c62828; color: #fff; }
.btn-danger:hover { background: #b71c1c; }
.btn-danger:disabled { opacity: .6; cursor: not-allowed; }

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
.toast.success { background: #2e7d32; color: #fff; }
.toast.error   { background: #c62828; color: #fff; }

/* ── Transitions ───────────────────────────────────────────── */
.modal-enter-active, .modal-leave-active { transition: opacity 0.2s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
.modal-enter-active .modal, .modal-leave-active .modal { transition: transform 0.2s ease; }
.modal-enter-from .modal { transform: scale(0.93); }
.modal-leave-to .modal   { transform: scale(0.93); }

.toast-enter-active, .toast-leave-active { transition: all 0.3s ease; }
.toast-enter-from, .toast-leave-to { opacity: 0; transform: translateX(-50%) translateY(20px); }

/* ── Responsive ────────────────────────────────────────────── */
@media (max-width: 768px) {
  .page-title { font-size: var(--font-size-2xl); }
  .header-content { flex-direction: column; align-items: flex-start; }
  .page-header .btn-primary { width: 100%; justify-content: center; }
  .toolbar { flex-direction: column; align-items: stretch; }
  .filters { flex-direction: column; }
  .filter-select { width: 100%; }
  .summary-bar { gap: var(--spacing-lg); justify-content: center; }
  .summary-divider { display: none; }
  .cards-grid { grid-template-columns: 1fr; }
}

@media (max-width: 480px) {
  .table-wrapper { display: none; }
  .view-toggle { display: none; }
}
</style>