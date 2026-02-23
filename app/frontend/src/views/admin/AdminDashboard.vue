<template>
  <div class="admin-view">

    <!-- Hero -->
    <div class="admin-hero">
      <div class="hero-overlay"></div>
      <div class="hero-content">
        <div class="hero-badge">Admin Panel</div>
        <h1 class="hero-title">Command Center</h1>
        <p class="hero-subtitle">Full oversight of users, properties, and platform activity</p>
      </div>
    </div>

    <!-- Main Content -->
    <div class="admin-content">
      <div class="container">

        <!-- Loading -->
        <div v-if="loading" class="loading-state">
          <div class="spinner"></div>
          <p>Loading dashboard data…</p>
        </div>

        <template v-else>

          <!-- Stats Grid -->
          <section class="stats-section">
            <div class="stats-grid">
              <div class="stat-card stat-users">
                <div class="stat-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24"
                    fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                    <circle cx="9" cy="7" r="4"></circle>
                    <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                    <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                  </svg>
                </div>
                <div class="stat-body">
                  <span class="stat-value">{{ stats.totalUsers.toLocaleString() }}</span>
                  <span class="stat-label">Total Users</span>
                  <span class="stat-change positive">+{{ stats.newUsersThisMonth }} this month</span>
                </div>
              </div>

              <div class="stat-card stat-properties">
                <div class="stat-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24"
                    fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                    <polyline points="9 22 9 12 15 12 15 22"></polyline>
                  </svg>
                </div>
                <div class="stat-body">
                  <span class="stat-value">{{ stats.totalProperties.toLocaleString() }}</span>
                  <span class="stat-label">Total Properties</span>
                  <span class="stat-change positive">+{{ stats.newPropertiesThisMonth }} this month</span>
                </div>
              </div>

              <div class="stat-card stat-active">
                <div class="stat-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24"
                    fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
                  </svg>
                </div>
                <div class="stat-body">
                  <span class="stat-value">{{ stats.activeListings.toLocaleString() }}</span>
                  <span class="stat-label">Active Listings</span>
                  <span class="stat-change neutral">{{ stats.pendingReview }} pending review</span>
                </div>
              </div>

              <div class="stat-card stat-revenue">
                <div class="stat-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24"
                    fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="12" y1="1" x2="12" y2="23"></line>
                    <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
                  </svg>
                </div>
                <div class="stat-body">
                  <span class="stat-value">${{ formatMillions(stats.totalValue) }}</span>
                  <span class="stat-label">Total Listing Value</span>
                  <span class="stat-change positive">↑ 12.4% vs last month</span>
                </div>
              </div>
            </div>
          </section>

          <!-- Quick Actions -->
          <section class="actions-section">
            <h2 class="section-title">Management</h2>
            <div class="actions-grid">

              <RouterLink to="/admin/users" class="action-card action-users">
                <div class="action-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24"
                    fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                    <circle cx="9" cy="7" r="4"></circle>
                    <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                    <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                  </svg>
                </div>
                <div class="action-body">
                  <h3 class="action-title">Manage Users</h3>
                  <p class="action-desc">View, edit roles, verify, and suspend user accounts.</p>
                  <div class="action-meta">
                    <span class="meta-pill">{{ stats.unverifiedUsers }} unverified</span>
                    <span class="meta-pill warn">{{ stats.suspendedUsers }} suspended</span>
                  </div>
                </div>
                <div class="action-arrow">→</div>
              </RouterLink>

              <RouterLink to="/admin/properties" class="action-card action-properties">
                <div class="action-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24"
                    fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="3" width="7" height="7"></rect>
                    <rect x="14" y="3" width="7" height="7"></rect>
                    <rect x="14" y="14" width="7" height="7"></rect>
                    <rect x="3" y="14" width="7" height="7"></rect>
                  </svg>
                </div>
                <div class="action-body">
                  <h3 class="action-title">Manage Properties</h3>
                  <p class="action-desc">Review listings, approve submissions, and moderate content.</p>
                  <div class="action-meta">
                    <span class="meta-pill warn">{{ stats.pendingReview }} need review</span>
                    <span class="meta-pill">{{ stats.activeListings }} active</span>
                  </div>
                </div>
                <div class="action-arrow">→</div>
              </RouterLink>

            </div>
          </section>

          <!-- Two-Column: Activity + Breakdown -->
          <div class="bottom-grid">

            <!-- Recent Activity -->
            <section class="activity-section">
              <div class="section-header">
                <h2 class="section-title">Recent Activity</h2>
                <span class="section-tag">Last 48h</span>
              </div>

              <div class="activity-list">
                <div
                  v-for="item in recentActivity"
                  :key="item.id"
                  class="activity-item"
                  :class="item.type"
                >
                  <div class="activity-dot"></div>
                  <div class="activity-content">
                    <p class="activity-text">{{ item.message }}</p>
                    <span class="activity-time">{{ formatTimeAgo(item.timestamp) }}</span>
                  </div>
                </div>
              </div>
            </section>

            <!-- Role Breakdown -->
            <section class="breakdown-section">
              <div class="section-header">
                <h2 class="section-title">User Roles</h2>
              </div>

              <div class="breakdown-list">
                <div v-for="role in roleBreakdown" :key="role.name" class="breakdown-item">
                  <div class="breakdown-label">
                    <span class="role-dot" :class="role.color"></span>
                    <span class="role-name">{{ role.name }}</span>
                    <span class="role-count">{{ role.count }}</span>
                  </div>
                  <div class="breakdown-bar-track">
                    <div
                      class="breakdown-bar-fill"
                      :class="role.color"
                      :style="{ width: (role.count / stats.totalUsers * 100) + '%' }"
                    ></div>
                  </div>
                </div>
              </div>

              <!-- Property Status Breakdown -->
              <div class="section-header" style="margin-top: var(--spacing-2xl)">
                <h2 class="section-title">Property Status</h2>
              </div>
              <div class="breakdown-list">
                <div v-for="status in statusBreakdown" :key="status.name" class="breakdown-item">
                  <div class="breakdown-label">
                    <span class="role-dot" :class="status.color"></span>
                    <span class="role-name">{{ status.name }}</span>
                    <span class="role-count">{{ status.count }}</span>
                  </div>
                  <div class="breakdown-bar-track">
                    <div
                      class="breakdown-bar-fill"
                      :class="status.color"
                      :style="{ width: (status.count / stats.totalProperties * 100) + '%' }"
                    ></div>
                  </div>
                </div>
              </div>
            </section>

          </div>

        </template>
      </div>
    </div>

  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import api from '../../services/api.js';

