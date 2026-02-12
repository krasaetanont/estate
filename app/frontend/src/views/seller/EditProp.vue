<template>
  <div class="edit-property-view">

    <!-- Breadcrumb -->
    <div class="container">
      <nav class="breadcrumb">
        <RouterLink to="/seller">Dashboard</RouterLink>
        <span class="sep">›</span>
        <RouterLink to="/seller/my-listings">My Listings</RouterLink>
        <span class="sep">›</span>
        <span class="current">Edit Property</span>
      </nav>
    </div>

    <!-- Page Header -->
    <div class="page-header">
      <div class="container">
        <div class="header-content">
          <div>
            <h1 class="page-title">
              Edit Property
              <span v-if="!pageLoading && formData.title" class="title-preview">
                — {{ formData.title }}
              </span>
            </h1>
            <p class="page-subtitle">ID #{{ propertyId }} · Last saved {{ lastSaved || 'never' }}</p>
          </div>
          <div class="header-actions">
            <a
              :href="`/properties/${propertyId}`"
              target="_blank"
              class="btn btn-ghost"
              title="View live listing"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24"
                fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                <polyline points="15 3 21 3 21 9"></polyline>
                <line x1="10" y1="14" x2="21" y2="3"></line>
              </svg>
              View Live
            </a>
            <RouterLink to="/seller/my-listings" class="btn btn-ghost">
              ← My Listings
            </RouterLink>
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
        <p>Only sellers and administrators can edit properties.</p>
        <RouterLink to="/seller" class="btn btn-primary">Return to Dashboard</RouterLink>
      </div>

      <!-- Page Loading -->
      <div v-else-if="pageLoading" class="page-loading">
        <div class="spinner"></div>
        <p>Loading property data...</p>
      </div>

      <!-- Not Found -->
      <div v-else-if="notFound" class="not-found">
        <svg xmlns="http://www.w3.org/2000/svg" width="72" height="72" viewBox="0 0 24 24"
          fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
          <polyline points="9 22 9 12 15 12 15 22"></polyline>
        </svg>
        <h2>Property Not Found</h2>
        <p>The property with ID #{{ propertyId }} doesn't exist or was deleted.</p>
        <RouterLink to="/seller/my-listings" class="btn btn-primary">Back to My Listings</RouterLink>
      </div>

      <!-- Form -->
      <div v-else class="form-layout">

        <!-- Alerts -->
        <div v-if="successMessage" class="alert alert-success">
          <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24"
            fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
            <polyline points="22 4 12 14.01 9 11.01"></polyline>
          </svg>
          <div><strong>Saved!</strong><p>{{ successMessage }}</p></div>
        </div>

        <div v-if="errorMessage" class="alert alert-error">
          <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24"
            fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          <div><strong>Error</strong><p>{{ errorMessage }}</p></div>
        </div>

        <!-- Unsaved Changes Banner -->
        <div v-if="hasUnsavedChanges" class="unsaved-banner">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24"
            fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          <span>You have unsaved changes.</span>
          <button @click="revertChanges" class="revert-btn">Revert</button>
        </div>

        <form @submit.prevent="handleSubmit" class="property-form">

          <!-- ══ SECTION: Photos ══════════════════════════════ -->
          <div class="form-section">
            <div class="section-header-row">
              <div>
                <h3 class="section-title">Property Photos</h3>
                <p class="section-desc">
                  First photo is the primary listing image. Drag to reorder.
                </p>
              </div>
              <span class="photo-counter" :class="{ full: photos.length >= 10 }">
                {{ photos.length }} / 10
              </span>
            </div>

            <!-- Existing + New Photos Grid -->
            <div
              class="photo-grid"
              @dragover.prevent
              @drop.prevent="onDropReorder"
            >
              <div
                v-for="(photo, index) in photos"
                :key="photo.id || photo.preview"
                class="photo-item"
                :class="{
                  'photo-primary': index === 0,
                  'photo-new': photo.isNew,
                  'photo-dragging': dragIndex === index
                }"
                draggable="true"
                @dragstart="onDragStart(index)"
                @dragenter.prevent="onDragEnter(index)"
                @dragend="onDragEnd"
              >
                <img :src="photo.preview || photo.url" :alt="`Photo ${index + 1}`" />

                <!-- Overlays -->
                <div class="photo-overlay">
                  <span v-if="index === 0" class="badge-primary">Primary</span>
                  <span v-if="photo.isNew" class="badge-new">New</span>
                  <div class="photo-tools">
                    <button
                      type="button"
                      class="photo-tool drag-handle"
                      title="Drag to reorder"
                    >⠿</button>
                    <button
                      type="button"
                      class="photo-tool remove-photo"
                      @click="removePhoto(index)"
                      title="Remove photo"
                    >✕</button>
                  </div>
                </div>
              </div>

              <!-- Upload Slot -->
              <label v-if="photos.length < 10" class="photo-upload-slot">
                <input
                  type="file"
                  ref="fileInput"
                  @change="handleFileSelect"
                  accept="image/*"
                  multiple
                  class="file-input"
                />
                <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24"
                  fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                  <polyline points="17 8 12 3 7 8"></polyline>
                  <line x1="12" y1="3" x2="12" y2="15"></line>
                </svg>
                <span>Add Photos</span>
              </label>
            </div>
          </div>

          <!-- ══ SECTION: Basic Info ═════════════════════════ -->
          <div class="form-section">
            <h3 class="section-title">Basic Information</h3>
            <div class="form-grid">

              <!-- Title -->
              <div class="form-group full-width">
                <label class="form-label">Title <span class="req">*</span></label>
                <input
                  v-model="formData.title"
                  type="text"
                  class="form-input"
                  :class="{ 'has-error': errors.title }"
                  placeholder="e.g., Modern 3-Bedroom House with Pool"
                />
                <span v-if="errors.title" class="error-msg">{{ errors.title }}</span>
              </div>

              <!-- Property Type -->
              <div class="form-group">
                <label class="form-label">Property Type <span class="req">*</span></label>
                <select
                  v-model="formData.property_type"
                  class="form-select"
                  :class="{ 'has-error': errors.property_type }"
                >
                  <option value="">Select type</option>
                  <option value="house">House</option>
                  <option value="apartment">Apartment</option>
                  <option value="land">Land</option>
                </select>
                <span v-if="errors.property_type" class="error-msg">{{ errors.property_type }}</span>
              </div>

              <!-- Status -->
              <div class="form-group">
                <label class="form-label">Status <span class="req">*</span></label>
                <select v-model="formData.status" class="form-select status-select" :class="formData.status">
                  <option value="available">Available</option>
                  <option value="pending">Pending</option>
                  <option value="sold">Sold</option>
                </select>
              </div>

              <!-- Price -->
              <div class="form-group">
                <label class="form-label">Price (USD) <span class="req">*</span></label>
                <div class="input-group">
                  <span class="prefix">$</span>
                  <input
                    v-model.number="formData.price"
                    type="number"
                    class="form-input with-prefix"
                    :class="{ 'has-error': errors.price }"
                    placeholder="425000"
                    min="0"
                    step="1000"
                  />
                </div>
                <span v-if="errors.price" class="error-msg">{{ errors.price }}</span>
              </div>

              <!-- Area -->
              <div class="form-group">
                <label class="form-label">Area (m²) <span class="req">*</span></label>
                <input
                  v-model.number="formData.area_sqm"
                  type="number"
                  class="form-input"
                  :class="{ 'has-error': errors.area_sqm }"
                  placeholder="150"
                  min="1"
                />
                <span v-if="errors.area_sqm" class="error-msg">{{ errors.area_sqm }}</span>
              </div>

              <!-- Bedrooms -->
              <div class="form-group">
                <label class="form-label">Bedrooms</label>
                <input
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
                <label class="form-label">Bathrooms</label>
                <input
                  v-model.number="formData.bathrooms"
                  type="number"
                  class="form-input"
                  placeholder="2"
                  min="0"
                  max="20"
                  step="0.5"
                />
              </div>

              <!-- Description -->
              <div class="form-group full-width">
                <label class="form-label">Description</label>
                <textarea
                  v-model="formData.description"
                  class="form-textarea"
                  rows="5"
                  maxlength="2000"
                  placeholder="Describe the property in detail..."
                ></textarea>
                <span class="char-count" :class="{ 'char-warn': formData.description.length > 1800 }">
                  {{ formData.description.length }} / 2000
                </span>
              </div>

            </div>
          </div>

          <!-- ══ SECTION: Location ═══════════════════════════ -->
          <div class="form-section">
            <h3 class="section-title">Location</h3>
            <div class="form-grid">

              <div class="form-group">
                <label class="form-label">City <span class="req">*</span></label>
                <input
                  v-model="locationData.city"
                  type="text"
                  class="form-input"
                  :class="{ 'has-error': errors.city }"
                  placeholder="Los Angeles"
                />
                <span v-if="errors.city" class="error-msg">{{ errors.city }}</span>
              </div>

              <div class="form-group">
                <label class="form-label">State / Province</label>
                <input
                  v-model="locationData.province"
                  type="text"
                  class="form-input"
                  placeholder="California"
                />
              </div>

              <div class="form-group">
                <label class="form-label">Country <span class="req">*</span></label>
                <input
                  v-model="locationData.country"
                  type="text"
                  class="form-input"
                  :class="{ 'has-error': errors.country }"
                  placeholder="United States"
                />
                <span v-if="errors.country" class="error-msg">{{ errors.country }}</span>
              </div>

              <div class="form-group">
                <label class="form-label">Postal Code</label>
                <input
                  v-model="locationData.postal_code"
                  type="text"
                  class="form-input"
                  placeholder="90001"
                />
              </div>

              <div class="form-group full-width">
                <label class="form-label">
                  Google Maps Link
                  <span class="optional">(optional)</span>
                </label>
                <input
                  v-model="locationData.google_maps_link"
                  type="url"
                  class="form-input"
                  placeholder="https://maps.google.com/..."
                />
                <span class="input-hint">
                  <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24"
                    fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"></circle>
                    <path d="M12 16v-4"></path>
                    <path d="M12 8h.01"></path>
                  </svg>
                  Right-click the pin in Google Maps → Share → Copy link
                </span>
              </div>

            </div>
          </div>

          <!-- ══ SECTION: Danger Zone ═══════════════════════ -->
          <div class="form-section danger-zone">
            <h3 class="section-title danger-title">Danger Zone</h3>
            <p class="section-desc">
              Deleting a property is permanent and cannot be undone. All photos and
              location data linked to this listing will also be removed.
            </p>
            <button
              type="button"
              @click="showDeleteModal = true"
              class="btn btn-danger-outline"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24"
                fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="3 6 5 6 21 6"></polyline>
                <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"></path>
                <path d="M10 11v6"></path>
                <path d="M14 11v6"></path>
                <path d="M9 6V4h6v2"></path>
              </svg>
              Delete This Property
            </button>
          </div>

          <!-- ══ Form Actions ════════════════════════════════ -->
          <div class="form-actions">
            <RouterLink to="/seller/my-listings" class="btn btn-secondary btn-lg">
              Cancel
            </RouterLink>
            <div class="right-actions">
              <span v-if="hasUnsavedChanges" class="unsaved-dot">● Unsaved</span>
              <button
                type="submit"
                class="btn btn-primary btn-lg"
                :disabled="submitting || !hasUnsavedChanges"
              >
                <span v-if="!submitting">
                  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24"
                    fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                    style="margin-right:6px;">
                    <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
                    <polyline points="17 21 17 13 7 13 7 21"></polyline>
                    <polyline points="7 3 7 8 15 8"></polyline>
                  </svg>
                  Save Changes
                </span>
                <span v-else class="saving-state">
                  <span class="spinner-sm"></span>
                  Saving...
                </span>
              </button>
            </div>
          </div>

        </form>
      </div>
    </div>

    <!-- ══ Delete Confirmation Modal ══════════════════════════ -->
    <Transition name="modal">
      <div v-if="showDeleteModal" class="modal-overlay" @click.self="showDeleteModal = false">
        <div class="modal">
          <div class="modal-danger-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24"
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
            This will permanently delete
            <strong>"{{ formData.title }}"</strong>
            (ID #{{ propertyId }}) and all associated photos. This cannot be undone.
          </p>
          <p class="modal-confirm-label">Type the property title to confirm:</p>
          <input
            v-model="deleteConfirmText"
            type="text"
            class="form-input modal-confirm-input"
            :placeholder="formData.title"
          />
          <div class="modal-actions">
            <button @click="showDeleteModal = false; deleteConfirmText = ''" class="btn btn-secondary">
              Cancel
            </button>
            <button
              @click="deleteProperty"
              class="btn btn-danger"
              :disabled="deleteConfirmText !== formData.title || deletingProperty"
            >
              <span v-if="!deletingProperty">Delete Forever</span>
              <span v-else>Deleting...</span>
            </button>
          </div>
        </div>
      </div>
    </Transition>

  </div>
</template>

<script>
import { ref, reactive, computed, watch, onMounted, onBeforeUnmount } from 'vue';
import { useRoute, useRouter } from 'vue-router';

export default {
  name: 'EditPropertyView',
  setup() {
    const route  = useRoute();
    const router = useRouter();

    // Admin check — for testing always true
    const isAdmin  = ref(true); // TODO: replace with real auth

    const propertyId   = computed(() => Number(route.params.id));
    const pageLoading  = ref(true);
    const notFound     = ref(false);
    const submitting   = ref(false);
    const successMessage = ref('');
    const errorMessage   = ref('');
    const lastSaved      = ref('');

    // Delete
    const showDeleteModal     = ref(false);
    const deleteConfirmText   = ref('');
    const deletingProperty    = ref(false);

    // Photos
    const photos    = ref([]); // { id?, url?, preview?, file?, isNew }
    const fileInput = ref(null);
    const dragIndex = ref(null);
    const dragOver  = ref(null);

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

    const locationData = reactive({
      city: '',
      province: '',
      country: '',
      postal_code: '',
      google_maps_link: ''
    });

    const errors = reactive({
      title: '',
      price: '',
      property_type: '',
      area_sqm: '',
      city: '',
      country: ''
    });

    // Snapshot to track changes
    let originalSnapshot = '';

    const currentSnapshot = computed(() =>
      JSON.stringify({ ...formData, ...locationData, photos: photos.value.map(p => p.url || p.preview) })
    );

    const hasUnsavedChanges = computed(() =>
      originalSnapshot !== '' && currentSnapshot.value !== originalSnapshot
    );

    // ── Fetch property ─────────────────────────────────────────

    const fetchProperty = async () => {
      pageLoading.value = true;
      notFound.value    = false;
      try {
        const res  = await fetch('/example.json');
        const data = await res.json();

        const property = (data.properties || []).find(p => p.id === propertyId.value);

        if (!property) {
          notFound.value = true;
          return;
        }

        // Populate formData
        formData.title         = property.title || '';
        formData.description   = property.description || '';
        formData.price         = property.price || null;
        formData.property_type = property.property_type || '';
        formData.bedrooms      = property.bedrooms || null;
        formData.bathrooms     = property.bathrooms || null;
        formData.area_sqm      = property.area_sqm || null;
        formData.status        = property.status || 'available';

        // Populate locationData
        const location = (data.locations || []).find(l => l.id === property.location_id);
        if (location) {
          locationData.city             = location.city || '';
          locationData.province         = location.province || '';
          locationData.country          = location.country || '';
          locationData.postal_code      = location.postal_code || '';
          locationData.google_maps_link = location.google_maps_link || '';
        }

        // Build photos array from existing URLs
        photos.value = (property.photo_location || []).map((url, i) => ({
          id: `existing-${i}`,
          url,
          preview: url,
          isNew: false
        }));

        // Take snapshot AFTER populating
        await new Promise(r => setTimeout(r, 50));
        originalSnapshot = currentSnapshot.value;

      } catch (err) {
        console.error('Error loading property:', err);
        errorMessage.value = 'Failed to load property data. Please refresh.';
      } finally {
        pageLoading.value = false;
      }
    };

    // ── Photo Handlers ─────────────────────────────────────────

    const handleFileSelect = (event) => {
      const files = Array.from(event.target.files);
      const remaining = 10 - photos.value.length;

      if (files.length > remaining) {
        errorMessage.value = `You can only add ${remaining} more photo${remaining !== 1 ? 's' : ''}.`;
        setTimeout(() => { errorMessage.value = ''; }, 3000);
      }

      files.slice(0, remaining).forEach(file => {
        if (!file.type.startsWith('image/')) return;
        if (file.size > 10 * 1024 * 1024) {
          errorMessage.value = `${file.name} exceeds 10 MB.`;
          return;
        }
        const reader = new FileReader();
        reader.onload = e => {
          photos.value.push({
            id: `new-${Date.now()}-${Math.random()}`,
            preview: e.target.result,
            file,
            isNew: true
          });
        };
        reader.readAsDataURL(file);
      });

      if (fileInput.value) fileInput.value.value = '';
    };

    const removePhoto = (index) => {
      photos.value.splice(index, 1);
    };

    // Drag-to-reorder
    const onDragStart = (index) => { dragIndex.value = index; };
    const onDragEnter = (index) => { dragOver.value  = index; };
    const onDragEnd   = ()      => {
      if (dragIndex.value !== null && dragOver.value !== null && dragIndex.value !== dragOver.value) {
        const arr  = [...photos.value];
        const item = arr.splice(dragIndex.value, 1)[0];
        arr.splice(dragOver.value, 0, item);
        photos.value = arr;
      }
      dragIndex.value = null;
      dragOver.value  = null;
    };
    const onDropReorder = () => { onDragEnd(); };

    // ── Validation ─────────────────────────────────────────────

    const validate = () => {
      let valid = true;
      Object.keys(errors).forEach(k => { errors[k] = ''; });

      if (!formData.title || formData.title.trim().length < 5) {
        errors.title = 'Title must be at least 5 characters';
        valid = false;
      }
      if (!formData.price || formData.price <= 0) {
        errors.price = 'Please enter a valid price';
        valid = false;
      }
      if (!formData.property_type) {
        errors.property_type = 'Please select a property type';
        valid = false;
      }
      if (!formData.area_sqm || formData.area_sqm <= 0) {
        errors.area_sqm = 'Please enter a valid area';
        valid = false;
      }
      if (!locationData.city || locationData.city.trim().length < 2) {
        errors.city = 'Please enter a valid city';
        valid = false;
      }
      if (!locationData.country || locationData.country.trim().length < 2) {
        errors.country = 'Please enter a valid country';
        valid = false;
      }
      if (photos.value.length === 0) {
        errorMessage.value = 'Please keep at least one photo.';
        valid = false;
      }
      return valid;
    };

    // ── Submit (Save Changes) ───────────────────────────────────

    const handleSubmit = async () => {
      successMessage.value = '';
      errorMessage.value   = '';

      if (!validate()) {
        errorMessage.value = 'Please fix the errors below.';
        window.scrollTo({ top: 0, behavior: 'smooth' });
        return;
      }

      submitting.value = true;
      try {
        // In a real app:
        // 1. Upload any new photos and get URLs
        // 2. PATCH /api/properties/:id  with updated formData + photo_location
        // 3. PATCH /api/locations/:locationId with updated locationData

        const newPhotoUrls = photos.value.map(p =>
          p.isNew
            ? `https://example.com/uploads/prop-${propertyId.value}-${Date.now()}.jpg`
            : p.url
        );

        const payload = {
          id: propertyId.value,
          ...formData,
          photo_location: newPhotoUrls,
          location: { ...locationData }
        };

        console.log('PATCH payload:', payload);

        // Simulate API delay
        await new Promise(r => setTimeout(r, 1200));

        // Commit snapshot so unsaved banner disappears
        originalSnapshot     = currentSnapshot.value;
        lastSaved.value      = new Date().toLocaleTimeString();
        successMessage.value = 'Changes saved successfully!';

        setTimeout(() => { successMessage.value = ''; }, 4000);
        window.scrollTo({ top: 0, behavior: 'smooth' });

      } catch (err) {
        console.error('Error saving:', err);
        errorMessage.value = 'Failed to save changes. Please try again.';
      } finally {
        submitting.value = false;
      }
    };

    // ── Revert ─────────────────────────────────────────────────

    const revertChanges = () => {
      if (!confirm('Revert all unsaved changes?')) return;
      fetchProperty();
    };

    // ── Delete ─────────────────────────────────────────────────

    const deleteProperty = async () => {
      if (deleteConfirmText.value !== formData.title) return;
      deletingProperty.value = true;
      try {
        // In real app: await fetch(`/api/properties/${propertyId.value}`, { method: 'DELETE' })
        await new Promise(r => setTimeout(r, 1000));
        showDeleteModal.value   = false;
        deleteConfirmText.value = '';
        router.push('/seller/my-listings');
      } catch {
        errorMessage.value = 'Failed to delete. Please try again.';
      } finally {
        deletingProperty.value = false;
      }
    };

    // ── Unsaved-changes guard ────────────────────────────────────

    const beforeUnloadHandler = (e) => {
      if (hasUnsavedChanges.value) {
        e.preventDefault();
        e.returnValue = '';
      }
    };

    onMounted(() => {
      fetchProperty();
      window.addEventListener('beforeunload', beforeUnloadHandler);
    });

    onBeforeUnmount(() => {
      window.removeEventListener('beforeunload', beforeUnloadHandler);
    });

    return {
      isAdmin,
      propertyId,
      pageLoading,
      notFound,
      submitting,
      successMessage,
      errorMessage,
      lastSaved,
      hasUnsavedChanges,
      showDeleteModal,
      deleteConfirmText,
      deletingProperty,
      photos,
      fileInput,
      dragIndex,
      formData,
      locationData,
      errors,
      handleFileSelect,
      removePhoto,
      onDragStart,
      onDragEnter,
      onDragEnd,
      onDropReorder,
      handleSubmit,
      revertChanges,
      deleteProperty
    };
  }
};
</script>

<style scoped>
/* ── Base ──────────────────────────────────────────── */
.edit-property-view {
  min-height: 100vh;
  background: var(--color-background);
  padding-bottom: var(--spacing-5xl);
}

/* Breadcrumb */
.breadcrumb {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-lg) 0;
  font-size: var(--font-size-sm);
}
.breadcrumb a {
  color: var(--color-primary-dark);
  text-decoration: none;
  transition: color var(--transition-base);
}
.breadcrumb a:hover { color: var(--color-primary); text-decoration: underline; }
.breadcrumb .sep    { color: var(--color-text-tertiary); }
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
  flex-wrap: wrap;
}
.page-title {
  font-size: var(--font-size-3xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-white);
  margin-bottom: var(--spacing-xs);
  text-shadow: 2px 2px 8px rgba(0,0,0,.2);
}
.title-preview {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-normal);
  opacity: 0.85;
}
.page-subtitle {
  font-size: var(--font-size-sm);
  color: var(--color-white);
  opacity: .8;
  margin: 0;
}
.header-actions {
  display: flex;
  gap: var(--spacing-md);
  flex-wrap: wrap;
}
.page-header .btn-ghost {
  background: rgba(255,255,255,.18);
  color: var(--color-white);
  border: 1px solid rgba(255,255,255,.3);
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}
.page-header .btn-ghost:hover {
  background: rgba(255,255,255,.3);
}

