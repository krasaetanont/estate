<template>
  <div class="add-property-view">
    <!-- Breadcrumb Navigation -->
    <div class="container">
      <nav class="breadcrumb">
        <RouterLink to="/seller">Dashboard</RouterLink>
        <span class="separator">›</span>
        <span class="current">Add Property</span>
      </nav>
    </div>

    <!-- Page Header -->
    <div class="page-header">
      <div class="container">
        <div class="header-content">
          <div>
            <h1 class="page-title">Add New Property</h1>
            <p class="page-subtitle">List your property and reach thousands of potential buyers</p>
          </div>
          <RouterLink to="/seller/my-listings" class="btn btn-ghost">
            <svg 
              xmlns="http://www.w3.org/2000/svg" 
              width="20" 
              height="20" 
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
            View My Listings
          </RouterLink>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="container">
      <div class="add-property-content">
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
          <p>Only sellers and administrators can add properties.</p>
          <p class="contact-text">Please contact support to become a seller.</p>
          <RouterLink to="/seller" class="btn btn-primary">Return to Dashboard</RouterLink>
        </div>

        <!-- Property Form -->
        <div v-else class="form-wrapper">
          <!-- Success Message -->
          <div v-if="successMessage" class="alert alert-success">
            <svg 
              xmlns="http://www.w3.org/2000/svg" 
              width="24" 
              height="24" 
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
            <div>
              <strong>Success!</strong>
              <p>{{ successMessage }}</p>
            </div>
          </div>

          <!-- Error Message -->
          <div v-if="errorMessage" class="alert alert-error">
            <svg 
              xmlns="http://www.w3.org/2000/svg" 
              width="24" 
              height="24" 
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
            <div>
              <strong>Error</strong>
              <p>{{ errorMessage }}</p>
            </div>
          </div>

          <form @submit.prevent="handleSubmit" class="property-form">
            <!-- Photo Upload Section -->
            <div class="form-section">
              <div class="section-header-inline">
                <div>
                  <h3 class="section-title">Property Photos</h3>
                  <p class="section-description">Upload high-quality photos (max 10)</p>
                </div>
                <span class="required-badge">Required</span>
              </div>
              
              <div class="photo-upload-area">
                <!-- Upload Button -->
                <label class="upload-label">
                  <input 
                    type="file" 
                    ref="fileInput"
                    @change="handleFileSelect" 
                    accept="image/*" 
                    multiple
                    class="file-input"
                  />
                  <div class="upload-box">
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
                      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                      <polyline points="17 8 12 3 7 8"></polyline>
                      <line x1="12" y1="3" x2="12" y2="15"></line>
                    </svg>
                    <p class="upload-text"><strong>Click to upload</strong> or drag and drop</p>
                    <p class="upload-hint">PNG, JPG, WEBP up to 10MB each</p>
                  </div>
                </label>

                <!-- Photo Preview Grid -->
                <div v-if="photos.length > 0" class="photo-preview-grid">
                  <div 
                    v-for="(photo, index) in photos" 
                    :key="index"
                    class="photo-preview-item"
                  >
                    <img :src="photo.preview" :alt="`Property photo ${index + 1}`" />
                    <button 
                      type="button"
                      @click="removePhoto(index)"
                      class="photo-remove-btn"
                      :aria-label="`Remove photo ${index + 1}`"
                    >
                      <svg 
                        xmlns="http://www.w3.org/2000/svg" 
                        width="20" 
                        height="20" 
                        viewBox="0 0 24 24" 
                        fill="none" 
                        stroke="currentColor" 
                        stroke-width="2" 
                        stroke-linecap="round" 
                        stroke-linejoin="round"
                      >
                        <line x1="18" y1="6" x2="6" y2="18"></line>
                        <line x1="6" y1="6" x2="18" y2="18"></line>
                      </svg>
                    </button>
                    <div v-if="index === 0" class="primary-badge">Primary</div>
                  </div>
                </div>

                <p v-if="photos.length > 0" class="photo-count">
                  {{ photos.length }} of 10 photos uploaded
                </p>
              </div>
            </div>

            <!-- Basic Information -->
            <div class="form-section">
              <h3 class="section-title">Basic Information</h3>
              
              <div class="form-grid">
                <!-- Title -->
                <div class="form-group full-width">
                  <label for="title" class="form-label">
                    Property Title <span class="required">*</span>
                  </label>
                  <input 
                    id="title"
                    v-model="formData.title"
                    type="text" 
                    class="form-input"
                    :class="{ 'input-error': errors.title }"
                    placeholder="e.g., Modern 3-Bedroom House with Pool"
                    required
                  />
                  <span v-if="errors.title" class="error-text">{{ errors.title }}</span>
                </div>

                <!-- Property Type -->
                <div class="form-group">
                  <label for="property-type" class="form-label">
                    Property Type <span class="required">*</span>
                  </label>
                  <select 
                    id="property-type"
                    v-model="formData.property_type"
                    class="form-select"
                    :class="{ 'input-error': errors.property_type }"
                    required
                  >
                    <option value="">Select Type</option>
                    <option value="house">House</option>
                    <option value="apartment">Apartment</option>
                    <option value="land">Land</option>
                  </select>
                  <span v-if="errors.property_type" class="error-text">{{ errors.property_type }}</span>
                </div>

                <!-- Price -->
                <div class="form-group">
                  <label for="price" class="form-label">
                    Price (USD) <span class="required">*</span>
                  </label>
                  <div class="input-group">
                    <span class="input-prefix">$</span>
                    <input 
                      id="price"
                      v-model.number="formData.price"
                      type="number" 
                      class="form-input with-prefix"
                      :class="{ 'input-error': errors.price }"
                      placeholder="425000"
                      min="0"
                      step="1000"
                      required
                    />
                  </div>
                  <span v-if="errors.price" class="error-text">{{ errors.price }}</span>
                </div>

                <!-- Bedrooms -->
                <div class="form-group">
                  <label for="bedrooms" class="form-label">Bedrooms</label>
                  <input 
                    id="bedrooms"
                    v-model.number="formData.bedrooms"
                    type="number" 
                    class="form-input"
                    placeholder="3"
                    min="0"
                    max="20"
                  />
                </div>

                <!-- Bathrooms -->
                <div class="form-group">
                  <label for="bathrooms" class="form-label">Bathrooms</label>
                  <input 
                    id="bathrooms"
                    v-model.number="formData.bathrooms"
                    type="number" 
                    class="form-input"
                    placeholder="2"
                    min="0"
                    max="20"
                    step="0.5"
                  />
                </div>

                <!-- Area -->
                <div class="form-group">
                  <label for="area" class="form-label">
                    Area (m²) <span class="required">*</span>
                  </label>
                  <input 
                    id="area"
                    v-model.number="formData.area_sqm"
                    type="number" 
                    class="form-input"
                    :class="{ 'input-error': errors.area_sqm }"
                    placeholder="150"
                    min="1"
                    required
                  />
                  <span v-if="errors.area_sqm" class="error-text">{{ errors.area_sqm }}</span>
                </div>

                <!-- Status -->
                <div class="form-group">
                  <label for="status" class="form-label">
                    Status <span class="required">*</span>
                  </label>
                  <select 
                    id="status"
                    v-model="formData.status"
                    class="form-select"
                    required
                  >
                    <option value="available">Available</option>
                    <option value="pending">Pending</option>
                    <option value="sold">Sold</option>
                  </select>
                </div>

                <!-- Description -->
                <div class="form-group full-width">
                  <label for="description" class="form-label">Description</label>
                  <textarea 
                    id="description"
                    v-model="formData.description"
                    class="form-textarea"
                    rows="5"
                    maxlength="2000"
                    placeholder="Describe your property in detail. Include features, amenities, nearby attractions, etc."
                  ></textarea>
                  <span class="char-count">{{ formData.description.length }} / 2000</span>
                </div>
              </div>
            </div>

            <!-- Location Information -->
            <div class="form-section">
              <h3 class="section-title">Location</h3>
              
              <div class="form-grid">
                <!-- City -->
                <div class="form-group">
                  <label for="city" class="form-label">
                    City <span class="required">*</span>
                  </label>
                  <input 
                    id="city"
                    v-model="locationData.city"
                    type="text" 
                    class="form-input"
                    :class="{ 'input-error': errors.city }"
                    placeholder="Los Angeles"
                    required
                  />
                  <span v-if="errors.city" class="error-text">{{ errors.city }}</span>
                </div>

                <!-- Province/State -->
                <div class="form-group">
                  <label for="province" class="form-label">State/Province</label>
                  <input 
                    id="province"
                    v-model="locationData.province"
                    type="text" 
                    class="form-input"
                    placeholder="California"
                  />
                </div>

                <!-- Country -->
                <div class="form-group">
                  <label for="country" class="form-label">
                    Country <span class="required">*</span>
                  </label>
                  <input 
                    id="country"
                    v-model="locationData.country"
                    type="text" 
                    class="form-input"
                    :class="{ 'input-error': errors.country }"
                    placeholder="United States"
                    required
                  />
                  <span v-if="errors.country" class="error-text">{{ errors.country }}</span>
                </div>

                <!-- Postal Code -->
                <div class="form-group">
                  <label for="postal-code" class="form-label">Postal Code</label>
                  <input 
                    id="postal-code"
                    v-model="locationData.postal_code"
                    type="text" 
                    class="form-input"
                    placeholder="90001"
                  />
                </div>

                <!-- Google Maps Link -->
                <div class="form-group full-width">
                  <label for="maps-link" class="form-label">
                    Google Maps Link
                    <span class="label-hint">(optional)</span>
                  </label>
                  <input 
                    id="maps-link"
                    v-model="locationData.google_maps_link"
                    type="url" 
                    class="form-input"
                    placeholder="https://maps.google.com/..."
                  />
                  <span class="input-hint">
                    <svg 
                      xmlns="http://www.w3.org/2000/svg" 
                      width="14" 
                      height="14" 
                      viewBox="0 0 24 24" 
                      fill="none" 
                      stroke="currentColor" 
                      stroke-width="2" 
                      stroke-linecap="round" 
                      stroke-linejoin="round"
                    >
                      <circle cx="12" cy="12" r="10"></circle>
                      <path d="M12 16v-4"></path>
                      <path d="M12 8h.01"></path>
                    </svg>
                    Right-click on location in Google Maps → Share → Copy link
                  </span>
                </div>
              </div>
            </div>

            <!-- Form Actions -->
            <div class="form-actions">
              <button 
                type="button" 
                @click="saveDraft"
                class="btn btn-ghost btn-lg"
                :disabled="submitting"
              >
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  width="20" 
                  height="20" 
                  viewBox="0 0 24 24" 
                  fill="none" 
                  stroke="currentColor" 
                  stroke-width="2" 
                  stroke-linecap="round" 
                  stroke-linejoin="round"
                >
                  <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
                  <polyline points="17 21 17 13 7 13 7 21"></polyline>
                  <polyline points="7 3 7 8 15 8"></polyline>
                </svg>
                Save Draft
              </button>
              <div class="primary-actions">
                <button 
                  type="button" 
                  @click="resetForm"
                  class="btn btn-secondary btn-lg"
                  :disabled="submitting"
                >
                  Reset
                </button>
                <button 
                  type="submit" 
                  class="btn btn-primary btn-lg"
                  :disabled="submitting || photos.length === 0"
                >
                  <span v-if="!submitting">
                    <svg 
                      xmlns="http://www.w3.org/2000/svg" 
                      width="20" 
                      height="20" 
                      viewBox="0 0 24 24" 
                      fill="none" 
                      stroke="currentColor" 
                      stroke-width="2" 
                      stroke-linecap="round" 
                      stroke-linejoin="round"
                      style="margin-right: 8px;"
                    >
                      <polyline points="9 11 12 14 22 4"></polyline>
                      <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path>
                    </svg>
                    Publish Property
                  </span>
                  <span v-else>
                    <span class="spinner-small"></span>
                    Publishing...
                  </span>
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'AddPropertyView',
  setup() {
    const router = useRouter();
    
    // Admin check (for testing, always true - replace with real auth)
    const isAdmin = ref(true); // TODO: Replace with actual seller/admin auth check
    
    // Form states
    const submitting = ref(false);
    const successMessage = ref('');
    const errorMessage = ref('');
    const fileInput = ref(null);
    
    // Photos array
    const photos = ref([]);
    
    // Form data
    const formData = reactive({
      title: '',
      description: '',
      price: null,
      property_type: '',
      bedrooms: null,
      bathrooms: null,
      area_sqm: null,
      status: 'available'
    });
    
    // Location data
    const locationData = reactive({
      city: '',
      province: '',
      country: '',
      postal_code: '',
      google_maps_link: ''
    });
    
    // Validation errors
    const errors = reactive({
      title: '',
      price: '',
      property_type: '',
      area_sqm: '',
      city: '',
      country: ''
    });
    
    // Handle file selection
    const handleFileSelect = (event) => {
      const files = Array.from(event.target.files);
      
      // Check if adding these files would exceed the limit
      if (photos.value.length + files.length > 10) {
        errorMessage.value = 'You can only upload a maximum of 10 photos.';
        setTimeout(() => { errorMessage.value = ''; }, 3000);
        return;
      }
      
      files.forEach(file => {
        // Validate file type
        if (!file.type.startsWith('image/')) {
          errorMessage.value = `${file.name} is not an image file.`;
          return;
        }
        
        // Validate file size (max 10MB)
        if (file.size > 10 * 1024 * 1024) {
          errorMessage.value = `${file.name} is too large. Maximum size is 10MB.`;
          return;
        }
        
        // Create preview
        const reader = new FileReader();
        reader.onload = (e) => {
          photos.value.push({
            file: file,
            preview: e.target.result,
            name: file.name
          });
        };
        reader.readAsDataURL(file);
      });
      
      // Reset file input
      if (fileInput.value) {
        fileInput.value.value = '';
      }
    };
    
    // Remove photo
    const removePhoto = (index) => {
      photos.value.splice(index, 1);
    };
    
    // Validate form
    const validateForm = () => {
      let isValid = true;
      
      // Reset errors
      Object.keys(errors).forEach(key => {
        errors[key] = '';
      });
      
      // Title validation
      if (!formData.title || formData.title.trim().length < 5) {
        errors.title = 'Title must be at least 5 characters long';
        isValid = false;
      }
      
      // Price validation
      if (!formData.price || formData.price <= 0) {
        errors.price = 'Please enter a valid price';
        isValid = false;
      }
      
      // Property type validation
      if (!formData.property_type) {
        errors.property_type = 'Please select a property type';
        isValid = false;
      }
      
      // Area validation
      if (!formData.area_sqm || formData.area_sqm <= 0) {
        errors.area_sqm = 'Please enter a valid area';
        isValid = false;
      }
      
      // City validation
      if (!locationData.city || locationData.city.trim().length < 2) {
        errors.city = 'Please enter a valid city';
        isValid = false;
      }
      
      // Country validation
      if (!locationData.country || locationData.country.trim().length < 2) {
        errors.country = 'Please enter a valid country';
        isValid = false;
      }
      
      // Photos validation
      if (photos.value.length === 0) {
        errorMessage.value = 'Please upload at least one photo';
        isValid = false;
      }
      
      return isValid;
    };
    
    // Handle form submission
    const handleSubmit = async () => {
      // Clear messages
      successMessage.value = '';
      errorMessage.value = '';
      
      // Validate form
      if (!validateForm()) {
        errorMessage.value = 'Please fix the errors in the form';
        window.scrollTo({ top: 0, behavior: 'smooth' });
        return;
      }
      
      submitting.value = true;
      
      try {
        // Simulate photo upload URLs
        const photoUrls = photos.value.map((photo, index) => 
          `https://example.com/uploads/property-${Date.now()}-${index}.jpg`
        );
        
        // Construct the data that would be sent to API
        const propertyData = {
          ...formData,
          photo_location: photoUrls,
          owner_id: 1, // Mock user ID - replace with actual auth
          location: {
            ...locationData
          },
          created_at: new Date().toISOString()
        };
        
        console.log('Property data to be submitted:', propertyData);
        
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        // Show success message
        successMessage.value = 'Property published successfully!';
        
        // Redirect to my listings after 2 seconds
        setTimeout(() => {
          router.push('/seller/my-listings');
        }, 2000);
        
      } catch (error) {
        console.error('Error submitting property:', error);
        errorMessage.value = 'An error occurred while publishing your property. Please try again.';
      } finally {
        submitting.value = false;
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    };
    
    // Save draft
    const saveDraft = () => {
      // In a real app, this would save to local storage or database
      const draftData = {
        formData: { ...formData },
        locationData: { ...locationData },
        photoCount: photos.value.length,
        savedAt: new Date().toISOString()
      };
      
      localStorage.setItem('property_draft', JSON.stringify(draftData));
      
      successMessage.value = 'Draft saved successfully!';
      setTimeout(() => { successMessage.value = ''; }, 3000);
      
      console.log('Draft saved:', draftData);
    };
    
    // Reset form
    const resetForm = () => {
      if (!confirm('Are you sure you want to reset the form? All unsaved data will be lost.')) {
        return;
      }
      
      // Reset form data
      formData.title = '';
      formData.description = '';
      formData.price = null;
      formData.property_type = '';
      formData.bedrooms = null;
      formData.bathrooms = null;
      formData.area_sqm = null;
      formData.status = 'available';
      
      // Reset location data
      locationData.city = '';
      locationData.province = '';
      locationData.country = '';
      locationData.postal_code = '';
      locationData.google_maps_link = '';
      
      // Reset photos
      photos.value = [];
      
      // Reset errors
      Object.keys(errors).forEach(key => {
        errors[key] = '';
      });
      
      // Clear messages
      successMessage.value = '';
      errorMessage.value = '';
      
      // Scroll to top
      window.scrollTo({ top: 0, behavior: 'smooth' });
    };
    
    return {
      isAdmin,
      submitting,
      successMessage,
      errorMessage,
      fileInput,
      photos,
      formData,
      locationData,
      errors,
      handleFileSelect,
      removePhoto,
      handleSubmit,
      saveDraft,
      resetForm
    };
  }
};
</script>

