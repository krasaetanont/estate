<template>
  <div class="seller-view">
    <!-- Hero Section -->
    <section class="seller-hero">
      <div class="hero-overlay"></div>
      <div class="hero-content">
        <div class="container">
          <h1 class="hero-title">Seller Dashboard</h1>
          <p class="hero-subtitle">
            Manage your property listings and track performance
          </p>
        </div>
      </div>
    </section>

    <!-- Main Content -->
    <div class="container">
      <div class="seller-content">
        <!-- Admin Check -->
        <div v-if="!isAdmin" class="access-denied">
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
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          <h2>Access Denied</h2>
          <p>Only sellers and administrators can access this dashboard.</p>
          <p class="contact-text">Please contact support to become a seller.</p>
          <RouterLink to="/" class="btn btn-primary">Return Home</RouterLink>
        </div>

        <!-- Dashboard Content -->
        <div v-else>
          <!-- Stats Overview -->
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-icon" style="background-color: #e3f2fd;">
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  width="32" 
                  height="32" 
                  viewBox="0 0 24 24" 
                  fill="none" 
                  stroke="#1976d2" 
                  stroke-width="2" 
                  stroke-linecap="round" 
                  stroke-linejoin="round"
                >
                  <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                  <polyline points="9 22 9 12 15 12 15 22"></polyline>
                </svg>
              </div>
              <div class="stat-content">
                <h3 class="stat-value">{{ stats.totalListings }}</h3>
                <p class="stat-label">Total Listings</p>
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-icon" style="background-color: #e8f5e9;">
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  width="32" 
                  height="32" 
                  viewBox="0 0 24 24" 
                  fill="none" 
                  stroke="#388e3c" 
                  stroke-width="2" 
                  stroke-linecap="round" 
                  stroke-linejoin="round"
                >
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                  <polyline points="22 4 12 14.01 9 11.01"></polyline>
                </svg>
              </div>
              <div class="stat-content">
                <h3 class="stat-value">{{ stats.activeListings }}</h3>
                <p class="stat-label">Active Listings</p>
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-icon" style="background-color: #fff3e0;">
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  width="32" 
                  height="32" 
                  viewBox="0 0 24 24" 
                  fill="none" 
                  stroke="#f57c00" 
                  stroke-width="2" 
                  stroke-linecap="round" 
                  stroke-linejoin="round"
                >
                  <circle cx="12" cy="12" r="10"></circle>
                  <polyline points="12 6 12 12 16 14"></polyline>
                </svg>
              </div>
              <div class="stat-content">
                <h3 class="stat-value">{{ stats.pendingListings }}</h3>
                <p class="stat-label">Pending Sales</p>
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-icon" style="background-color: var(--color-primary-light);">
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  width="32" 
                  height="32" 
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
              </div>
              <div class="stat-content">
                <h3 class="stat-value">{{ formatNumber(stats.totalViews) }}</h3>
                <p class="stat-label">Total Views</p>
              </div>
            </div>
          </div>

          <!-- Quick Actions -->
          <div class="quick-actions-section">
            <h2 class="section-title">Quick Actions</h2>
            <div class="actions-grid">
              <RouterLink to="/seller/add" class="action-card">
                <div class="action-icon add">
                  <svg 
                    xmlns="http://www.w3.org/2000/svg" 
                    width="40" 
                    height="40" 
                    viewBox="0 0 24 24" 
                    fill="none" 
                    stroke="currentColor" 
                    stroke-width="2" 
                    stroke-linecap="round" 
                    stroke-linejoin="round"
                  >
                    <line x1="12" y1="5" x2="12" y2="19"></line>
                    <line x1="5" y1="12" x2="19" y2="12"></line>
                  </svg>
                </div>
                <h3>Add New Property</h3>
                <p>List a new property for sale on the platform</p>
                <div class="action-arrow">→</div>
              </RouterLink>

              <RouterLink to="/seller/my-listings" class="action-card">
                <div class="action-icon list">
                  <svg 
                    xmlns="http://www.w3.org/2000/svg" 
                    width="40" 
                    height="40" 
                    viewBox="0 0 24 24" 
                    fill="none" 
                    stroke="currentColor" 
                    stroke-width="2" 
                    stroke-linecap="round" 
                    stroke-linejoin="round"
                  >
                    <line x1="8" y1="6" x2="21" y2="6"></line>
                    <line x1="8" y1="12" x2="21" y2="12"></line>
                    <line x1="8" y1="18" x2="21" y2="18"></line>
                    <line x1="3" y1="6" x2="3.01" y2="6"></line>
                    <line x1="3" y1="12" x2="3.01" y2="12"></line>
                    <line x1="3" y1="18" x2="3.01" y2="18"></line>
                  </svg>
                </div>
                <h3>My Listings</h3>
                <p>View and manage all your property listings</p>
                <div class="action-arrow">→</div>
              </RouterLink>

              <div @click="showAnalytics" class="action-card clickable">
                <div class="action-icon analytics">
                  <svg 
                    xmlns="http://www.w3.org/2000/svg" 
                    width="40" 
                    height="40" 
                    viewBox="0 0 24 24" 
                    fill="none" 
                    stroke="currentColor" 
                    stroke-width="2" 
                    stroke-linecap="round" 
                    stroke-linejoin="round"
                  >
                    <line x1="18" y1="20" x2="18" y2="10"></line>
                    <line x1="12" y1="20" x2="12" y2="4"></line>
                    <line x1="6" y1="20" x2="6" y2="14"></line>
                  </svg>
                </div>
                <h3>Analytics</h3>
                <p>View detailed performance metrics and insights</p>
                <div class="action-arrow">→</div>
              </div>

              <div @click="showMessages" class="action-card clickable">
                <div class="action-icon messages">
                  <svg 
                    xmlns="http://www.w3.org/2000/svg" 
                    width="40" 
                    height="40" 
                    viewBox="0 0 24 24" 
                    fill="none" 
                    stroke="currentColor" 
                    stroke-width="2" 
                    stroke-linecap="round" 
                    stroke-linejoin="round"
                  >
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                  </svg>
                </div>
                <h3>Messages</h3>
                <p>Check inquiries from potential buyers</p>
                <span v-if="stats.unreadMessages > 0" class="notification-badge">
                  {{ stats.unreadMessages }}
                </span>
                <div class="action-arrow">→</div>
              </div>
            </div>
          </div>

          <!-- Recent Activity -->
          <div class="recent-activity-section">
            <div class="section-header">
              <h2 class="section-title">Recent Activity</h2>
              <RouterLink to="/seller/my-listings" class="view-all-link">
                View All →
              </RouterLink>
            </div>

            <div v-if="recentActivity.length === 0" class="empty-state">
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
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="8" x2="12" y2="12"></line>
                <line x1="12" y1="16" x2="12.01" y2="16"></line>
              </svg>
              <p>No recent activity</p>
            </div>

            <div v-else class="activity-list">
              <div 
                v-for="activity in recentActivity" 
                :key="activity.id"
                class="activity-item"
              >
                <div class="activity-icon" :class="activity.type">
                  <component :is="getActivityIcon(activity.type)" />
                </div>
                <div class="activity-content">
                  <p class="activity-text">{{ activity.message }}</p>
                  <span class="activity-time">{{ formatTimeAgo(activity.timestamp) }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Tips & Resources -->
          <div class="tips-section">
            <h2 class="section-title">Seller Tips & Resources</h2>
            <div class="tips-grid">
              <div class="tip-card">
                <div class="tip-number">1</div>
                <h3>High-Quality Photos</h3>
                <p>Properties with professional photos get 3x more views. Ensure good lighting and showcase key features.</p>
              </div>

              <div class="tip-card">
                <div class="tip-number">2</div>
                <h3>Competitive Pricing</h3>
                <p>Research similar properties in your area. Price competitively to attract serious buyers quickly.</p>
              </div>

              <div class="tip-card">
                <div class="tip-number">3</div>
                <h3>Detailed Descriptions</h3>
                <p>Include all amenities, nearby facilities, and unique selling points to help buyers make decisions.</p>
              </div>

              <div class="tip-card">
                <div class="tip-number">4</div>
                <h3>Quick Responses</h3>
                <p>Respond to inquiries within 24 hours. Fast communication leads to higher conversion rates.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, h } from 'vue';