/* States */
.access-denied,
.page-loading,
.not-found {
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
.access-denied svg,
.not-found svg { color: var(--color-text-tertiary); }
.access-denied h2,
.not-found h2 { font-size: var(--font-size-2xl); color: var(--color-text-primary); margin: 0; }
.access-denied p,
.not-found p,
.page-loading p { font-size: var(--font-size-lg); color: var(--color-text-secondary); margin: 0; }

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid var(--color-primary-light);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* Form Layout */
.form-layout { max-width: 980px; margin: 0 auto; }

/* Alerts */
.alert {
  display: flex;
  align-items: flex-start;
  gap: var(--spacing-md);
  padding: var(--spacing-lg);
  border-radius: var(--radius-md);
  margin-bottom: var(--spacing-xl);
}
.alert svg { flex-shrink: 0; margin-top: 2px; }
.alert strong { display: block; margin-bottom: 2px; }
.alert p { margin: 0; }
.alert-success { background: #d4edda; border: 1px solid #c3e6cb; color: #155724; }
.alert-error   { background: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; }

/* Unsaved Banner */
.unsaved-banner {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md) var(--spacing-lg);
  background: #fff3cd;
  border: 1px solid #ffc107;
  border-radius: var(--radius-md);
  margin-bottom: var(--spacing-xl);
  font-size: var(--font-size-sm);
  color: #856404;
}
.unsaved-banner svg { flex-shrink: 0; }
.revert-btn {
  margin-left: auto;
  background: none;
  border: 1px solid #856404;
  color: #856404;
  padding: var(--spacing-xs) var(--spacing-md);
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  transition: all var(--transition-base);
}
.revert-btn:hover { background: #856404; color: var(--color-white); }

/* Form */
.property-form { display: flex; flex-direction: column; gap: var(--spacing-3xl); }

/* Form Sections */
.form-section {
  background: var(--color-white);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-card);
  padding: var(--spacing-2xl) var(--spacing-3xl);
}

.section-header-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--spacing-xl);
}
.section-title {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-xs);
}
.section-desc {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  margin: 0;
}