<style scoped>
.add-property-view {
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

.breadcrumb a:hover {
  color: var(--color-primary);
  text-decoration: underline;
}

.breadcrumb .separator {
  color: var(--color-text-tertiary);
}

.breadcrumb .current {
  color: var(--color-text-secondary);
}

/* Page Header */
.page-header {
  background: linear-gradient(135deg, var(--color-primary-dark) 0%, var(--color-primary) 100%);
  padding: var(--spacing-3xl) 0;
  margin-bottom: var(--spacing-3xl);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-title {
  font-size: var(--font-size-4xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-white);
  margin-bottom: var(--spacing-sm);
  text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.2);
}

.page-subtitle {
  font-size: var(--font-size-lg);
  color: var(--color-white);
  opacity: 0.95;
  margin: 0;
}

.page-header .btn-ghost {
  background-color: rgba(255, 255, 255, 0.2);
  color: var(--color-white);
  border: 1px solid rgba(255, 255, 255, 0.3);
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.page-header .btn-ghost:hover {
  background-color: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.5);
}

/* Content */
.add-property-content {
  max-width: 1000px;
  margin: 0 auto;
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

/* Form Wrapper */
.form-wrapper {
  background-color: var(--color-white);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-card);
  padding: var(--spacing-3xl);
}

/* Form Sections */
.form-section {
  margin-bottom: var(--spacing-3xl);
  padding-bottom: var(--spacing-3xl);
  border-bottom: 1px solid var(--color-border);
}

.form-section:last-of-type {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.section-header-inline {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--spacing-xl);
}

.section-title {
  font-size: var(--font-size-2xl);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-sm);
  font-weight: var(--font-weight-semibold);
}