export default {
  name: 'SellerView',
  setup() {
    // Admin check (for testing, always true - replace with real auth)
    const isAdmin = ref(true); // TODO: Replace with actual seller/admin auth check
    
    // Stats data
    const stats = ref({
      totalListings: 12,
      activeListings: 8,
      pendingListings: 2,
      totalViews: 3847,
      unreadMessages: 5
    });

//     onMounted(async () => {
//   // Fetch seller stats
//   const response = await fetch('/api/seller/stats');
//   const data = await response.json();
//   stats.value = data;

//   // Fetch recent activity
//   const activityResponse = await fetch('/api/seller/activity');
//   const activityData = await activityResponse.json();
//   recentActivity.value = activityData;
// });
    // Recent activity
    const recentActivity = ref([
      {
        id: 1,
        type: 'view',
        message: 'Your property "Modern Downtown Apartment" received 24 new views',
        timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000) // 2 hours ago
      },
      {
        id: 2,
        type: 'inquiry',
        message: 'New inquiry received for "Luxury Villa with Pool"',
        timestamp: new Date(Date.now() - 5 * 60 * 60 * 1000) // 5 hours ago
      },
      {
        id: 3,
        type: 'favorite',
        message: '3 users added "Cozy Family Home" to their favorites',
        timestamp: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000) // 1 day ago
      },
      {
        id: 4,
        type: 'update',
        message: 'You updated the listing "Beach House Retreat"',
        timestamp: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000) // 2 days ago
      },
      {
        id: 5,
        type: 'status',
        message: '"Mountain Cabin" status changed to Pending',
        timestamp: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000) // 3 days ago
      }
    ]);

    // Format number with commas
    const formatNumber = (num) => {
      return num.toLocaleString();
    };

    // Format time ago
    const formatTimeAgo = (date) => {
      const now = new Date();
      const diff = now - date;
      const seconds = Math.floor(diff / 1000);
      const minutes = Math.floor(seconds / 60);
      const hours = Math.floor(minutes / 60);
      const days = Math.floor(hours / 24);

      if (days > 0) {
        return `${days} day${days > 1 ? 's' : ''} ago`;
      } else if (hours > 0) {
        return `${hours} hour${hours > 1 ? 's' : ''} ago`;
      } else if (minutes > 0) {
        return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
      } else {
        return 'Just now';
      }
    };

    // Get activity icon component
    const getActivityIcon = (type) => {
      const icons = {
        view: () => h('svg', {
          xmlns: 'http://www.w3.org/2000/svg',
          width: '20',
          height: '20',
          viewBox: '0 0 24 24',
          fill: 'none',
          stroke: 'currentColor',
          'stroke-width': '2',
          'stroke-linecap': 'round',
          'stroke-linejoin': 'round'
        }, [
          h('path', { d: 'M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z' }),
          h('circle', { cx: '12', cy: '12', r: '3' })
        ]),
        inquiry: () => h('svg', {
          xmlns: 'http://www.w3.org/2000/svg',
          width: '20',
          height: '20',
          viewBox: '0 0 24 24',
          fill: 'none',
          stroke: 'currentColor',
          'stroke-width': '2',
          'stroke-linecap': 'round',
          'stroke-linejoin': 'round'
        }, [
          h('path', { d: 'M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z' })
        ]),
        favorite: () => h('svg', {
          xmlns: 'http://www.w3.org/2000/svg',
          width: '20',
          height: '20',
          viewBox: '0 0 24 24',
          fill: 'currentColor',
          stroke: 'currentColor',
          'stroke-width': '2',
          'stroke-linecap': 'round',
          'stroke-linejoin': 'round'
        }, [
          h('path', { d: 'M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z' })
        ]),
        update: () => h('svg', {
          xmlns: 'http://www.w3.org/2000/svg',
          width: '20',
          height: '20',
          viewBox: '0 0 24 24',
          fill: 'none',
          stroke: 'currentColor',
          'stroke-width': '2',
          'stroke-linecap': 'round',
          'stroke-linejoin': 'round'
        }, [
          h('path', { d: 'M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7' }),
          h('path', { d: 'M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z' })
        ]),
        status: () => h('svg', {
          xmlns: 'http://www.w3.org/2000/svg',
          width: '20',
          height: '20',
          viewBox: '0 0 24 24',
          fill: 'none',
          stroke: 'currentColor',
          'stroke-width': '2',
          'stroke-linecap': 'round',
          'stroke-linejoin': 'round'
        }, [
          h('circle', { cx: '12', cy: '12', r: '10' }),
          h('polyline', { points: '12 6 12 12 16 14' })
        ])
      };

      return icons[type] || icons.view;
    };

    // Show analytics (placeholder)
    const showAnalytics = () => {
      alert('Analytics feature coming soon! This will show detailed metrics about your listings.');
    };

    // Show messages (placeholder)
    const showMessages = () => {
      alert('Messages feature coming soon! You have ' + stats.value.unreadMessages + ' unread messages.');
    };

    // Fetch stats on mount (in real app, this would be an API call)
    onMounted(() => {
      // Simulate fetching stats
      console.log('Seller dashboard mounted');
    });

    return {
      isAdmin,
      stats,
      recentActivity,
      formatNumber,
      formatTimeAgo,
      getActivityIcon,
      showAnalytics,
      showMessages
    };
  }
};
</script>