/* Photo Counter */
.photo-counter {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-secondary);
  background: var(--color-cream);
  padding: var(--spacing-xs) var(--spacing-md);
  border-radius: var(--radius-full);
}
.photo-counter.full { background: #fce4ec; color: #c62828; }

/* Photo Grid */
.photo-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: var(--spacing-md);
}

.photo-item {
  position: relative;
  aspect-ratio: 1;
  border-radius: var(--radius-md);
  overflow: hidden;
  border: 2px solid var(--color-border);
  cursor: grab;
  transition: all var(--transition-base);
}
.photo-item:hover { border-color: var(--color-primary); box-shadow: var(--shadow-card); }
.photo-item.photo-primary { border-color: var(--color-primary); border-width: 3px; }
.photo-item.photo-new { border-color: #388e3c; }
.photo-item.photo-dragging { opacity: 0.5; transform: scale(0.96); }

.photo-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  pointer-events: none;
}

.photo-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: var(--spacing-sm);
  background: linear-gradient(to bottom, rgba(0,0,0,.3) 0%, transparent 40%, transparent 60%, rgba(0,0,0,.25) 100%);
  opacity: 0;
  transition: opacity var(--transition-base);
}
.photo-item:hover .photo-overlay { opacity: 1; }

.badge-primary,
.badge-new {
  display: inline-block;
  padding: 2px var(--spacing-sm);
  border-radius: var(--radius-full);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-bold);
  align-self: flex-start;
}
.badge-primary { background: var(--color-primary); color: var(--color-gray-900); }
.badge-new     { background: #388e3c; color: var(--color-white); }

.photo-tools {
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-xs);
  align-self: flex-end;
}
.photo-tool {
  width: 28px;
  height: 28px;
  border-radius: var(--radius-sm);
  background: rgba(255,255,255,.9);
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  transition: all var(--transition-base);
}
.drag-handle { cursor: grab; }
.remove-photo:hover { background: var(--color-accent); color: var(--color-white); }