export default {
  name: 'AdminDashboardView',

  setup() {
    const loading = ref(true);

    const stats = ref({
      totalUsers: 0,
      newUsersThisMonth: 0,
      unverifiedUsers: 0,
      suspendedUsers: 0,
      totalProperties: 0,
      newPropertiesThisMonth: 0,
      activeListings: 0,
      pendingReview: 0,
      totalValue: 0,
    });

    const roleBreakdown = ref([
      { name: 'Buyers / Users', count: 0, color: 'blue' },
      { name: 'Sellers',        count: 0, color: 'gold' },
      { name: 'Agents',         count: 0, color: 'green' },
      { name: 'Admins',         count: 0, color: 'red' },
    ]);

    const statusBreakdown = ref([
      { name: 'Available', count: 0, color: 'green' },
      { name: 'Pending',   count: 0, color: 'gold' },
      { name: 'Sold',      count: 0, color: 'blue' },
      { name: 'Rented',    count: 0, color: 'red' },
    ]);

    const recentActivity = ref([]);

    // ── Helpers ────────────────────────────────────────────────

    const formatMillions = (val) => {
      if (val >= 1_000_000_000) return (val / 1_000_000_000).toFixed(1) + 'B';
      if (val >= 1_000_000)     return (val / 1_000_000).toFixed(1) + 'M';
      return val.toLocaleString();
    };

    const formatTimeAgo = (date) => {
      const diff    = Date.now() - new Date(date).getTime();
      const minutes = Math.floor(diff / 60_000);
      const hours   = Math.floor(minutes / 60);
      const days    = Math.floor(hours / 24);
      if (days > 0)    return `${days}d ago`;
      if (hours > 0)   return `${hours}h ago`;
      if (minutes > 0) return `${minutes}m ago`;
      return 'Just now';
    };

    // ── Data Loading ───────────────────────────────────────────

    const loadMockData = () => {
      // Replace with real API calls, e.g.:
      //   const { data: users }      = await api.get('/admin/users/stats');
      //   const { data: properties } = await api.get('/admin/properties/stats');

      stats.value = {
        totalUsers:            247,
        newUsersThisMonth:     18,
        unverifiedUsers:       9,
        suspendedUsers:        3,
        totalProperties:       134,
        newPropertiesThisMonth: 11,
        activeListings:        98,
        pendingReview:         7,
        totalValue:            182_400_000,
      };

      roleBreakdown.value = [
        { name: 'Buyers / Users', count: 190, color: 'blue' },
        { name: 'Sellers',        count: 42,  color: 'gold' },
        { name: 'Agents',         count: 12,  color: 'green' },
        { name: 'Admins',         count: 3,   color: 'red' },
      ];

      statusBreakdown.value = [
        { name: 'Available', count: 98,  color: 'green' },
        { name: 'Pending',   count: 14,  color: 'gold' },
        { name: 'Sold',      count: 17,  color: 'blue' },
        { name: 'Rented',    count: 5,   color: 'red' },
      ];

      recentActivity.value = [
        { id: 1, type: 'user',     message: 'New user registered: sarah.kim@example.com',            timestamp: new Date(Date.now() - 12 * 60_000) },
        { id: 2, type: 'property', message: 'Listing "Oceanfront Villa" submitted for review',        timestamp: new Date(Date.now() - 45 * 60_000) },
        { id: 3, type: 'user',     message: 'User michael.torres verified their account',             timestamp: new Date(Date.now() - 2 * 3600_000) },
        { id: 4, type: 'warn',     message: 'Listing "Downtown Loft" flagged for missing photos',     timestamp: new Date(Date.now() - 5 * 3600_000) },
        { id: 5, type: 'property', message: 'Property #88 status changed to Sold',                   timestamp: new Date(Date.now() - 9 * 3600_000) },
        { id: 6, type: 'warn',     message: 'User david.brown suspended due to policy violation',     timestamp: new Date(Date.now() - 24 * 3600_000) },
        { id: 7, type: 'user',     message: '5 new users registered overnight',                       timestamp: new Date(Date.now() - 30 * 3600_000) },
      ];
    };

    onMounted(async () => {
      try {
        // await api.get('/admin/stats') — swap in real endpoints when ready
        loadMockData();
      } catch (err) {
        console.error('Admin dashboard error:', err);
        loadMockData(); // fallback
      } finally {
        loading.value = false;
      }
    });

    return {
      loading,
      stats,
      roleBreakdown,
      statusBreakdown,
      recentActivity,
      formatMillions,
      formatTimeAgo,
    };
  }
};
</script>