<style scoped>
.seller-view {
  min-height: 100vh;
  background-color: var(--color-background);
}

/* Hero Section */
.seller-hero {
  position: relative;
  height: 250px;
  background: linear-gradient(135deg, var(--color-primary-dark) 0%, var(--color-primary) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(228, 169, 93, 0.9) 0%, rgba(255, 195, 96, 0.8) 100%);
}

.hero-content {
  position: relative;
  z-index: 10;
  text-align: center;
  color: var(--color-white);
}

.hero-title {
  font-size: var(--font-size-4xl);
  font-weight: var(--font-weight-bold);
  margin-bottom: var(--spacing-sm);
  text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.2);
}

.hero-subtitle {
  font-size: var(--font-size-lg);
  margin: 0;
  opacity: 0.95;
}

/* Content */
.seller-content {
  padding: var(--spacing-3xl) 0;
}

/* Access Denied */
.access-denied {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-5xl);
  text-align: center;
  background-color: var(--color-white);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-card);
  max-width: 600px;
  margin: 0 auto;
}

.access-denied svg {
  color: var(--color-accent);
  margin-bottom: var(--spacing-lg);
}

.access-denied h2 {
  font-size: var(--font-size-3xl);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-md);
}

.access-denied p {
  font-size: var(--font-size-lg);
  color: var(--color-text-secondary);
  margin-bottom: var(--spacing-md);
}