/* Upload Slot */
.photo-upload-slot {
  aspect-ratio: 1;
  border: 2px dashed var(--color-border);
  border-radius: var(--radius-md);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  cursor: pointer;
  background: var(--color-cream);
  transition: all var(--transition-base);
  color: var(--color-text-tertiary);
  font-size: var(--font-size-sm);
}
.photo-upload-slot:hover { border-color: var(--color-primary); background: var(--color-primary-light); color: var(--color-primary-dark); }
.file-input { display: none; }

/* Form Grid */
.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--spacing-xl);
}
.form-group { display: flex; flex-direction: column; }
.form-group.full-width { grid-column: 1 / -1; }

.form-label {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-sm);
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
}
.req      { color: var(--color-accent); }
.optional { font-size: var(--font-size-xs); color: var(--color-text-tertiary); font-weight: normal; }

.form-input,
.form-select,
.form-textarea {
  padding: var(--spacing-md);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  font-size: var(--font-size-base);
  font-family: inherit;
  background: var(--color-white);
  transition: all var(--transition-base);
  width: 100%;
  box-sizing: border-box;
}
.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px var(--color-primary-light);
}
.form-input.has-error,
.form-select.has-error { border-color: var(--color-accent); }

.form-textarea {
  resize: vertical;
  min-height: 120px;
}

