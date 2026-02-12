<template>
  <div class="about-page">
    <section class="about-hero">
      <div class="container">
        <h1>Redefining Real Estate</h1>
        <p>Connecting people with their dream homes since 2024.</p>
      </div>
    </section>

    <section class="mission-section container">
      <div class="mission-grid">
        <div class="mission-text">
          <span class="badge">Our Mission</span>
          <h2>We make finding a home as easy as a single click.</h2>
          <p>
            EstateMatch was founded on the principle that the real estate market should be 
            transparent, accessible, and efficient. We leverage cutting-edge technology 
            to match buyers with the perfect properties based on lifestyle, budget, and future goals.
          </p>
          <div class="stats-row">
            <div class="stat-item">
              <span class="stat-number">10k+</span>
              <span class="stat-label">Properties</span>
            </div>
            <div class="stat-item">
              <span class="stat-number">5k+</span>
              <span class="stat-label">Happy Clients</span>
            </div>
          </div>
        </div>
        
        <div class="image-placeholder main-img">
          <div class="placeholder-content">
            <i class="icon">🖼️</i>
            <span>Main Office Photo</span>
          </div>
        </div>
      </div>
    </section>

    <section class="team-section">
      <div class="container">
        <div class="section-header">
          <h2>Meet Our Leaders</h2>
          <p>The experts behind our seamless property matching experience.</p>
        </div>
        
        <div class="team-grid">
          <div v-for="i in 3" :key="i" class="team-card">
            <div class="image-placeholder team-img">
              <div class="placeholder-content">
                <i class="icon">👤</i>
              </div>
            </div>
            <h3>Team Member {{ i }}</h3>
            <p>Department Lead</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.about-page {
  padding-bottom: var(--spacing-2xl);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--spacing-md);
}

/* Hero Section */
.about-hero {
  background-color: var(--color-primary);
  color: white;
  padding: 100px 0;
  text-align: center;
  margin-bottom: var(--spacing-2xl);
}

.about-hero h1 {
  font-size: 3rem;
  margin-bottom: var(--spacing-sm);
}

/* Mission Section */
.mission-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-2xl);
  align-items: center;
  margin-bottom: var(--spacing-2xl);
}

.badge {
  color: var(--color-primary);
  font-weight: bold;
  text-transform: uppercase;
  font-size: 0.8rem;
  letter-spacing: 1px;
}

.mission-text h2 {
  font-size: 2.5rem;
  margin: var(--spacing-sm) 0;
  line-height: 1.2;
}

.stats-row {
  display: flex;
  gap: var(--spacing-xl);
  margin-top: var(--spacing-lg);
}

.stat-number {
  display: block;
  font-size: 2rem;
  font-weight: bold;
  color: var(--color-primary);
}

/* Team Section */
.team-section {
  background-color: var(--color-gray-50);
  padding: var(--spacing-2xl) 0;
}

.section-header {
  text-align: center;
  margin-bottom: var(--spacing-xl);
}

.team-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-lg);
}

.team-card {
  background: white;
  padding: var(--spacing-md);
  border-radius: var(--radius-lg);
  text-align: center;
  box-shadow: var(--shadow-sm);
}

/* Placeholder Styling */
.image-placeholder {
  background-color: #e2e8f0;
  border: 2px dashed #cbd5e1;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
  position: relative;
  overflow: hidden;
}

.main-img {
  height: 400px;
}

.team-img {
  height: 250px;
  margin-bottom: var(--spacing-md);
}

.placeholder-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.icon {
  font-size: 2rem;
  font-style: normal;
}

@media (max-width: 768px) {
  .mission-grid {
    grid-template-columns: 1fr;
  }
  
  .about-hero h1 {
    font-size: 2rem;
  }
}
</style>