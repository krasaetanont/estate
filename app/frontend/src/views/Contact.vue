<template>
  <div class="contact-page">
    <section class="contact-header">
      <div class="container">
        <h1>Get in Touch</h1>
        <p>Have questions about a property? Our team is here to help you every step of the way.</p>
      </div>
    </section>

    <div class="container">
      <div class="contact-grid">
        <div class="contact-card form-section">
          <h2>Send us a Message</h2>
          <form @submit.prevent="handleSubmit">
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">First Name</label>
                <input type="text" v-model="form.firstName" class="form-input" placeholder="Jane" required />
              </div>
              <div class="form-group">
                <label class="form-label">Last Name</label>
                <input type="text" v-model="form.lastName" class="form-input" placeholder="Doe" required />
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">Email Address</label>
              <input type="email" v-model="form.email" class="form-input" placeholder="jane@example.com" required />
            </div>

            <div class="form-group">
              <label class="form-label">Subject</label>
              <select v-model="form.subject" class="form-input">
                <option value="general">General Inquiry</option>
                <option value="buying">Buying a Property</option>
                <option value="selling">Selling a Property</option>
                <option value="support">Technical Support</option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label">Message</label>
              <textarea v-model="form.message" class="form-input" rows="5" placeholder="How can we help you?" required></textarea>
            </div>

            <button type="submit" class="btn btn-primary btn-full" :disabled="isSubmitting">
              {{ isSubmitting ? 'Sending...' : 'Send Message' }}
            </button>
          </form>
        </div>

        <div class="info-section">
          <div class="contact-card info-card">
            <h3>Contact Information</h3>
            <div class="info-list">
              <div class="info-item">
                <span class="info-icon">📍</span>
                <div>
                  <p class="info-title">Office Address</p>
                  <p>123 Real Estate Blvd, Suite 100<br>San Francisco, CA 94105</p>
                </div>
              </div>
              <div class="info-item">
                <span class="info-icon">📞</span>
                <div>
                  <p class="info-title">Phone Number</p>
                  <p>+1 (555) 123-4567</p>
                </div>
              </div>
              <div class="info-item">
                <span class="info-icon">✉️</span>
                <div>
                  <p class="info-title">Email Us</p>
                  <p>hello@estatematch.com</p>
                </div>
              </div>
            </div>
          </div>

          <div class="image-placeholder map-holder">
            <div class="placeholder-content">
              <i class="icon">🗺️</i>
              <span>Map or Office Photo Placeholder</span>
              <p class="placeholder-hint">Tip: Replace this div with a Google Maps iframe or an &lt;img&gt; tag</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'

const isSubmitting = ref(false)
const form = reactive({
  firstName: '',
  lastName: '',
  email: '',
  subject: 'general',
  message: ''
})

const handleSubmit = async () => {
  isSubmitting.value = true
  // Mock API call
  setTimeout(() => {
    alert('Thank you! Your message has been sent.')
    isSubmitting.value = false
    // Reset form
    form.firstName = ''
    form.lastName = ''
    form.email = ''
    form.message = ''
  }, 1500)
}
</script>

<style scoped>
.contact-page {
  background-color: var(--color-gray-50);
  padding-bottom: var(--spacing-2xl);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--spacing-md);
}

.contact-header {
  background-color: var(--color-white);
  padding: 60px 0;
  text-align: center;
  border-bottom: 1px solid var(--color-border);
  margin-bottom: var(--spacing-2xl);
}

.contact-header h1 {
  font-size: 2.5rem;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-xs);
}

.contact-header p {
  color: var(--color-text-secondary);
  font-size: 1.1rem;
}

.contact-grid {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: var(--spacing-xl);
  align-items: start;
}

.contact-card {
  background: var(--color-white);
  padding: var(--spacing-xl);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-md);
}

.info-section {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xl);
}

.info-card h3 {
  margin-bottom: var(--spacing-lg);
  font-size: 1.25rem;
}

.info-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.info-item {
  display: flex;
  gap: var(--spacing-md);
}

.info-icon {
  font-size: 1.5rem;
}

.info-title {
  font-weight: var(--font-weight-bold);
  color: var(--color-text-primary);
  margin-bottom: 2px;
}

/* Placeholder Styling */
.image-placeholder {
  background-color: #e2e8f0;
  border: 2px dashed #cbd5e1;
  border-radius: var(--radius-lg);
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: #64748b;
  padding: var(--spacing-md);
}

.placeholder-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.icon {
  font-size: 2.5rem;
  font-style: normal;
}

.placeholder-hint {
  font-size: 0.75rem;
  margin-top: 10px;
  opacity: 0.8;
}

@media (max-width: 992px) {
  .contact-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 600px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>