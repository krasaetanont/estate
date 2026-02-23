<template>
  <div class="manage-users-view">

    <!-- Breadcrumb -->
    <div class="container">
      <nav class="breadcrumb">
        <RouterLink to="/admin">Admin Dashboard</RouterLink>
        <span class="separator">›</span>
        <span class="current">Manage Users</span>
      </nav>
    </div>

    <!-- Page Header -->
    <div class="page-header">
      <div class="container">
        <div class="header-content">
          <div>
            <h1 class="page-title">Manage Users</h1>
            <p class="page-subtitle">View, edit roles, and moderate all registered users</p>
          </div>
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

      <div v-else>

        <!-- Summary Bar -->
        <div class="summary-bar">
          <div class="summary-stat">
            <span class="summary-value">{{ allUsers.length }}</span>
            <span class="summary-label">Total Users</span>
          </div>
          <div class="summary-divider"></div>
          <div class="summary-stat">
            <span class="summary-value role-admin">{{ countByRole('admin') }}</span>
            <span class="summary-label">Admins</span>
          </div>
          <div class="summary-divider"></div>
          <div class="summary-stat">
            <span class="summary-value role-agent">{{ countByRole('agent') }}</span>
            <span class="summary-label">Agents</span>
          </div>
          <div class="summary-divider"></div>
          <div class="summary-stat">
            <span class="summary-value role-seller">{{ countByRole('seller') }}</span>
            <span class="summary-label">Sellers</span>
          </div>
          <div class="summary-divider"></div>
          <div class="summary-stat">
            <span class="summary-value role-user">{{ countByRole('user') }}</span>
            <span class="summary-label">Users</span>
          </div>
          <div class="summary-divider"></div>
          <div class="summary-stat">
            <span class="summary-value verified">{{ countVerified }}</span>
            <span class="summary-label">Verified</span>
          </div>
          <div class="summary-divider"></div>
          <div class="summary-stat">
            <span class="summary-value unverified">{{ allUsers.length - countVerified }}</span>
            <span class="summary-label">Unverified</span>
          </div>
        </div>

        <!-- Toolbar -->
        <div class="toolbar">
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
              placeholder="Search by name, email, phone…"
              class="search-input"
              @input="currentPage = 1"
            />
            <button v-if="searchQuery" @click="searchQuery = ''; currentPage = 1" class="clear-search">✕</button>
          </div>

          <div class="filters">
            <select v-model="filterRole" class="filter-select" @change="currentPage = 1">
              <option value="">All Roles</option>
              <option value="admin">Admin</option>
              <option value="agent">Agent</option>
              <option value="seller">Seller</option>
              <option value="user">User</option>
            </select>

            <select v-model="filterVerified" class="filter-select" @change="currentPage = 1">
              <option value="">All Verification</option>
              <option value="true">Verified</option>
              <option value="false">Unverified</option>
            </select>

            <select v-model="sortBy" class="filter-select" @change="currentPage = 1">
              <option value="newest">Newest First</option>
              <option value="oldest">Oldest First</option>
              <option value="name-asc">Name: A → Z</option>
              <option value="name-desc">Name: Z → A</option>
            </select>
          </div>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="loading-state">
          <div class="spinner"></div>
          <p>Loading users…</p>
        </div>

        <!-- Empty -->
        <div v-else-if="allUsers.length === 0" class="empty-state">
          <svg xmlns="http://www.w3.org/2000/svg" width="72" height="72" viewBox="0 0 24 24"
            fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
            <circle cx="9" cy="7" r="4"></circle>
            <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
          </svg>
          <h3>No Users Found</h3>
          <p>No users are registered on the platform yet.</p>
        </div>

        <!-- No Filter Results -->
        <div v-else-if="filteredUsers.length === 0" class="empty-state">
          <svg xmlns="http://www.w3.org/2000/svg" width="72" height="72" viewBox="0 0 24 24"
            fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle><path d="m21 21-4.35-4.35"></path>
          </svg>
          <h3>No Results Found</h3>
          <p>No users match your current search or filters.</p>
          <button @click="clearFilters" class="btn btn-secondary">Clear Filters</button>
        </div>

        <!-- User Table -->
        <div v-else class="table-wrapper">
          <div class="results-info">
            Showing <strong>{{ paginatedUsers.length }}</strong> of <strong>{{ filteredUsers.length }}</strong> users
          </div>

          <table class="user-table">
            <thead>
              <tr>
                <th class="th-avatar"></th>
                <th class="th-name">Name</th>
                <th class="th-email">Email</th>
                <th class="th-phone th-hide-md">Phone</th>
                <th class="th-role">Role</th>
                <th class="th-verified">Verified</th>
                <th class="th-joined th-hide-lg">Joined</th>
                <th class="th-actions">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="user in paginatedUsers"
                :key="user.id"
                class="user-row"
                :class="{ 'row-unverified': !user.is_verified }"
              >
                <!-- Avatar -->
                <td class="td-avatar">
                  <div class="avatar" :style="{ background: avatarColor(user.name) }">
                    {{ initials(user.name) }}
                  </div>
                </td>

                <!-- Name + ID -->
                <td>
                  <p class="user-name-text">{{ user.name }}</p>
                  <span class="user-id">#{{ user.id }}</span>
                </td>

                <!-- Email -->
                <td>
                  <a :href="`mailto:${user.email}`" class="email-link">{{ user.email }}</a>
                </td>

                <!-- Phone -->
                <td class="td-hide-md">
                  <span class="phone-text">{{ user.phone_number || '—' }}</span>
                </td>

                <!-- Role -->
                <td>
                  <select
                    :value="user.role"
                    @change="updateRole(user, $event.target.value)"
                    :class="['role-select', `role-${user.role}`]"
                    :disabled="user.role === 'admin'"
                  >
                    <option value="admin">Admin</option>
                    <option value="agent">Agent</option>
                    <option value="seller">Seller</option>
                    <option value="user">User</option>
                  </select>
                </td>

                <!-- Verified -->
                <td>
                  <button
                    @click="toggleVerified(user)"
                    :class="['verified-btn', user.is_verified ? 'is-verified' : 'not-verified']"
                    :title="user.is_verified ? 'Click to unverify' : 'Click to verify'"
                  >
                    <svg v-if="user.is_verified" xmlns="http://www.w3.org/2000/svg" width="13" height="13"
                      viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"
                      stroke-linecap="round" stroke-linejoin="round">
                      <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                    <svg v-else xmlns="http://www.w3.org/2000/svg" width="13" height="13"
                      viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"
                      stroke-linecap="round" stroke-linejoin="round">
                      <line x1="18" y1="6" x2="6" y2="18"></line>
                      <line x1="6" y1="6" x2="18" y2="18"></line>
                    </svg>
                    {{ user.is_verified ? 'Verified' : 'Unverified' }}
                  </button>
                </td>

                <!-- Joined -->
                <td class="td-hide-lg">
                  <span class="joined-text">{{ formatDate(user.created_at) }}</span>
                </td>

                <!-- Actions -->
                <td>
                  <div class="action-buttons">
                    <button
                      @click="openEditModal(user)"
                      class="action-btn edit-btn"
                      title="Edit user"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24"
                        fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                        <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                      </svg>
                    </button>
                    <button
                      @click="confirmDelete(user)"
                      class="action-btn delete-btn"
                      title="Delete user"
                      :disabled="user.role === 'admin'"
                    >
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

      </div><!-- /v-else -->
    </div><!-- /container -->

    <!-- ── Edit User Modal ───────────────────────────────────── -->
    <Transition name="modal">
      <div v-if="editModal.show" class="modal-overlay" @click.self="closeEditModal">
        <div class="modal">
          <div class="modal-header">
            <div class="modal-avatar" :style="{ background: avatarColor(editModal.user?.name || '') }">
              {{ initials(editModal.user?.name || '') }}
            </div>
            <div>
              <h3 class="modal-title">Edit User</h3>
              <p class="modal-subtitle">ID #{{ editModal.user?.id }}</p>
            </div>
            <button @click="closeEditModal" class="modal-close">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"
                fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>

          <div class="modal-body-form">
            <div class="form-group">
              <label class="form-label">Full Name</label>
              <input v-model="editForm.name" type="text" class="form-input" placeholder="Full name" />
              <span v-if="editErrors.name" class="form-error">{{ editErrors.name }}</span>
            </div>

            <div class="form-group">
              <label class="form-label">Email Address</label>
              <input v-model="editForm.email" type="email" class="form-input" placeholder="email@example.com" />
              <span v-if="editErrors.email" class="form-error">{{ editErrors.email }}</span>
            </div>

            <div class="form-group">
              <label class="form-label">Phone Number</label>
              <input v-model="editForm.phone_number" type="text" class="form-input" placeholder="+1-555-0000" />
            </div>

            <div class="form-row-2">
              <div class="form-group">
                <label class="form-label">Role</label>
                <select v-model="editForm.role" class="form-input">
                  <option value="admin">Admin</option>
                  <option value="agent">Agent</option>
                  <option value="seller">Seller</option>
                  <option value="user">User</option>
                </select>
              </div>
              <div class="form-group">
                <label class="form-label">Verification</label>
                <select v-model="editForm.is_verified" class="form-input">
                  <option :value="true">Verified</option>
                  <option :value="false">Unverified</option>
                </select>
              </div>
            </div>
          </div>

          <div class="modal-actions">
            <button @click="closeEditModal" class="btn btn-secondary">Cancel</button>
            <button @click="saveEdit" class="btn btn-primary" :disabled="editModal.saving">
              <span v-if="!editModal.saving">Save Changes</span>
              <span v-else>Saving…</span>
            </button>
          </div>
        </div>
      </div>
    </Transition>

    <!-- ── Delete Confirmation Modal ─────────────────────────── -->
    <Transition name="modal">
      <div v-if="deleteModal.show" class="modal-overlay" @click.self="deleteModal.show = false">
        <div class="modal modal-sm">
          <div class="modal-icon danger">
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24"
              fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="3 6 5 6 21 6"></polyline>
              <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"></path>
              <path d="M10 11v6"></path><path d="M14 11v6"></path>
              <path d="M9 6V4h6v2"></path>
            </svg>
          </div>
          <h3 class="modal-title">Delete User?</h3>
          <p class="modal-body-text">
            Are you sure you want to permanently delete
            <strong>{{ deleteModal.user?.name }}</strong>?
            All their data and listings will be removed. This cannot be undone.
          </p>
          <div class="modal-actions">
            <button @click="deleteModal.show = false" class="btn btn-secondary">Cancel</button>
            <button @click="deleteUser" class="btn btn-danger" :disabled="deleteModal.loading">
              <span v-if="!deleteModal.loading">Delete User</span>
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