.section-description {
  font-size: var(--font-size-base);
  color: var(--color-text-secondary);
  margin: 0;
}

.required-badge {
  background-color: var(--color-accent);
  color: var(--color-white);
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--radius-full);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-bold);
}

/* Photo Upload */
.photo-upload-area {
  margin-top: var(--spacing-lg);
}

.upload-label {
  display: block;
  cursor: pointer;
}

.file-input {
  display: none;
}

.upload-box {
  border: 2px dashed var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--spacing-3xl);
  text-align: center;
  transition: all var(--transition-base);
  background-color: var(--color-cream);
}

.upload-box:hover {
  border-color: var(--color-primary);
  background-color: var(--color-primary-light);
}

.upload-box svg {
  color: var(--color-primary);
  margin-bottom: var(--spacing-md);
}

.upload-text {
  font-size: var(--font-size-lg);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-xs);
}

.upload-hint {
  font-size: var(--font-size-sm);
  color: var(--color-text-tertiary);
  margin: 0;
}

/* Photo Preview Grid */
.photo-preview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: var(--spacing-lg);
  margin-top: var(--spacing-xl);
}

.photo-preview-item {
  position: relative;
  aspect-ratio: 1;
  border-radius: var(--radius-md);
  overflow: hidden;
  border: 2px solid var(--color-border);
  transition: all var(--transition-base);
}

