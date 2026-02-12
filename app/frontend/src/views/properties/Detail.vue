<template>
  <div class="detail-page">

    <!-- Loading State -->
    <div v-if="loading" class="detail-loading">
      <div class="detail-loading__track">
        <div class="detail-loading__bar"></div>
      </div>
      <p class="detail-loading__text">Fetching property…</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="detail-error">
      <span class="detail-error__code">404</span>
      <p class="detail-error__msg">{{ error }}</p>
      <button class="btn btn--ghost" @click="$router.back()">← Go Back</button>
    </div>

    <!-- Property Detail -->
    <template v-else-if="property">

      <!-- ───── Sticky top bar ───── -->
      <header class="detail-topbar">
        <button class="detail-topbar__back" @click="$router.back()">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24"
            fill="none" stroke="currentColor" stroke-width="2.5"
            stroke-linecap="round" stroke-linejoin="round">
            <polyline points="15 18 9 12 15 6"></polyline>
          </svg>
          Back
        </button>

        <div class="detail-topbar__actions">
          <button
            class="detail-topbar__fav"
            :class="{ 'is-fav': favorited }"
            @click="toggleFavorite"
            :aria-label="favorited ? 'Remove from favorites' : 'Add to favorites'"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"
              :fill="favorited ? 'currentColor' : 'none'"
              stroke="currentColor" stroke-width="2"
              stroke-linecap="round" stroke-linejoin="round">
              <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06
                       a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78
                       1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
            </svg>
          </button>

          <button class="detail-topbar__share" @click="handleShare">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24"
              fill="none" stroke="currentColor" stroke-width="2"
              stroke-linecap="round" stroke-linejoin="round">
              <circle cx="18" cy="5" r="3"></circle>
              <circle cx="6" cy="12" r="3"></circle>
              <circle cx="18" cy="19" r="3"></circle>
              <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line>
              <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line>
            </svg>
            Share
          </button>
        </div>
      </header>

      <!-- ───── Image Gallery ───── -->
      <section class="detail-gallery" :class="{ 'detail-gallery--single': !hasMultipleImages }">
        <!-- Main image -->
        <div
          class="detail-gallery__main"
          @click="openLightbox(activeImageIndex)"
        >
          <img
            :src="activeImage"
            :alt="property.title || 'Property image'"
            class="detail-gallery__img"
          />
          <div class="detail-gallery__overlay">
            <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24"
              fill="none" stroke="currentColor" stroke-width="2"
              stroke-linecap="round" stroke-linejoin="round">
              <circle cx="11" cy="11" r="8"></circle>
              <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
              <line x1="11" y1="8" x2="11" y2="14"></line>
              <line x1="8" y1="11" x2="14" y2="11"></line>
            </svg>
            View All Photos
          </div>
          <!-- Status badge -->
          <span class="detail-badge" :class="`detail-badge--${property.status}`">
            {{ formatStatus(property.status) }}
          </span>
        </div>

        <!-- Thumbnail strip -->
        <div v-if="hasMultipleImages" class="detail-gallery__thumbs">
          <button
            v-for="(img, idx) in galleryImages"
            :key="idx"
            class="detail-gallery__thumb"
            :class="{ 'is-active': idx === activeImageIndex }"
            @click="activeImageIndex = idx"
          >
            <img :src="img" :alt="`Photo ${idx + 1}`" />
          </button>
        </div>
      </section>

      <!-- ───── Lightbox ───── -->
      <Teleport to="body">
        <div v-if="lightboxOpen" class="lightbox" @click.self="lightboxOpen = false">
          <button class="lightbox__close" @click="lightboxOpen = false">✕</button>
          <button class="lightbox__prev" @click="lightboxPrev">‹</button>
          <img :src="galleryImages[lightboxIndex]" class="lightbox__img" />
          <button class="lightbox__next" @click="lightboxNext">›</button>
          <p class="lightbox__counter">{{ lightboxIndex + 1 }} / {{ galleryImages.length }}</p>
        </div>
      </Teleport>

      <!-- ───── Main content grid ───── -->
      <div class="detail-body">

        <!-- LEFT: info column -->
        <div class="detail-main">

          <!-- Title & price block -->
          <div class="detail-header">
            <div class="detail-header__top">
              <span v-if="property.property_type" class="detail-type-pill">
                {{ formatType(property.property_type) }}
              </span>
              <span v-if="property.views_count !== undefined" class="detail-views">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24"
                  fill="none" stroke="currentColor" stroke-width="2"
                  stroke-linecap="round" stroke-linejoin="round">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                  <circle cx="12" cy="12" r="3"></circle>
                </svg>
                {{ property.views_count.toLocaleString() }} views
              </span>
            </div>

            <h1 class="detail-title">{{ property.title || 'Untitled Property' }}</h1>

            <div class="detail-location" v-if="location">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"
                fill="none" stroke="currentColor" stroke-width="2"
                stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                <circle cx="12" cy="10" r="3"></circle>
              </svg>
              <span>{{ locationLabel }}</span>
            </div>

            <div class="detail-price-row">
              <span class="detail-price">
                {{ formatPrice(property.price) }}
                <small v-if="forRent">/ mo</small>
              </span>
              <span v-if="property.price_per_sqm" class="detail-price-psm">
                {{ formatPrice(property.price_per_sqm) }} / m²
              </span>
            </div>
          </div>

          <!-- Quick stats strip -->
          <ul class="detail-stats" v-if="hasStats">
            <li v-if="property.bedrooms !== undefined" class="detail-stats__item">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"
                fill="none" stroke="currentColor" stroke-width="1.8"
                stroke-linecap="round" stroke-linejoin="round">
                <path d="M2 20v-8a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v8"></path>
                <path d="M4 10V6a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v4"></path>
                <path d="M12 10v10"></path>
                <path d="M2 16h20"></path>
              </svg>
              <strong>{{ property.bedrooms }}</strong>
              <span>{{ property.bedrooms === 1 ? 'Bedroom' : 'Bedrooms' }}</span>
            </li>
            <li v-if="property.bathrooms !== undefined" class="detail-stats__item">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"
                fill="none" stroke="currentColor" stroke-width="1.8"
                stroke-linecap="round" stroke-linejoin="round">
                <path d="M9 6 6.5 3.5a1.5 1.5 0 0 0-1-.5C4.683 3 4 3.683 4 4.5V17a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-5"></path>
                <line x1="10" y1="5" x2="8" y2="7"></line>
                <line x1="2" y1="12" x2="22" y2="12"></line>
              </svg>
              <strong>{{ property.bathrooms }}</strong>
              <span>{{ property.bathrooms === 1 ? 'Bathroom' : 'Bathrooms' }}</span>
            </li>
            <li v-if="property.area !== undefined" class="detail-stats__item">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"
                fill="none" stroke="currentColor" stroke-width="1.8"
                stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="3" width="18" height="18" rx="2"></rect>
                <path d="M3 9h18M3 15h18M9 3v18M15 3v18"></path>
              </svg>
              <strong>{{ property.area }}</strong>
              <span>m²</span>
            </li>
            <li v-if="property.parking !== undefined" class="detail-stats__item">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"
                fill="none" stroke="currentColor" stroke-width="1.8"
                stroke-linecap="round" stroke-linejoin="round">
                <rect x="1" y="3" width="22" height="18" rx="2" ry="2"></rect>
                <path d="M1 9h22M1 15h22M8 3v18M16 3v18"></path>
              </svg>
              <strong>{{ property.parking }}</strong>
              <span>{{ property.parking === 1 ? 'Parking' : 'Parking spots' }}</span>
            </li>
          </ul>

          <!-- Description -->
          <section v-if="property.description" class="detail-section">
            <h2 class="detail-section__title">About this property</h2>
            <p class="detail-description" :class="{ 'is-truncated': descTruncated }">
              {{ property.description }}
            </p>
            <button
              v-if="descNeedsTruncation"
              class="detail-toggle-desc"
              @click="descTruncated = !descTruncated"
            >
              {{ descTruncated ? 'Read more ↓' : 'Show less ↑' }}
            </button>
          </section>

          <!-- Features / Amenities -->
          <section v-if="features.length" class="detail-section">
            <h2 class="detail-section__title">Features & Amenities</h2>
            <ul class="detail-features">
              <li v-for="feature in features" :key="feature" class="detail-features__item">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24"
                  fill="none" stroke="currentColor" stroke-width="3"
                  stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
                {{ feature }}
              </li>
            </ul>
          </section>

          <!-- Map placeholder -->
          <section v-if="location" class="detail-section">
            <h2 class="detail-section__title">Location</h2>
            <div class="detail-map-placeholder">
              <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24"
                fill="none" stroke="currentColor" stroke-width="1.5"
                stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                <circle cx="12" cy="10" r="3"></circle>
              </svg>
              <p>{{ locationLabel }}</p>
            </div>
          </section>

          <!-- Meta info -->
          <section class="detail-section detail-meta">
            <span v-if="property.created_at">
              Listed {{ formatDate(property.created_at) }}
            </span>
            <span v-if="property.updated_at">
              · Updated {{ formatDate(property.updated_at) }}
            </span>
            <span v-if="property.id" class="detail-meta__id">
              Ref #{{ property.id }}
            </span>
          </section>
        </div>

        <!-- RIGHT: sticky CTA sidebar -->
        <aside class="detail-sidebar">
          <div class="detail-cta-card">
            <p class="detail-cta-card__price">
              {{ formatPrice(property.price) }}
              <small v-if="forRent">/ mo</small>
            </p>

            <div class="detail-cta-card__status">
              <span class="detail-badge" :class="`detail-badge--${property.status}`">
                {{ formatStatus(property.status) }}
              </span>
            </div>

            <template v-if="property.status === 'available'">
              <button class="btn btn--primary btn--full" @click="handleContact">
                {{ forRent ? 'Request a Viewing' : 'Make an Enquiry' }}
              </button>
              <button class="btn btn--outline btn--full" @click="handleSchedule">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"
                  fill="none" stroke="currentColor" stroke-width="2"
                  stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                  <line x1="16" y1="2" x2="16" y2="6"></line>
                  <line x1="8" y1="2" x2="8" y2="6"></line>
                  <line x1="3" y1="10" x2="21" y2="10"></line>
                </svg>
                Schedule a Tour
              </button>
            </template>
            <template v-else>
              <p class="detail-cta-card__unavailable">
                This property is currently <strong>{{ formatStatus(property.status) }}</strong>
                and not available for new enquiries.
              </p>
            </template>

            <div class="detail-cta-card__divider"></div>

            <button
              class="detail-cta-card__fav-btn"
              :class="{ 'is-fav': favorited }"
              @click="toggleFavorite"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"
                :fill="favorited ? 'currentColor' : 'none'"
                stroke="currentColor" stroke-width="2"
                stroke-linecap="round" stroke-linejoin="round">
                <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06
                         a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78
                         1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
              </svg>
              {{ favorited ? 'Saved to Favorites' : 'Save to Favorites' }}
            </button>

            <button class="detail-cta-card__share-btn" @click="handleShare">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"
                fill="none" stroke="currentColor" stroke-width="2"
                stroke-linecap="round" stroke-linejoin="round">
                <circle cx="18" cy="5" r="3"></circle>
                <circle cx="6" cy="12" r="3"></circle>
                <circle cx="18" cy="19" r="3"></circle>
                <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line>
                <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line>
              </svg>
              Share Property
            </button>
          </div>

          <!-- Similar properties teaser -->
          <div v-if="similarProperties.length" class="detail-similar">
            <h3 class="detail-similar__title">Similar Properties</h3>
            <RouterLink
              v-for="sp in similarProperties"
              :key="sp.id"
              :to="{ name: 'PropertyDetail', params: { id: sp.id } }"
              class="detail-similar__item"
            >
              <img
                :src="sp.images?.[0] || sp.image || sp.thumbnail || '/placeholder.jpg'"
                :alt="sp.title"
                class="detail-similar__img"
              />
              <div class="detail-similar__info">
                <p class="detail-similar__name">{{ sp.title || 'Property' }}</p>
                <p class="detail-similar__price">{{ formatPrice(sp.price) }}</p>
              </div>
            </RouterLink>
          </div>
        </aside>

      </div><!-- /detail-body -->

      <!-- Toast notification -->
      <Transition name="toast">
        <div v-if="toast.visible" class="detail-toast" :class="`detail-toast--${toast.type}`">
          {{ toast.message }}
        </div>
      </Transition>

    </template>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';