// Deterministic avatar colour from name
const AVATAR_COLORS = [
  '#3949ab', '#00838f', '#2e7d32', '#e65100',
  '#c62828', '#6a1b9a', '#1565c0', '#37474f'
];

export default {
  name: 'ManageUsersView',

  setup() {
    // ── Auth ──────────────────────────────────────────────────
    const isAdmin = ref(true); // TODO: replace with real admin auth check

    // ── State ─────────────────────────────────────────────────
    const loading   = ref(true);
    const allUsers  = ref([]);

    // Toolbar
    const searchQuery    = ref('');
    const filterRole     = ref('');
    const filterVerified = ref('');
    const sortBy         = ref('newest');

    // Pagination
    const currentPage  = ref(1);
    const itemsPerPage = 10;

    // Edit modal
    const editModal = reactive({
      show:   false,
      user:   null,
      saving: false
    });
    const editForm = reactive({
      name:         '',
      email:        '',
      phone_number: '',
      role:         'user',
      is_verified:  false
    });
    const editErrors = reactive({ name: '', email: '' });

    // Delete modal
    const deleteModal = reactive({
      show:    false,
      user:    null,
      loading: false
    });

    // Toast
    const toast = reactive({
      show:    false,
      message: '',
      type:    'success',
      timer:   null
    });

    // ── Helpers ───────────────────────────────────────────────

    const initials = (name) => {
      if (!name) return '?';
      const parts = name.trim().split(' ');
      return parts.length >= 2
        ? (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
        : name.slice(0, 2).toUpperCase();
    };

    const avatarColor = (name) => {
      if (!name) return AVATAR_COLORS[0];
      const idx = name.charCodeAt(0) % AVATAR_COLORS.length;
      return AVATAR_COLORS[idx];
    };

    const formatDate = (dateStr) => {
      if (!dateStr) return '—';
      return new Date(dateStr).toLocaleDateString('en-US', {
        year: 'numeric', month: 'short', day: 'numeric'
      });
    };

    const countByRole = (role) =>
      allUsers.value.filter(u => u.role === role).length;

    const countVerified = computed(() =>
      allUsers.value.filter(u => u.is_verified).length
    );

    const clearFilters = () => {
      searchQuery.value    = '';
      filterRole.value     = '';
      filterVerified.value = '';
      sortBy.value         = 'newest';
      currentPage.value    = 1;
    };

    // ── Computed ──────────────────────────────────────────────

    const filteredUsers = computed(() => {
      let result = [...allUsers.value];

      if (searchQuery.value.trim()) {
        const q = searchQuery.value.toLowerCase();
        result = result.filter(u =>
          u.name?.toLowerCase().includes(q) ||
          u.email?.toLowerCase().includes(q) ||
          u.phone_number?.toLowerCase().includes(q) ||
          String(u.id).includes(q)
        );
      }

      if (filterRole.value) {
        result = result.filter(u => u.role === filterRole.value);
      }

      if (filterVerified.value !== '') {
        const verified = filterVerified.value === 'true';
        result = result.filter(u => u.is_verified === verified);
      }

      switch (sortBy.value) {
        case 'newest':
          result.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
          break;
        case 'oldest':
          result.sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
          break;
        case 'name-asc':
          result.sort((a, b) => a.name.localeCompare(b.name));
          break;
        case 'name-desc':
          result.sort((a, b) => b.name.localeCompare(a.name));
          break;
      }

      return result;
    });

    const totalPages = computed(() =>
      Math.ceil(filteredUsers.value.length / itemsPerPage)
    );

    const paginatedUsers = computed(() => {
      const start = (currentPage.value - 1) * itemsPerPage;
      return filteredUsers.value.slice(start, start + itemsPerPage);
    });

    const pageNumbers = computed(() => {
      const total   = totalPages.value;
      const current = currentPage.value;
      let start = Math.max(1, current - 2);
      let end   = Math.min(total, current + 2);
      if (current <= 3) end   = Math.min(5, total);
      if (current >= total - 2) start = Math.max(1, total - 4);
      const pages = [];
      for (let i = start; i <= end; i++) pages.push(i);
      return pages;
    });

    // ── Toast ─────────────────────────────────────────────────

    const showToast = (message, type = 'success') => {
      if (toast.timer) clearTimeout(toast.timer);
      toast.message = message;
      toast.type    = type;
      toast.show    = true;
      toast.timer   = setTimeout(() => { toast.show = false; }, 3000);
    };

    // ── Role Update ───────────────────────────────────────────

    const updateRole = async (user, newRole) => {
      const oldRole = user.role;
      user.role = newRole;
      try {
        await new Promise(resolve => setTimeout(resolve, 400));
        // Real app: await fetch(`/api/users/${user.id}`, { method: 'PATCH', body: JSON.stringify({ role: newRole }) })
        showToast(`${user.name}'s role updated to "${newRole}"`);
      } catch {
        user.role = oldRole;
        showToast('Failed to update role. Please try again.', 'error');
      }
    };

    // ── Verified Toggle ───────────────────────────────────────

    const toggleVerified = async (user) => {
      const prev = user.is_verified;
      user.is_verified = !prev;
      try {
        await new Promise(resolve => setTimeout(resolve, 300));
        // Real app: await fetch(`/api/users/${user.id}`, { method: 'PATCH', body: JSON.stringify({ is_verified: user.is_verified }) })
        showToast(`${user.name} marked as ${user.is_verified ? 'verified' : 'unverified'}`);
      } catch {
        user.is_verified = prev;
        showToast('Failed to update verification. Please try again.', 'error');
      }
    };

    // ── Edit Modal ────────────────────────────────────────────

    const openEditModal = (user) => {
      editModal.user    = user;
      editModal.show    = true;
      editModal.saving  = false;
      editForm.name         = user.name;
      editForm.email        = user.email;
      editForm.phone_number = user.phone_number || '';
      editForm.role         = user.role;
      editForm.is_verified  = user.is_verified;
      editErrors.name  = '';
      editErrors.email = '';
    };

    const closeEditModal = () => {
      editModal.show = false;
      editModal.user = null;
    };

    const validateEdit = () => {
      editErrors.name  = '';
      editErrors.email = '';
      let valid = true;
      if (!editForm.name.trim()) {
        editErrors.name = 'Name is required.';
        valid = false;
      }
      if (!editForm.email.trim() || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(editForm.email)) {
        editErrors.email = 'A valid email is required.';
        valid = false;
      }
      return valid;
    };

    const saveEdit = async () => {
      if (!validateEdit()) return;
      editModal.saving = true;
      try {
        await new Promise(resolve => setTimeout(resolve, 600));
        // Real app: await fetch(`/api/users/${editModal.user.id}`, { method: 'PUT', body: JSON.stringify(editForm) })

        // Apply changes locally
        const user = editModal.user;
        user.name         = editForm.name;
        user.email        = editForm.email;
        user.phone_number = editForm.phone_number;
        user.role         = editForm.role;
        user.is_verified  = editForm.is_verified;

        showToast(`${user.name}'s profile updated successfully`);
        closeEditModal();
      } catch {
        showToast('Failed to save changes. Please try again.', 'error');
      } finally {
        editModal.saving = false;
      }
    };

    // ── Delete ────────────────────────────────────────────────

    const confirmDelete = (user) => {
      if (user.role === 'admin') return;
      deleteModal.user    = user;
      deleteModal.show    = true;
      deleteModal.loading = false;
    };

    const deleteUser = async () => {
      deleteModal.loading = true;
      try {
        await new Promise(resolve => setTimeout(resolve, 700));
        // Real app: await fetch(`/api/users/${deleteModal.user.id}`, { method: 'DELETE' })

        allUsers.value = allUsers.value.filter(u => u.id !== deleteModal.user.id);
        showToast(`${deleteModal.user.name} has been deleted`);
        deleteModal.show = false;
        deleteModal.user = null;

        if (paginatedUsers.value.length === 0 && currentPage.value > 1) {
          currentPage.value--;
        }
      } catch {
        showToast('Failed to delete user. Please try again.', 'error');
      } finally {
        deleteModal.loading = false;
      }
    };

    // ── Fetch ─────────────────────────────────────────────────

    const fetchData = async () => {
      loading.value = true;
      try {
        const res  = await fetch('/example.json');
        const data = await res.json();
        allUsers.value = data.users || [];
      } catch (err) {
        console.error('Error fetching users:', err);
        showToast('Failed to load users. Please refresh.', 'error');
      } finally {
        loading.value = false;
      }
    };

    onMounted(fetchData);

    return {
      isAdmin,
      loading,
      allUsers,
      searchQuery,
      filterRole,
      filterVerified,
      sortBy,
      currentPage,
      filteredUsers,
      paginatedUsers,
      totalPages,
      pageNumbers,
      countVerified,
      editModal,
      editForm,
      editErrors,
      deleteModal,
      toast,
      initials,
      avatarColor,
      formatDate,
      countByRole,
      clearFilters,
      updateRole,
      toggleVerified,
      openEditModal,
      closeEditModal,
      saveEdit,
      confirmDelete,
      deleteUser
    };
  }
};
</script>

<style scoped>
/* ── Base ──────────────────────────────────────────────────── */
.manage-users-view {
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
.breadcrumb a { color: var(--color-primary-dark); text-decoration: none; transition: color var(--transition-base); }
.breadcrumb a:hover { color: var(--color-primary); text-decoration: underline; }
.breadcrumb .separator { color: var(--color-text-tertiary); }
.breadcrumb .current   { color: var(--color-text-secondary); }

/* ── Page Header ───────────────────────────────────────────── */
.page-header {
  background: linear-gradient(135deg, #004d40 0%, #00695c 50%, #00897b 100%);
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

/* ── Access Denied ─────────────────────────────────────────── */
.access-denied {
  display: flex; flex-direction: column; align-items: center;
  gap: var(--spacing-md); padding: var(--spacing-5xl);
  text-align: center; background: var(--color-white);
  border-radius: var(--radius-xl); box-shadow: var(--shadow-card);
}

/* ── Summary Bar ───────────────────────────────────────────── */
.summary-bar {
  display: flex; align-items: center; gap: var(--spacing-2xl);
  padding: var(--spacing-xl) var(--spacing-2xl);
  background: var(--color-white); border-radius: var(--radius-xl);
  box-shadow: var(--shadow-card); margin-bottom: var(--spacing-2xl);
  flex-wrap: wrap;
}
.summary-stat { display: flex; flex-direction: column; align-items: center; gap: 2px; }
.summary-value {
  font-size: var(--font-size-2xl); font-weight: var(--font-weight-bold);
  color: var(--color-text-primary); line-height: 1;
}
.summary-value.role-admin  { color: #c62828; }
.summary-value.role-agent  { color: #3949ab; }
.summary-value.role-seller { color: #e65100; }
.summary-value.role-user   { color: #00838f; }
.summary-value.verified    { color: #2e7d32; }
.summary-value.unverified  { color: #9e9e9e; }
.summary-label {
  font-size: var(--font-size-xs); color: var(--color-text-secondary);
  text-transform: uppercase; letter-spacing: 0.05em; white-space: nowrap;
}
.summary-divider { width: 1px; height: 40px; background: var(--color-border); }

/* ── Toolbar ───────────────────────────────────────────────── */
.toolbar {
  display: flex; align-items: center; gap: var(--spacing-md);
  margin-bottom: var(--spacing-xl); flex-wrap: wrap;
}
.search-wrapper { position: relative; flex: 1; min-width: 200px; }
.search-icon {
  position: absolute; left: var(--spacing-md); top: 50%;
  transform: translateY(-50%); color: var(--color-text-tertiary); pointer-events: none;
}
.search-input {
  width: 100%;
  padding: var(--spacing-md) var(--spacing-md) var(--spacing-md) calc(var(--spacing-md) * 2 + 16px);
  border: 1.5px solid var(--color-border); border-radius: var(--radius-lg);
  font-size: var(--font-size-sm); background: var(--color-white);
  color: var(--color-text-primary); transition: border-color var(--transition-base);
}
.search-input:focus { outline: none; border-color: var(--color-primary); }
.clear-search {
  position: absolute; right: var(--spacing-md); top: 50%;
  transform: translateY(-50%); background: none; border: none;
  cursor: pointer; color: var(--color-text-tertiary); padding: 2px 4px;
}
.clear-search:hover { color: var(--color-text-primary); }

.filters { display: flex; gap: var(--spacing-md); flex-wrap: wrap; }
.filter-select {
  padding: var(--spacing-md) var(--spacing-lg); border: 1.5px solid var(--color-border);
  border-radius: var(--radius-lg); font-size: var(--font-size-sm);
  background: var(--color-white); color: var(--color-text-primary);
  cursor: pointer; transition: border-color var(--transition-base);
}
.filter-select:focus { outline: none; border-color: var(--color-primary); }

/* ── Loading / Empty ───────────────────────────────────────── */
.loading-state {
  display: flex; flex-direction: column; align-items: center;
  gap: var(--spacing-lg); padding: var(--spacing-5xl);
  color: var(--color-text-secondary);
}
.spinner {
  width: 40px; height: 40px;
  border: 3px solid var(--color-border); border-top-color: var(--color-primary);
  border-radius: 50%; animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.empty-state {
  display: flex; flex-direction: column; align-items: center;
  gap: var(--spacing-md); padding: var(--spacing-5xl);
  text-align: center; background: var(--color-white);
  border-radius: var(--radius-xl); box-shadow: var(--shadow-card);
  color: var(--color-text-tertiary);
}
.empty-state h3 { color: var(--color-text-primary); margin: 0; }
.empty-state p  { margin: 0; }

/* ── Table ─────────────────────────────────────────────────── */
.table-wrapper {
  background: var(--color-white); border-radius: var(--radius-xl);
  box-shadow: var(--shadow-card); overflow-x: auto;
}
.results-info {
  padding: var(--spacing-md) var(--spacing-lg);
  font-size: var(--font-size-sm); color: var(--color-text-secondary);
  border-bottom: 1px solid var(--color-border);
}

.user-table {
  width: 100%; border-collapse: collapse; font-size: var(--font-size-sm);
}
.user-table th {
  background: var(--color-cream); padding: var(--spacing-lg) var(--spacing-md);
  text-align: left; font-weight: var(--font-weight-semibold);
  color: var(--color-text-secondary); font-size: var(--font-size-xs);
  text-transform: uppercase; letter-spacing: 0.05em; white-space: nowrap;
  border-bottom: 2px solid var(--color-border);
}
.user-table th:first-child { border-radius: var(--radius-xl) 0 0 0; }
.user-table th:last-child  { border-radius: 0 var(--radius-xl) 0 0; }

.user-row {
  border-bottom: 1px solid var(--color-border);
  transition: background-color var(--transition-base);
}
.user-row:last-child { border-bottom: none; }
.user-row:hover { background-color: var(--color-cream); }
.user-row.row-unverified { opacity: 0.75; }

.user-table td { padding: var(--spacing-md) var(--spacing-md); vertical-align: middle; }

/* Responsive hide */
@media (max-width: 1100px) { .th-hide-lg, .td-hide-lg { display: none; } }
@media (max-width: 800px)  { .th-hide-md, .td-hide-md { display: none; } }

/* ── Avatar ────────────────────────────────────────────────── */
.avatar {
  width: 40px; height: 40px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: var(--font-size-sm); font-weight: var(--font-weight-bold);
  color: #fff; flex-shrink: 0; letter-spacing: 0.5px;
}
.td-avatar { width: 56px; }

/* ── User Info ─────────────────────────────────────────────── */
.user-name-text {
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  margin: 0 0 2px 0;
  white-space: nowrap;
}
.user-id { font-size: var(--font-size-xs); color: var(--color-text-tertiary); }

.email-link {
  color: var(--color-primary-dark); text-decoration: none; font-size: var(--font-size-sm);
}
.email-link:hover { text-decoration: underline; }
.phone-text { color: var(--color-text-secondary); font-size: var(--font-size-sm); }
.joined-text { color: var(--color-text-secondary); font-size: var(--font-size-sm); white-space: nowrap; }

/* ── Role Select ───────────────────────────────────────────── */
.role-select {
  padding: 4px 10px; border-radius: var(--radius-full);
  font-size: var(--font-size-xs); font-weight: var(--font-weight-semibold);
  border: 2px solid transparent; cursor: pointer;
  transition: all var(--transition-base); appearance: auto;
}
.role-select:disabled { cursor: not-allowed; opacity: 0.8; }
.role-admin  { background: #fce4ec; color: #c62828; border-color: #f8bbd0; }
.role-agent  { background: #e8eaf6; color: #3949ab; border-color: #c5cae9; }
.role-seller { background: #fff3e0; color: #e65100; border-color: #ffe0b2; }
.role-user   { background: #e0f7fa; color: #00838f; border-color: #b2ebf2; }

/* ── Verified Toggle ───────────────────────────────────────── */
.verified-btn {
  display: inline-flex; align-items: center; gap: 5px;
  padding: 4px 12px; border-radius: var(--radius-full);
  border: 2px solid transparent; cursor: pointer;
  font-size: var(--font-size-xs); font-weight: var(--font-weight-semibold);
  transition: all var(--transition-base); white-space: nowrap;
}
.is-verified  { background: #e8f5e9; color: #2e7d32; border-color: #c8e6c9; }
.is-verified:hover  { background: #2e7d32; color: #fff; }
.not-verified { background: #fafafa; color: #9e9e9e; border-color: #e0e0e0; }
.not-verified:hover { background: #eeeeee; color: #424242; }

/* ── Action Buttons ────────────────────────────────────────── */
.action-buttons { display: flex; align-items: center; gap: var(--spacing-sm); }
.action-btn {
  display: flex; align-items: center; justify-content: center;
  width: 32px; height: 32px; border-radius: var(--radius-md);
  border: none; cursor: pointer; transition: all var(--transition-base);
}
.action-btn:disabled { opacity: 0.3; cursor: not-allowed; }
.edit-btn   { background: #e8f5e9; color: #2e7d32; }
.edit-btn:hover:not(:disabled)   { background: #2e7d32; color: #fff; }
.delete-btn { background: #fce4ec; color: #c62828; }
.delete-btn:hover:not(:disabled) { background: #c62828; color: #fff; }

/* ── Pagination ────────────────────────────────────────────── */
.pagination {
  display: flex; justify-content: center; align-items: center;
  gap: var(--spacing-sm); margin-top: var(--spacing-2xl); flex-wrap: wrap;
}
.page-btn {
  padding: var(--spacing-sm) var(--spacing-lg);
  border: 1.5px solid var(--color-border); border-radius: var(--radius-md);
  background: var(--color-white); color: var(--color-text-primary);
  cursor: pointer; font-size: var(--font-size-sm); font-weight: var(--font-weight-medium);
  transition: all var(--transition-base);
}
.page-btn:hover:not(:disabled) { border-color: var(--color-primary); color: var(--color-primary); }
.page-btn.active { background: var(--color-primary); border-color: var(--color-primary); color: #fff; }
.page-btn:disabled { opacity: 0.4; cursor: not-allowed; }

/* ── Modal Shared ──────────────────────────────────────────── */
.modal-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,.5);
  display: flex; align-items: center; justify-content: center;
  z-index: 1000; padding: var(--spacing-lg);
}
.modal {
  background: var(--color-white); border-radius: var(--radius-xl);
  padding: var(--spacing-3xl); max-width: 520px; width: 100%;
  box-shadow: 0 24px 64px rgba(0,0,0,.2);
}
.modal.modal-sm { max-width: 420px; text-align: center; }

/* Edit modal header */
.modal-header {
  display: flex; align-items: center; gap: var(--spacing-lg);
  margin-bottom: var(--spacing-2xl);
}
.modal-avatar {
  width: 52px; height: 52px; border-radius: 50%; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
  font-size: var(--font-size-base); font-weight: var(--font-weight-bold);
  color: #fff; letter-spacing: 0.5px;
}
.modal-title    { font-size: var(--font-size-xl); font-weight: var(--font-weight-bold); margin: 0 0 2px 0; }
.modal-subtitle { font-size: var(--font-size-sm); color: var(--color-text-tertiary); margin: 0; }
.modal-close {
  margin-left: auto; background: none; border: none; cursor: pointer;
  color: var(--color-text-tertiary); padding: 4px;
  border-radius: var(--radius-md); transition: all var(--transition-base);
}
.modal-close:hover { background: var(--color-cream); color: var(--color-text-primary); }

/* Delete modal icon */
.modal-icon {
  display: inline-flex; align-items: center; justify-content: center;
  width: 64px; height: 64px; border-radius: 50%; margin-bottom: var(--spacing-lg);
}
.modal-icon.danger { background: #fce4ec; color: #c62828; }
.modal-body-text { color: var(--color-text-secondary); margin-bottom: var(--spacing-xl); line-height: 1.6; }

/* Form */
.modal-body-form { display: flex; flex-direction: column; gap: var(--spacing-lg); margin-bottom: var(--spacing-2xl); }
.form-group { display: flex; flex-direction: column; gap: var(--spacing-xs); }
.form-row-2 { display: grid; grid-template-columns: 1fr 1fr; gap: var(--spacing-lg); }
.form-label { font-size: var(--font-size-sm); font-weight: var(--font-weight-medium); color: var(--color-text-primary); }
.form-input {
  padding: var(--spacing-md) var(--spacing-lg);
  border: 1.5px solid var(--color-border); border-radius: var(--radius-lg);
  font-size: var(--font-size-sm); color: var(--color-text-primary);
  background: var(--color-white); transition: border-color var(--transition-base);
}
.form-input:focus { outline: none; border-color: var(--color-primary); }
.form-error { font-size: var(--font-size-xs); color: #c62828; }

.modal-actions { display: flex; gap: var(--spacing-md); justify-content: flex-end; }
.modal.modal-sm .modal-actions { justify-content: center; }

/* ── Buttons ───────────────────────────────────────────────── */
.btn {
  display: inline-flex; align-items: center; gap: var(--spacing-sm);
  padding: var(--spacing-md) var(--spacing-xl); border-radius: var(--radius-lg);
  font-size: var(--font-size-base); font-weight: var(--font-weight-medium);
  cursor: pointer; border: none; text-decoration: none;
  transition: all var(--transition-base);
}
.btn-primary   { background: var(--color-primary); color: #fff; }
.btn-primary:hover:not(:disabled)   { background: var(--color-primary-dark); }
.btn-secondary { background: var(--color-cream); color: var(--color-text-primary); border: 1.5px solid var(--color-border); }
.btn-secondary:hover { background: var(--color-border); }
.btn-danger    { background: #c62828; color: #fff; }
.btn-danger:hover:not(:disabled) { background: #b71c1c; }
.btn:disabled  { opacity: 0.6; cursor: not-allowed; }

/* ── Toast ─────────────────────────────────────────────────── */
.toast {
  position: fixed; bottom: var(--spacing-2xl); left: 50%;
  transform: translateX(-50%); display: flex; align-items: center;
  gap: var(--spacing-md); padding: var(--spacing-md) var(--spacing-2xl);
  border-radius: var(--radius-full); font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium); box-shadow: 0 8px 32px rgba(0,0,0,.18);
  z-index: 2000; white-space: nowrap;
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
  .toolbar { flex-direction: column; align-items: stretch; }
  .filters { flex-direction: column; }
  .filter-select { width: 100%; }
  .summary-bar { gap: var(--spacing-lg); justify-content: center; }
  .summary-divider { display: none; }
  .form-row-2 { grid-template-columns: 1fr; }
  .modal-actions { flex-direction: column; }
}
</style>