.contact-text {
  font-size: var(--font-size-base);
  color: var(--color-text-tertiary);
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-xl);
  margin-bottom: var(--spacing-3xl);
}

.stat-card {
  background-color: var(--color-white);
  padding: var(--spacing-xl);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-card);
  display: flex;
  align-items: center;
  gap: var(--spacing-lg);
  transition: all var(--transition-base);
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-card-hover);
}

.stat-icon {
  width: 64px;
  height: 64px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: var(--font-size-3xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-xs) 0;
}

.stat-label {
  font-size: var(--font-size-base);
  color: var(--color-text-secondary);
  margin: 0;
}

/* Quick Actions */
.quick-actions-section {
  margin-bottom: var(--spacing-3xl);
}

.section-title {
  font-size: var(--font-size-2xl);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-xl);
  font-weight: var(--font-weight-semibold);
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--spacing-xl);
}

.action-card {
  position: relative;
  background-color: var(--color-white);
  padding: var(--spacing-2xl);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-card);
  text-decoration: none;
  transition: all var(--transition-base);
  border: 2px solid transparent;
}

.action-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-card-hover);
  border-color: var(--color-primary);
  text-decoration: none;
}

.action-card.clickable {
  cursor: pointer;
}

.action-icon {
  width: 80px;
  height: 80px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: var(--spacing-lg);
}

.action-icon.add {
  background-color: var(--color-primary-light);
  color: var(--color-primary-dark);
}

.action-icon.list {
  background-color: #e3f2fd;
  color: #1976d2;
}