.photo-preview-item:hover {
  border-color: var(--color-primary);
  box-shadow: var(--shadow-card);
}

.photo-preview-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.photo-remove-btn {
  position: absolute;
  top: var(--spacing-sm);
  right: var(--spacing-sm);
  width: 32px;
  height: 32px;
  border-radius: var(--radius-full);
  background-color: rgba(255, 255, 255, 0.95);
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-base);
  box-shadow: var(--shadow-sm);
}

.photo-remove-btn:hover {
  background-color: var(--color-accent);
  color: var(--color-white);
  transform: scale(1.1);
}

.primary-badge {
  position: absolute;
  bottom: var(--spacing-sm);
  left: var(--spacing-sm);
  background-color: var(--color-primary);
  color: var(--color-gray-900);
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--radius-sm);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-bold);
}

.photo-count {
  margin-top: var(--spacing-md);
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  text-align: center;
}

/* Form Grid */
.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--spacing-xl);
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-label {
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-sm);
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
}

.required {
  color: var(--color-accent);
}

.label-hint {
  font-size: var(--font-size-sm);
  color: var(--color-text-tertiary);
  font-weight: var(--font-weight-normal);
}

.form-input,
.form-select,
.form-textarea {
  padding: var(--spacing-md);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  font-size: var(--font-size-base);
  font-family: inherit;
  transition: all var(--transition-base);
  background-color: var(--color-white);
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px var(--color-primary-light);
}