export default {
  name: 'PropertyDetail',

  props: {
    jsonPath: {
      type: String,
      default: '../src/example.json'
    },
    forRent: {
      type: Boolean,
      default: false
    }
  },

  setup(props) {
    const route  = useRoute();
    const router = useRouter();

    // ─── State ────────────────────────────────────────────────
    const loading   = ref(true);
    const error     = ref(null);
    const property  = ref(null);
    const location  = ref(null);
    const allData   = ref(null);
    const favorited = ref(false);

    const activeImageIndex = ref(0);
    const lightboxOpen     = ref(false);
    const lightboxIndex    = ref(0);

    const descTruncated = ref(true);
    const TRUNCATE_AT   = 300; // chars

    const toast = ref({ visible: false, message: '', type: 'info' });
    let toastTimer = null;

    // ─── Fetch ────────────────────────────────────────────────
    const fetchProperty = async () => {
      loading.value = true;
      error.value   = null;

      try {
        const response = await fetch(props.jsonPath);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const data = await response.json();
        allData.value = data;

        const id = route.params.id;
        const found = (data.properties || []).find(
          p => String(p.id) === String(id)
        );

        if (!found) {
          error.value = `Property #${id} not found.`;
          return;
        }

        property.value = found;

        // Resolve location
        if (found.location_id && data.locations) {
          location.value = data.locations.find(
            loc => loc.id === found.location_id
          ) || null;
        }

        // Resolve favorite status
        const favs = data.favorites || [];
        favorited.value = favs.some(f => String(f.property_id) === String(found.id));

      } catch (err) {
        console.error('Error fetching property:', err);
        error.value = err.message || 'Failed to load property.';
      } finally {
        loading.value = false;
      }
    };

    // ─── Computed ─────────────────────────────────────────────

    // Normalise images: support images[], image, thumbnail
    const galleryImages = computed(() => {
      if (!property.value) return [];
      const p = property.value;
      if (Array.isArray(p.images) && p.images.length) return p.images;
      if (p.image)     return [p.image];
      if (p.thumbnail) return [p.thumbnail];
      return ['/placeholder.jpg'];
    });

    const activeImage = computed(
      () => galleryImages.value[activeImageIndex.value] || galleryImages.value[0]
    );

    const hasMultipleImages = computed(() => galleryImages.value.length > 1);

    // Location label: try city, district, name, address…
    const locationLabel = computed(() => {
      if (!location.value) return '';
      const l = location.value;
      return [l.city, l.district, l.name, l.address].filter(Boolean).join(', ');
    });

    // Features: support array or comma-string
    const features = computed(() => {
      if (!property.value) return [];
      const f = property.value.features || property.value.amenities;
      if (!f) return [];
      if (Array.isArray(f)) return f;
      if (typeof f === 'string') return f.split(',').map(s => s.trim()).filter(Boolean);
      return [];
    });

    // Quick stats
    const hasStats = computed(() => {
      if (!property.value) return false;
      return ['bedrooms', 'bathrooms', 'area', 'parking'].some(
        k => property.value[k] !== undefined
      );
    });

    // Description truncation
    const descNeedsTruncation = computed(
      () => (property.value?.description || '').length > TRUNCATE_AT
    );

    // Similar properties: same type, different id, max 3
    const similarProperties = computed(() => {
      if (!allData.value || !property.value) return [];
      return (allData.value.properties || [])
        .filter(
          p => p.id !== property.value.id &&
               p.property_type === property.value.property_type &&
               p.status === 'available'
        )
        .slice(0, 3);
    });

    // ─── Formatters ───────────────────────────────────────────
    const formatPrice = (price) => {
      if (price == null) return 'Price on request';
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        maximumFractionDigits: 0
      }).format(price);
    };

    const formatStatus = (status) => {
      const map = {
        available: 'Available',
        pending:   'Pending',
        sold:      'Sold',
        rented:    'Rented'
      };
      return map[status] || status;
    };

    const formatType = (type) => {
      const map = {
        house:       'House',
        apartment:   'Apartment',
        land:        'Land',
        villa:       'Villa',
        commercial:  'Commercial',
        condo:       'Condo'
      };
      return map[type] || type;
    };

    const formatDate = (dateStr) => {
      if (!dateStr) return '';
      const d = new Date(dateStr);
      return d.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
    };

    // ─── Lightbox ─────────────────────────────────────────────
    const openLightbox = (idx) => {
      lightboxIndex.value = idx;
      lightboxOpen.value  = true;
    };

    const lightboxPrev = () => {
      lightboxIndex.value =
        (lightboxIndex.value - 1 + galleryImages.value.length) % galleryImages.value.length;
    };

    const lightboxNext = () => {
      lightboxIndex.value =
        (lightboxIndex.value + 1) % galleryImages.value.length;
    };

    // Close lightbox on Escape
    const onKeydown = (e) => {
      if (!lightboxOpen.value) return;
      if (e.key === 'Escape') lightboxOpen.value = false;
      if (e.key === 'ArrowLeft')  lightboxPrev();
      if (e.key === 'ArrowRight') lightboxNext();
    };

    // ─── Actions ──────────────────────────────────────────────
    const toggleFavorite = () => {
      favorited.value = !favorited.value;
      showToast(
        favorited.value ? '❤️  Saved to favorites' : 'Removed from favorites',
        favorited.value ? 'success' : 'info'
      );
    };

    const handleContact = () => {
      showToast('Opening contact form…', 'info');
    };

    const handleSchedule = () => {
      showToast('Opening calendar…', 'info');
    };

    const handleShare = async () => {
      const url = window.location.href;
      if (navigator.share) {
        try {
          await navigator.share({
            title: property.value?.title || 'Property',
            url
          });
        } catch { /* user cancelled */ }
      } else {
        await navigator.clipboard.writeText(url).catch(() => {});
        showToast('Link copied to clipboard!', 'success');
      }
    };

    const showToast = (message, type = 'info') => {
      clearTimeout(toastTimer);
      toast.value = { visible: true, message, type };
      toastTimer = setTimeout(() => { toast.value.visible = false; }, 3000);
    };

    // ─── Lifecycle ────────────────────────────────────────────
    onMounted(() => {
      fetchProperty();
      window.addEventListener('keydown', onKeydown);
    });

    // Re-fetch if route param changes (navigating between properties)
    watch(() => route.params.id, () => {
      activeImageIndex.value = 0;
      fetchProperty();
    });

    return {
      loading,
      error,
      property,
      location,
      favorited,
      activeImageIndex,
      activeImage,
      galleryImages,
      hasMultipleImages,
      lightboxOpen,
      lightboxIndex,
      descTruncated,
      descNeedsTruncation,
      locationLabel,
      features,
      hasStats,
      similarProperties,
      toast,
      formatPrice,
      formatStatus,
      formatType,
      formatDate,
      openLightbox,
      lightboxPrev,
      lightboxNext,
      toggleFavorite,
      handleContact,
      handleSchedule,
      handleShare,
    };
  }
};
</script>