<style scoped>
/* ── Base ──────────────────────────────────────────────────── */
.admin-view {
  min-height: 100vh;
  background-color: var(--color-background);
  padding-bottom: var(--spacing-5xl);
}

.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 var(--spacing-xl);
}

/* ── Hero ──────────────────────────────────────────────────── */
.admin-hero {
  position: relative;
  height: 240px;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 60%, #0f3460 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse at 20% 50%, rgba(228, 169, 93, 0.15) 0%, transparent 60%),
    radial-gradient(ellipse at 80% 30%, rgba(255, 195, 96, 0.10) 0%, transparent 50%);
}

.hero-content {
  position: relative;
  z-index: 10;
  text-align: center;
}

.hero-badge {
  display: inline-block;
  padding: 4px 14px;
  border: 1px solid rgba(228, 169, 93, 0.6);
  border-radius: var(--radius-full);
  font-size: var(--font-size-xs);
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--color-primary);
  margin-bottom: var(--spacing-md);
  backdrop-filter: blur(4px);
}

.hero-title {
  font-size: var(--font-size-4xl);
  font-weight: var(--font-weight-bold);
  color: #fff;
  margin-bottom: var(--spacing-sm);
  text-shadow: 0 2px 20px rgba(0,0,0,0.4);
}

.hero-subtitle {
  font-size: var(--font-size-base);
  color: rgba(255,255,255,0.7);
  margin: 0;
}