.form-input.input-error,
.form-select.input-error {
  border-color: var(--color-accent);
}

.form-input::placeholder,
.form-textarea::placeholder {
  color: var(--color-text-tertiary);
}

.input-group {
  position: relative;
  display: flex;
  align-items: center;
}

.input-prefix {
  position: absolute;
  left: var(--spacing-md);
  font-size: var(--font-size-lg);
  color: var(--color-text-secondary);
  font-weight: var(--font-weight-semibold);
  pointer-events: none;
}

.form-input.with-prefix {
  padding-left: var(--spacing-2xl);
}

.form-textarea {
  resize: vertical;
  min-height: 120px;
}

.char-count {
  font-size: var(--font-size-sm);
  color: var(--color-text-tertiary);
  margin-top: var(--spacing-xs);
  text-align: right;
}

.error-text {
  font-size: var(--font-size-sm);
  color: var(--color-accent);
  margin-top: var(--spacing-xs);
}

.input-hint {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  font-size: var(--font-size-sm);
  color: var(--color-text-tertiary);
  margin-top: var(--spacing-xs);
}

.input-hint svg {
  flex-shrink: 0;
}

/* Form Actions */
.form-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: var(--spacing-3xl);
  padding-top: var(--spacing-xl);
  border-top: 2px solid var(--color-border);
}