<style scoped>
/* ─────────────────────────────────────────────
   Design tokens
───────────────────────────────────────────── */
:root {
  --clr-bg:        #f8f7f4;
  --clr-surface:   #ffffff;
  --clr-primary:   #1a1a2e;
  --clr-accent:    #e07b39;
  --clr-accent-lt: #fdf0e6;
  --clr-text:      #1a1a2e;
  --clr-muted:     #6b7280;
  --clr-border:    #e8e5e0;
  --clr-success:   #16a34a;
  --clr-error:     #dc2626;
  --radius-sm:     6px;
  --radius-md:     12px;
  --radius-lg:     20px;
  --shadow-sm:     0 1px 3px rgba(0,0,0,.06), 0 1px 2px rgba(0,0,0,.04);
  --shadow-md:     0 4px 12px rgba(0,0,0,.08);
  --shadow-lg:     0 12px 32px rgba(0,0,0,.12);
  --font-display:  'Georgia', 'Times New Roman', serif;
  --font-body:     'system-ui', sans-serif;
}

/* ─────────────────────────────────────────────
   Page shell
───────────────────────────────────────────── */
.detail-page {
  min-height: 100vh;
  background: var(--clr-bg);
  font-family: var(--font-body);
  color: var(--clr-text);
}

/* ─────────────────────────────────────────────
   Loading
───────────────────────────────────────────── */
.detail-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  gap: 1rem;
}
.detail-loading__track {
  width: 200px;
  height: 3px;
  background: var(--clr-border);
  border-radius: 99px;
  overflow: hidden;
}
.detail-loading__bar {
  height: 100%;
  background: var(--clr-accent);
  border-radius: 99px;
  animation: loadBar 1.4s ease-in-out infinite;
}
@keyframes loadBar {
  0%   { width: 0; transform: translateX(0); }
  50%  { width: 60%; transform: translateX(70%); }
  100% { width: 0; transform: translateX(200px); }
}
.detail-loading__text {
  color: var(--clr-muted);
  font-size: .9rem;
  letter-spacing: .04em;
}

