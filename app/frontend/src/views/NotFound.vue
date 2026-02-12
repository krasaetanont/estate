<template>
  <main class="not-found-view">
    <div class="content">
      <div class="error-code">404</div>
      <div class="illustration-placeholder">
        <div class="house-icon">🏠</div>
        <div class="magnifier">🔍</div>
      </div>
      
      <h1>Page Not Found</h1>
      <p>
        Oops! It looks like the property or page you're looking for has moved 
        or doesn't exist anymore. Let's get you back on track.
      </p>

      <div class="actions">
        <RouterLink to="/" class="btn btn-primary">
          Back to Home
        </RouterLink>
        <RouterLink to="/contact" class="btn btn-outline">
          Report an Issue
        </RouterLink>
      </div>
    </div>
  </main>
</template>

<style scoped>
.not-found-view {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 160px); /* Adjust based on header/footer height */
  padding: var(--spacing-xl);
  background-color: var(--color-background-soft);
  text-align: center;
}

.content {
  max-width: 500px;
  width: 100%;
}

.error-code {
  font-size: 6rem;
  font-weight: 800;
  line-height: 1;
  color: var(--color-primary);
  opacity: 0.2;
  margin-bottom: -40px;
}

.illustration-placeholder {
  position: relative;
  font-size: 4rem;
  margin-bottom: var(--spacing-lg);
  display: flex;
  justify-content: center;
  align-items: center;
}

.magnifier {
  position: absolute;
  font-size: 2.5rem;
  bottom: -5px;
  right: 40%;
  animation: search 3s ease-in-out infinite;
}

h1 {
  font-size: var(--font-size-3xl);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-sm);
}

p {
  color: var(--color-text-secondary);
  font-size: 1.1rem;
  margin-bottom: var(--spacing-xl);
  line-height: 1.6;
}

.actions {
  display: flex;
  gap: var(--spacing-md);
  justify-content: center;
}

@keyframes search {
  0%, 100% { transform: translate(0, 0) rotate(0deg); }
  25% { transform: translate(15px, -10px) rotate(15deg); }
  75% { transform: translate(-15px, 5px) rotate(-15deg); }
}

@media (max-width: 480px) {
  .actions {
    flex-direction: column;
  }
  
  .error-code {
    font-size: 4rem;
  }
}
</style>