.primary-actions {
  display: flex;
  gap: var(--spacing-md);
}

/* Spinner */
.spinner-small {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: var(--color-white);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-right: var(--spacing-sm);
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Alerts */
.alert {
  display: flex;
  align-items: flex-start;
  gap: var(--spacing-md);
  padding: var(--spacing-lg);
  border-radius: var(--radius-md);
  margin-bottom: var(--spacing-xl);
}

.alert svg {
  flex-shrink: 0;
  margin-top: 2px;
}

.alert strong {
  display: block;
  margin-bottom: var(--spacing-xs);
}

.alert p {
  margin: 0;
}

.alert-success {
  background-color: #d4edda;
  border: 1px solid #c3e6cb;
  color: #155724;
}

.alert-error {
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
  color: #721c24;
}

/* Responsive */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-lg);
  }

  .page-title {
    font-size: var(--font-size-3xl);
  }

  .page-subtitle {
    font-size: var(--font-size-base);
  }

  .form-wrapper {
    padding: var(--spacing-xl);
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column;
    align-items: stretch;
    gap: var(--spacing-md);
  }

  .primary-actions {
    flex-direction: column;
    width: 100%;
  }

  .primary-actions .btn {
    width: 100%;
  }

  .photo-preview-grid {
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  }

  .section-header-inline {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-sm);
  }
}

@media (max-width: 480px) {
  .page-header {
    padding: var(--spacing-2xl) 0;
  }

  .page-title {
    font-size: var(--font-size-2xl);
  }

  .form-wrapper {
    padding: var(--spacing-lg);
  }

  .section-title {
    font-size: var(--font-size-xl);
  }
}
</style>