/* ── Content Wrapper ───────────────────────────────────────── */
.admin-content {
  padding: var(--spacing-3xl) 0;
}

/* ── Loading ───────────────────────────────────────────────── */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-lg);
  padding: var(--spacing-5xl);
  color: var(--color-text-secondary);
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid var(--color-primary-light);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 0.9s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

/* ── Section Titles ────────────────────────────────────────── */
.section-title {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-text-primary);
  margin: 0;
}

.section-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-xl);
}

.section-tag {
  font-size: var(--font-size-xs);
  padding: 3px 10px;
  border-radius: var(--radius-full);
  background-color: var(--color-primary-light);
  color: var(--color-primary-dark);
  font-weight: var(--font-weight-semibold);
}

/* ── Stats Grid ────────────────────────────────────────────── */
.stats-section {
  margin-bottom: var(--spacing-3xl);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--spacing-xl);
}

.stat-card {
  background: var(--color-white);
  border-radius: var(--radius-xl);
  padding: var(--spacing-2xl);
  display: flex;
  align-items: flex-start;
  gap: var(--spacing-lg);
  box-shadow: var(--shadow-card);
  border-left: 4px solid transparent;
  transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 30px rgba(0,0,0,0.10);
}

.stat-users     { border-left-color: #60a5fa; }
.stat-properties{ border-left-color: var(--color-primary); }
.stat-active    { border-left-color: #34d399; }
.stat-revenue   { border-left-color: #f472b6; }

.stat-icon {
  flex-shrink: 0;
  width: 52px;
  height: 52px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-users     .stat-icon { background: #eff6ff; color: #60a5fa; }
.stat-properties .stat-icon{ background: var(--color-primary-light); color: var(--color-primary-dark); }
.stat-active    .stat-icon { background: #ecfdf5; color: #34d399; }
.stat-revenue   .stat-icon { background: #fdf2f8; color: #f472b6; }

.stat-body {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.stat-value {
  font-size: var(--font-size-3xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-text-primary);
  line-height: 1;
}

.stat-label {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  font-weight: var(--font-weight-medium);
}

.stat-change {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  margin-top: 4px;
}

.stat-change.positive { color: #34d399; }
.stat-change.neutral  { color: var(--color-primary-dark); }

/* ── Action Cards ──────────────────────────────────────────── */
.actions-section {
  margin-bottom: var(--spacing-3xl);
}

.actions-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-xl);
}

.action-card {
  background: var(--color-white);
  border-radius: var(--radius-xl);
  padding: var(--spacing-2xl);
  display: flex;
  align-items: center;
  gap: var(--spacing-xl);
  box-shadow: var(--shadow-card);
  text-decoration: none;
  border: 2px solid transparent;
  transition: all 0.2s;
  cursor: pointer;
}

.action-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 40px rgba(0,0,0,0.12);
  text-decoration: none;
}

.action-users:hover     { border-color: #60a5fa; }
.action-properties:hover{ border-color: var(--color-primary); }

.action-icon {
  flex-shrink: 0;
  width: 64px;
  height: 64px;
  border-radius: var(--radius-xl);
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-users     .action-icon { background: #eff6ff; color: #60a5fa; }
.action-properties .action-icon{ background: var(--color-primary-light); color: var(--color-primary-dark); }

.action-body {
  flex: 1;
}

.action-title {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-xs);
}

.action-desc {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  margin-bottom: var(--spacing-md);
  line-height: 1.5;
}

.action-meta {
  display: flex;
  gap: var(--spacing-sm);
  flex-wrap: wrap;
}

.meta-pill {
  font-size: var(--font-size-xs);
  padding: 3px 10px;
  border-radius: var(--radius-full);
  background: var(--color-primary-light);
  color: var(--color-primary-dark);
  font-weight: var(--font-weight-semibold);
}

.meta-pill.warn {
  background: #fef3c7;
  color: #92400e;
}

.action-arrow {
  font-size: var(--font-size-2xl);
  color: var(--color-text-tertiary);
  transition: transform 0.2s, color 0.2s;
}

.action-card:hover .action-arrow {
  transform: translateX(4px);
  color: var(--color-primary-dark);
}

/* ── Bottom Grid ───────────────────────────────────────────── */
.bottom-grid {
  display: grid;
  grid-template-columns: 3fr 2fr;
  gap: var(--spacing-xl);
}

/* ── Activity ──────────────────────────────────────────────── */
.activity-section {
  background: var(--color-white);
  border-radius: var(--radius-xl);
  padding: var(--spacing-2xl);
  box-shadow: var(--shadow-card);
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.activity-item {
  display: flex;
  align-items: flex-start;
  gap: var(--spacing-md);
  padding: var(--spacing-md) 0;
  border-bottom: 1px solid var(--color-background-soft, #f5f5f5);
  position: relative;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-dot {
  flex-shrink: 0;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-top: 5px;
}

.activity-item.user .activity-dot     { background: #60a5fa; }
.activity-item.property .activity-dot { background: var(--color-primary); }
.activity-item.warn .activity-dot     { background: #f97316; }

.activity-content {
  flex: 1;
}

.activity-text {
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
  margin: 0 0 2px;
  line-height: 1.4;
}

.activity-time {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
}

/* ── Breakdown ─────────────────────────────────────────────── */
.breakdown-section {
  background: var(--color-white);
  border-radius: var(--radius-xl);
  padding: var(--spacing-2xl);
  box-shadow: var(--shadow-card);
}

.breakdown-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.breakdown-item {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.breakdown-label {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.role-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}

.role-dot.blue  { background: #60a5fa; }
.role-dot.gold  { background: var(--color-primary); }
.role-dot.green { background: #34d399; }
.role-dot.red   { background: #f87171; }

.role-name {
  flex: 1;
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}

.role-count {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-bold);
  color: var(--color-text-primary);
}

.breakdown-bar-track {
  height: 6px;
  border-radius: 3px;
  background: var(--color-background-soft, #f0f0f0);
  overflow: hidden;
}

.breakdown-bar-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.8s ease;
}

.breakdown-bar-fill.blue  { background: #60a5fa; }
.breakdown-bar-fill.gold  { background: var(--color-primary); }
.breakdown-bar-fill.green { background: #34d399; }
.breakdown-bar-fill.red   { background: #f87171; }

/* ── Responsive ────────────────────────────────────────────── */
@media (max-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .bottom-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }

  .actions-grid {
    grid-template-columns: 1fr;
  }

  .hero-title {
    font-size: var(--font-size-3xl);
  }

  .container {
    padding: 0 var(--spacing-md);
  }

  .action-card {
    flex-wrap: wrap;
  }
}

@media (max-width: 480px) {
  .admin-hero {
    height: 180px;
  }

  .hero-title {
    font-size: var(--font-size-2xl);
  }

  .stat-value {
    font-size: var(--font-size-2xl);
  }
}
</style>