/* Status select coloring */
.status-select.available { background: #e8f5e9; color: #2e7d32; }
.status-select.pending   { background: #fff3e0; color: #e65100; }
.status-select.sold      { background: #fce4ec; color: #880e4f; }

.input-group { position: relative; display: flex; align-items: center; }
.prefix {
  position: absolute;
  left: var(--spacing-md);
  font-size: var(--font-size-lg);
  color: var(--color-text-secondary);
  font-weight: var(--font-weight-semibold);
  pointer-events: none;
}
.form-input.with-prefix { padding-left: var(--spacing-2xl); }

.char-count {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
  text-align: right;
  margin-top: var(--spacing-xs);
}
.char-count.char-warn { color: #e65100; font-weight: var(--font-weight-semibold); }

.error-msg {
  font-size: var(--font-size-xs);
  color: var(--color-accent);
  margin-top: var(--spacing-xs);
}

.input-hint {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
  margin-top: var(--spacing-xs);
}

/* Danger Zone */
.danger-zone {
  border: 2px solid #ffcdd2;
  background: #fff8f8;
}
.danger-title { color: #c62828; }

.btn-danger-outline {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-md) var(--spacing-xl);
  background: transparent;
  border: 2px solid #c62828;
  color: #c62828;
  border-radius: var(--radius-md);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-semibold);
  cursor: pointer;
  transition: all var(--transition-base);
  margin-top: var(--spacing-lg);
}
.btn-danger-outline:hover { background: #c62828; color: var(--color-white); }

/* Form Actions */
.form-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--color-white);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-card);
  padding: var(--spacing-xl) var(--spacing-3xl);
}
.right-actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-lg);
}
.unsaved-dot {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
  color: #e65100;
}
.saving-state {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}
.spinner-sm {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255,255,255,.3);
  border-top-color: var(--color-white);
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  flex-shrink: 0;
}