/* ─────────────────────────────────────────────
   Error
───────────────────────────────────────────── */
.detail-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  gap: 1rem;
  text-align: center;
}
.detail-error__code {
  font-family: var(--font-display);
  font-size: 7rem;
  line-height: 1;
  color: var(--clr-border);
}
.detail-error__msg {
  color: var(--clr-muted);
  max-width: 360px;
}

/* ─────────────────────────────────────────────
   Top bar
───────────────────────────────────────────── */
.detail-topbar {
  position: sticky;
  top: 0;
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: .75rem 1.5rem;
  background: rgba(248, 247, 244, .9);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--clr-border);
}
.detail-topbar__back {
  display: flex;
  align-items: center;
  gap: .4rem;
  padding: .45rem .9rem;
  background: var(--clr-surface);
  border: 1px solid var(--clr-border);
  border-radius: var(--radius-sm);
  font-size: .875rem;
  font-weight: 500;
  cursor: pointer;
  transition: background .15s, box-shadow .15s;
}
.detail-topbar__back:hover {
  background: var(--clr-border);
  box-shadow: var(--shadow-sm);
}
.detail-topbar__actions {
  display: flex;
  align-items: center;
  gap: .5rem;
}
.detail-topbar__fav,
.detail-topbar__share {
  display: flex;
  align-items: center;
  gap: .4rem;
  padding: .45rem .9rem;
  background: var(--clr-surface);
  border: 1px solid var(--clr-border);
  border-radius: var(--radius-sm);
  font-size: .875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all .15s;
}
.detail-topbar__fav:hover,
.detail-topbar__share:hover {
  background: var(--clr-border);
}
.detail-topbar__fav.is-fav {
  color: #e0305a;
  border-color: #e0305a;
  background: #fff0f4;
}

