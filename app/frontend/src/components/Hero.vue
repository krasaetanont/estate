<template>
  <section class="hero">
    <div class="hero-content">
      <!-- Text holder -->
      <div class="hero-text">
        <h1>{{ title }}</h1>
        <p>{{ subtitle }}</p>

        <div v-if="$slots.actions" class="hero-actions">
          <slot name="actions" />
        </div>
      </div>

      <!-- Photo holder -->
      <div class="hero-image">
        <img :src="image" :alt="imageAlt" />
      </div>
    </div>
  </section>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  subtitle: {
    type: String,
    default: '',
  },
  image: {
    type: String,
    required: true,
  },
  imageAlt: {
    type: String,
    default: 'Hero image',
  },
});
</script>

<style scoped>
.hero {
  width: 100%;
  padding: 4rem 1.5rem;
  background: linear-gradient(135deg, #f5f7fa, #e4ecf7);
}

.hero-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  gap: 3rem;
  align-items: center;
}

.hero-text {
  flex: 1;
}

.hero-text h1 {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.hero-text p {
  font-size: 1.1rem;
  line-height: 1.6;
  color: #555;
}

.hero-actions {
  margin-top: 1.5rem;
}

.hero-image {
  flex: 1;
  display: flex;
  justify-content: center;
}

.hero-image img {
  width: 100%;
  max-width: 480px;
  border-radius: 16px;
  object-fit: cover;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
}

/* Responsive */
@media (max-width: 900px) {
  .hero-content {
    flex-direction: column-reverse;
    text-align: center;
  }

  .hero-text h1 {
    font-size: 2rem;
  }
}
</style>