/* ── Modal ────────────────────────────────────────── */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,.55);
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
  max-width: 480px;
  width: 100%;
  box-shadow: 0 24px 64px rgba(0,0,0,.3);
  text-align: center;
}
.modal-danger-icon {
  width: 72px;
  height: 72px;
  background: #fce4ec;
  color: #c62828;
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto var(--spacing-xl);
}
.modal-title { font-size: var(--font-size-2xl); color: var(--color-text-primary); margin-bottom: var(--spacing-md); }
.modal-body  { font-size: var(--font-size-base); color: var(--color-text-secondary); line-height: 1.6; margin-bottom: var(--spacing-xl); }
.modal-confirm-label {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-sm);
  text-align: left;
}
.modal-confirm-input { margin-bottom: var(--spacing-xl); }
.modal-actions { display: flex; gap: var(--spacing-md); justify-content: center; }

.btn-danger {
  background: #c62828;
  color: var(--color-white);
  border: none;
  padding: var(--spacing-md) var(--spacing-2xl);
  border-radius: var(--radius-md);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-semibold);
  cursor: pointer;
  transition: background-color var(--transition-base);
}
.btn-danger:hover:not(:disabled) { background: #b71c1c; }
.btn-danger:disabled { opacity: .45; cursor: not-allowed; }

/* Modal Transitions */
.modal-enter-active, .modal-leave-active { transition: opacity .2s ease; }
.modal-enter-from,   .modal-leave-to    { opacity: 0; }
.modal-enter-active .modal { transition: transform .2s ease; }
.modal-enter-from .modal   { transform: scale(.92); }

/* ── Responsive ───────────────────────────────────── */
@media (max-width: 768px) {
  .page-title    { font-size: var(--font-size-2xl); }
  .title-preview { display: none; }
  .header-content { flex-direction: column; align-items: flex-start; }
  .header-actions { width: 100%; }
  .header-actions .btn-ghost { flex: 1; justify-content: center; }

  .form-section { padding: var(--spacing-xl); }
  .form-grid    { grid-template-columns: 1fr; }

  .form-actions {
    flex-direction: column;
    gap: var(--spacing-md);
    align-items: stretch;
  }
  .right-actions { flex-direction: column-reverse; align-items: stretch; }
  .right-actions .btn { width: 100%; justify-content: center; }

  .photo-grid { grid-template-columns: repeat(auto-fill, minmax(110px, 1fr)); }

  .modal { padding: var(--spacing-xl); }
  .modal-actions { flex-direction: column; }
  .modal-actions .btn { width: 100%; }
}

@media (max-width: 480px) {
  .page-header { padding: var(--spacing-xl) 0; }
  .header-actions { flex-direction: column; }
  .photo-grid { grid-template-columns: repeat(3, 1fr); }
  .form-section { padding: var(--spacing-lg); }
}
</style>