/* ─────────────────────────────────────────────
   Gallery
───────────────────────────────────────────── */
.detail-gallery {
  display: grid;
  grid-template-columns: 1fr 100px;
  gap: 8px;
  max-height: 520px;
  padding: 1rem 1.5rem .5rem;
}
.detail-gallery--single {
  grid-template-columns: 1fr;
}
.detail-gallery__main {
  position: relative;
  border-radius: var(--radius-lg);
  overflow: hidden;
  cursor: zoom-in;
  background: var(--clr-border);
}
.detail-gallery__img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform .35s ease;
}
.detail-gallery__main:hover .detail-gallery__img {
  transform: scale(1.02);
}
.detail-gallery__overlay {
  position: absolute;
  bottom: .75rem;
  right: .75rem;
  display: flex;
  align-items: center;
  gap: .4rem;
  padding: .4rem .8rem;
  background: rgba(0,0,0,.55);
  color: #fff;
  border-radius: 99px;
  font-size: .8rem;
  font-weight: 500;
  opacity: 0;
  transition: opacity .2s;
}
.detail-gallery__main:hover .detail-gallery__overlay {
  opacity: 1;
}
.detail-gallery__thumbs {
  display: flex;
  flex-direction: column;
  gap: 6px;
  overflow-y: auto;
  scrollbar-width: none;
}
.detail-gallery__thumbs::-webkit-scrollbar { display: none; }
.detail-gallery__thumb {
  flex-shrink: 0;
  height: 76px;
  border-radius: var(--radius-sm);
  overflow: hidden;
  border: 2px solid transparent;
  cursor: pointer;
  transition: border-color .15s;
  padding: 0;
  background: none;
}
.detail-gallery__thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.detail-gallery__thumb.is-active {
  border-color: var(--clr-accent);
}