.action-icon.analytics {
  background-color: #f3e5f5;
  color: #7b1fa2;
}

.action-icon.messages {
  background-color: #e8f5e9;
  color: #388e3c;
}

.action-card h3 {
  font-size: var(--font-size-xl);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-sm);
}

.action-card p {
  font-size: var(--font-size-base);
  color: var(--color-text-secondary);
  margin: 0;
}

.action-arrow {
  position: absolute;
  top: var(--spacing-lg);
  right: var(--spacing-lg);
  font-size: var(--font-size-2xl);
  color: var(--color-primary);
  font-weight: var(--font-weight-bold);
  opacity: 0;
  transition: all var(--transition-base);
}

.action-card:hover .action-arrow {
  opacity: 1;
  transform: translateX(4px);
}

.notification-badge {
  position: absolute;
  top: var(--spacing-lg);
  right: var(--spacing-lg);
  background-color: var(--color-accent);
  color: var(--color-white);
  width: 28px;
  height: 28px;
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-bold);
}

/* Recent Activity */
.recent-activity-section {
  margin-bottom: var(--spacing-3xl);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-xl);
}

.view-all-link {
  font-size: var(--font-size-base);
  color: var(--color-primary-dark);
  text-decoration: none;
  font-weight: var(--font-weight-medium);
  transition: color var(--transition-base);
}

.view-all-link:hover {
  color: var(--color-primary);
  text-decoration: none;
}

.activity-list {
  background-color: var(--color-white);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-card);
  overflow: hidden;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-lg);
  padding: var(--spacing-lg) var(--spacing-xl);
  border-bottom: 1px solid var(--color-border);
  transition: background-color var(--transition-base);
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-item:hover {
  background-color: var(--color-cream);
}

.activity-icon {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.activity-icon.view {
  background-color: #e3f2fd;
  color: #1976d2;
}

.activity-icon.inquiry {
  background-color: #e8f5e9;
  color: #388e3c;
}

.activity-icon.favorite {
  background-color: #fce4ec;
  color: #c2185b;
}

.activity-icon.update {
  background-color: #fff3e0;
  color: #f57c00;
}

.activity-icon.status {
  background-color: #f3e5f5;
  color: #7b1fa2;
}

.activity-content {
  flex: 1;
}

.activity-text {
  font-size: var(--font-size-base);
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-xs) 0;
}

.activity-time {
  font-size: var(--font-size-sm);
  color: var(--color-text-tertiary);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-5xl);
  background-color: var(--color-white);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-card);
}

.empty-state svg {
  color: var(--color-text-tertiary);
  margin-bottom: var(--spacing-md);
}

.empty-state p {
  font-size: var(--font-size-lg);
  color: var(--color-text-secondary);
  margin: 0;
}

/* Tips Section */
.tips-section {
  margin-top: var(--spacing-3xl);
}

.tips-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-xl);
}

.tip-card {
  background-color: var(--color-white);
  padding: var(--spacing-2xl);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-card);
  position: relative;
  border-left: 4px solid var(--color-primary);
}

.tip-number {
  position: absolute;
  top: var(--spacing-lg);
  right: var(--spacing-lg);
  width: 40px;
  height: 40px;
  border-radius: var(--radius-full);
  background-color: var(--color-primary-light);
  color: var(--color-primary-dark);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
}

.tip-card h3 {
  font-size: var(--font-size-lg);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-sm);
  padding-right: var(--spacing-3xl);
}

.tip-card p {
  font-size: var(--font-size-base);
  color: var(--color-text-secondary);
  margin: 0;
  line-height: 1.6;
}

/* Responsive */
@media (max-width: 768px) {
  .hero-title {
    font-size: var(--font-size-3xl);
  }

  .hero-subtitle {
    font-size: var(--font-size-base);
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .actions-grid {
    grid-template-columns: 1fr;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-md);
  }

  .tips-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .seller-hero {
    height: 200px;
  }

  .hero-title {
    font-size: var(--font-size-2xl);
  }

  .stat-card {
    flex-direction: column;
    text-align: center;
  }

  .action-card {
    padding: var(--spacing-lg);
  }

  .action-icon {
    width: 60px;
    height: 60px;
  }
}
</style>