/* Badge */
.detail-badge {
  display: inline-flex;
  align-items: center;
  padding: .25rem .7rem;
  border-radius: 99px;
  font-size: .78rem;
  font-weight: 700;
  letter-spacing: .04em;
  text-transform: uppercase;
}
.detail-badge--available { background: #dcfce7; color: #166534; }
.detail-badge--pending   { background: #fef9c3; color: #854d0e; }
.detail-badge--sold      { background: #fee2e2; color: #991b1b; }
.detail-badge--rented    { background: #e0e7ff; color: #3730a3; }

/* In gallery main — position absolute */
.detail-gallery__main .detail-badge {
  position: absolute;
  top: .75rem;
  left: .75rem;
}

/* ─────────────────────────────────────────────
   Lightbox
───────────────────────────────────────────── */
.lightbox {
  position: fixed;
  inset: 0;
  z-index: 1000;
  background: rgba(0,0,0,.92);
  display: flex;
  align-items: center;
  justify-content: center;
}
.lightbox__img {
  max-width: 90vw;
  max-height: 88vh;
  object-fit: contain;
  border-radius: var(--radius-sm);
}
.lightbox__close,
.lightbox__prev,
.lightbox__next {
  position: absolute;
  background: rgba(255,255,255,.1);
  border: none;
  color: #fff;
  cursor: pointer;
  font-size: 1.75rem;
  line-height: 1;
  border-radius: 50%;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background .15s;
}
.lightbox__close:hover,
.lightbox__prev:hover,
.lightbox__next:hover { background: rgba(255,255,255,.25); }
.lightbox__close { top: 1rem; right: 1rem; font-size: 1.1rem; }
.lightbox__prev  { left: 1rem; }
.lightbox__next  { right: 1rem; }
.lightbox__counter {
  position: absolute;
  bottom: 1rem;
  left: 50%;
  transform: translateX(-50%);
  color: rgba(255,255,255,.65);
  font-size: .85rem;
}

/* ─────────────────────────────────────────────
   Body grid
───────────────────────────────────────────── */
.detail-body {
  display: grid;
  grid-template-columns: 1fr 360px;
  gap: 2rem;
  max-width: 1280px;
  margin: 0 auto;
  padding: 1.5rem 1.5rem 4rem;
  align-items: start;
}

/* ─────────────────────────────────────────────
   Main column
───────────────────────────────────────────── */
.detail-header { margin-bottom: 1.5rem; }

.detail-header__top {
  display: flex;
  align-items: center;
  gap: .75rem;
  margin-bottom: .5rem;
}

.detail-type-pill {
  display: inline-flex;
  padding: .25rem .75rem;
  border-radius: 99px;
  background: var(--clr-accent-lt);
  color: var(--clr-accent);
  font-size: .78rem;
  font-weight: 700;
  letter-spacing: .04em;
  text-transform: uppercase;
}

.detail-views {
  display: flex;
  align-items: center;
  gap: .3rem;
  color: var(--clr-muted);
  font-size: .8rem;
}

.detail-title {
  font-family: var(--font-display);
  font-size: clamp(1.5rem, 3vw, 2.25rem);
  font-weight: 400;
  line-height: 1.2;
  margin: 0 0 .5rem;
}

.detail-location {
  display: flex;
  align-items: center;
  gap: .35rem;
  color: var(--clr-muted);
  font-size: .9rem;
  margin-bottom: .75rem;
}

.detail-price-row {
  display: flex;
  align-items: baseline;
  gap: 1rem;
  flex-wrap: wrap;
}

.detail-price {
  font-family: var(--font-display);
  font-size: 2rem;
  font-weight: 700;
  color: var(--clr-accent);
  letter-spacing: -.02em;
}
.detail-price small {
  font-size: 1rem;
  color: var(--clr-muted);
  font-weight: 400;
  font-family: var(--font-body);
}
.detail-price-psm {
  font-size: .85rem;
  color: var(--clr-muted);
  background: var(--clr-border);
  padding: .2rem .6rem;
  border-radius: var(--radius-sm);
}

/* Stats strip */
.detail-stats {
  list-style: none;
  padding: 1.25rem 0;
  margin: 0 0 .5rem;
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
  border-top: 1px solid var(--clr-border);
  border-bottom: 1px solid var(--clr-border);
}
.detail-stats__item {
  display: flex;
  align-items: center;
  gap: .4rem;
  color: var(--clr-muted);
  font-size: .9rem;
}
.detail-stats__item strong {
  color: var(--clr-text);
  font-size: 1.05rem;
}

/* Sections */
.detail-section {
  margin: 1.75rem 0;
}
.detail-section__title {
  font-family: var(--font-display);
  font-size: 1.2rem;
  font-weight: 400;
  margin: 0 0 .75rem;
  padding-bottom: .5rem;
  border-bottom: 1px solid var(--clr-border);
}

.detail-description {
  color: var(--clr-muted);
  line-height: 1.75;
  font-size: .95rem;
  margin: 0;
  transition: max-height .3s ease;
}
.detail-description.is-truncated {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.detail-toggle-desc {
  background: none;
  border: none;
  color: var(--clr-accent);
  font-size: .875rem;
  font-weight: 600;
  cursor: pointer;
  padding: .4rem 0 0;
}

/* Features */
.detail-features {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: .5rem .75rem;
}
.detail-features__item {
  display: flex;
  align-items: center;
  gap: .5rem;
  font-size: .88rem;
  color: var(--clr-text);
}
.detail-features__item svg { color: var(--clr-success); flex-shrink: 0; }

/* Map placeholder */
.detail-map-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 160px;
  background: var(--clr-border);
  border-radius: var(--radius-md);
  color: var(--clr-muted);
  gap: .5rem;
  font-size: .9rem;
}

/* Meta */
.detail-meta {
  color: var(--clr-muted);
  font-size: .8rem;
  display: flex;
  align-items: center;
  gap: .3rem;
  flex-wrap: wrap;
}
.detail-meta__id {
  margin-left: auto;
  background: var(--clr-border);
  padding: .2rem .6rem;
  border-radius: var(--radius-sm);
  font-family: monospace;
}

/* ─────────────────────────────────────────────
   Sidebar
───────────────────────────────────────────── */
.detail-sidebar {
  position: sticky;
  top: 4.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.detail-cta-card {
  background: var(--clr-surface);
  border: 1px solid var(--clr-border);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  box-shadow: var(--shadow-md);
  display: flex;
  flex-direction: column;
  gap: .75rem;
}
.detail-cta-card__price {
  font-family: var(--font-display);
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--clr-accent);
  letter-spacing: -.02em;
  margin: 0;
}
.detail-cta-card__price small {
  font-size: 1rem;
  color: var(--clr-muted);
  font-weight: 400;
  font-family: var(--font-body);
}
.detail-cta-card__status { margin-bottom: .25rem; }

.detail-cta-card__unavailable {
  font-size: .875rem;
  color: var(--clr-muted);
  text-align: center;
  padding: .75rem;
  background: var(--clr-bg);
  border-radius: var(--radius-sm);
  margin: 0;
}

.detail-cta-card__divider {
  border: none;
  border-top: 1px solid var(--clr-border);
  margin: .25rem 0;
}

.detail-cta-card__fav-btn,
.detail-cta-card__share-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: .5rem;
  padding: .6rem;
  border-radius: var(--radius-sm);
  background: none;
  border: 1px solid var(--clr-border);
  font-size: .875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all .15s;
}
.detail-cta-card__fav-btn:hover,
.detail-cta-card__share-btn:hover {
  background: var(--clr-bg);
}
.detail-cta-card__fav-btn.is-fav {
  color: #e0305a;
  border-color: #e0305a;
  background: #fff0f4;
}

/* Similar */
.detail-similar {
  background: var(--clr-surface);
  border: 1px solid var(--clr-border);
  border-radius: var(--radius-lg);
  padding: 1.25rem;
  box-shadow: var(--shadow-sm);
}
.detail-similar__title {
  font-family: var(--font-display);
  font-size: 1rem;
  font-weight: 400;
  margin: 0 0 .75rem;
  color: var(--clr-muted);
  text-transform: uppercase;
  letter-spacing: .06em;
  font-size: .8rem;
}
.detail-similar__item {
  display: flex;
  align-items: center;
  gap: .75rem;
  padding: .6rem 0;
  border-bottom: 1px solid var(--clr-border);
  text-decoration: none;
  color: inherit;
  transition: opacity .15s;
}
.detail-similar__item:last-child { border-bottom: none; }
.detail-similar__item:hover { opacity: .75; }
.detail-similar__img {
  width: 56px;
  height: 44px;
  object-fit: cover;
  border-radius: var(--radius-sm);
  flex-shrink: 0;
}
.detail-similar__info { min-width: 0; }
.detail-similar__name {
  font-size: .85rem;
  font-weight: 500;
  margin: 0 0 .15rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.detail-similar__price {
  font-size: .8rem;
  color: var(--clr-accent);
  margin: 0;
  font-weight: 600;
}

/* ─────────────────────────────────────────────
   Buttons (reusable)
───────────────────────────────────────────── */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: .5rem;
  padding: .7rem 1.25rem;
  border-radius: var(--radius-sm);
  font-size: .9rem;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: all .15s ease;
  text-decoration: none;
}
.btn--primary {
  background: var(--clr-primary);
  color: #fff;
}
.btn--primary:hover { opacity: .88; }
.btn--outline {
  background: transparent;
  color: var(--clr-text);
  border: 1.5px solid var(--clr-border);
}
.btn--outline:hover { background: var(--clr-bg); }
.btn--ghost {
  background: transparent;
  color: var(--clr-muted);
  border: 1px solid var(--clr-border);
}
.btn--ghost:hover { background: var(--clr-border); }
.btn--full { width: 100%; }

/* ─────────────────────────────────────────────
   Toast
───────────────────────────────────────────── */
.detail-toast {
  position: fixed;
  bottom: 1.5rem;
  left: 50%;
  transform: translateX(-50%);
  z-index: 500;
  padding: .65rem 1.4rem;
  border-radius: 99px;
  font-size: .875rem;
  font-weight: 600;
  box-shadow: var(--shadow-lg);
  white-space: nowrap;
  pointer-events: none;
}
.detail-toast--info    { background: var(--clr-primary); color: #fff; }
.detail-toast--success { background: #166534; color: #fff; }

.toast-enter-active,
.toast-leave-active { transition: opacity .25s, transform .25s; }
.toast-enter-from   { opacity: 0; transform: translateX(-50%) translateY(12px); }
.toast-leave-to     { opacity: 0; transform: translateX(-50%) translateY(12px); }

/* ─────────────────────────────────────────────
   Responsive
───────────────────────────────────────────── */
@media (max-width: 900px) {
  .detail-body {
    grid-template-columns: 1fr;
    padding: 1rem 1rem 3rem;
  }
  .detail-sidebar {
    position: static;
    order: -1;
  }
  .detail-gallery {
    grid-template-columns: 1fr;
    max-height: none;
    padding: .75rem 1rem .25rem;
  }
  .detail-gallery__thumbs {
    flex-direction: row;
    overflow-x: auto;
  }
  .detail-gallery__thumb {
    width: 80px;
    height: 60px;
    flex-shrink: 0;
  }
  .detail-topbar {
    padding: .65rem 1rem;
  }
}

@media (max-width: 480px) {
  .detail-stats {
    gap: 1rem;
  }
  .detail-features {
    grid-template-columns: 1fr;
  }
  .detail-price {
    font-size: 1.6rem;
  }
}
</style>