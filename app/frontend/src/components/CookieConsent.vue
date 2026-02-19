<template>
  <Teleport to="body">
    <!-- Banner -->
    <Transition name="slide-up">
      <div v-if="visible" class="cookie-banner">
        <div class="cookie-top">
          <div class="cookie-icon">🍪</div>
          <div class="cookie-text">
            <h2>We use cookies</h2>
            <p>
              We use cookies to enhance your browsing experience, serve personalized
              content, and analyze our traffic. Choose which cookies you're comfortable with.
              <a href="/privacy-policy">Learn more</a>
            </p>
          </div>
        </div>

        <div class="cookie-options">
          <!-- Essential (always on) -->
          <div class="cookie-option disabled">
            <div class="toggle on muted"></div>
            <div class="option-label">
              <span>Essential</span>
              <span>Always active</span>
            </div>
          </div>

          <!-- Analytics -->
          <div class="cookie-option" @click="toggleCategory('analytics')">
            <div class="toggle" :class="{ on: preferences.analytics }"></div>
            <div class="option-label">
              <span>Analytics</span>
              <span>Usage &amp; performance</span>
            </div>
          </div>

          <!-- Marketing -->
          <div class="cookie-option" @click="toggleCategory('marketing')">
            <div class="toggle" :class="{ on: preferences.marketing }"></div>
            <div class="option-label">
              <span>Marketing</span>
              <span>Personalized ads</span>
            </div>
          </div>
        </div>

        <div class="cookie-actions">
          <button class="btn btn-accept" @click="acceptAll">Accept All</button>
          <button class="btn btn-selected" @click="saveSelected">Save Preferences</button>
          <button class="btn btn-reject" @click="rejectAll">Reject All</button>
        </div>
      </div>
    </Transition>

    <!-- Success Toast -->
    <Transition name="pop">
      <div v-if="toastVisible" class="cookie-toast">
        <span>✓</span>
        <span>{{ toastMessage }}</span>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'

// ── Props ──────────────────────────────────────────────────────────────────
const props = defineProps({
  /** localStorage key used to persist consent */
  storageKey: {
    type: String,
    default: 'cookie_consent',
  },
})

// ── Emits ──────────────────────────────────────────────────────────────────
/**
 * Emitted when the user saves their choice.
 * Payload: { essential: true, analytics: boolean, marketing: boolean }
 */
const emit = defineEmits(['consent'])

// ── State ──────────────────────────────────────────────────────────────────
const visible = ref(false)
const toastVisible = ref(false)
const toastMessage = ref('')

const preferences = reactive({
  analytics: false,
  marketing: false,
})

// ── Lifecycle ──────────────────────────────────────────────────────────────
onMounted(() => {
  const saved = localStorage.getItem(props.storageKey)
  if (!saved) {
    // No consent stored yet → show banner
    visible.value = true
  } else {
    // Restore stored prefs and emit so the app can react immediately
    const parsed = JSON.parse(saved)
    Object.assign(preferences, parsed)
    emit('consent', { essential: true, ...parsed })
  }
})

// ── Methods ────────────────────────────────────────────────────────────────
function toggleCategory(key) {
  preferences[key] = !preferences[key]
}

function save(message) {
  const result = { essential: true, ...preferences }
  localStorage.setItem(props.storageKey, JSON.stringify(preferences))
  emit('consent', result)
  visible.value = false
  showToast(message)
}

function acceptAll() {
  preferences.analytics = true
  preferences.marketing = true
  save('All cookies accepted 🎉')
}

function rejectAll() {
  preferences.analytics = false
  preferences.marketing = false
  save('Only essential cookies enabled.')
}

function saveSelected() {
  const active = Object.entries(preferences)
    .filter(([, v]) => v)
    .map(([k]) => k)
  const msg = active.length
    ? `Saved: essential + ${active.join(', ')}.`
    : 'Only essential cookies enabled.'
  save(msg)
}

function showToast(message) {
  toastMessage.value = message
  toastVisible.value = true
  setTimeout(() => (toastVisible.value = false), 3500)
}

// ── Expose for parent ref access (optional) ────────────────────────────────
defineExpose({
  /** Call this to re-open the banner (e.g. from a "Cookie Settings" link) */
  reopen() {
    visible.value = true
  },
})
</script>

<style scoped>
/* ── Layout ───────────────────────────────────────────────────────────────── */
.cookie-banner {
  position: fixed;
  bottom: 32px;
  left: 50%;
  transform: translateX(-50%);
  width: min(680px, calc(100vw - 32px));
  background: #141414;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  padding: 28px 32px;
  z-index: 9999;
  box-shadow: 0 32px 80px rgba(0, 0, 0, 0.6), 0 0 0 1px rgba(245, 200, 66, 0.06);
  font-family: 'DM Sans', sans-serif;
  color: #fff;
}

/* ── Top row ──────────────────────────────────────────────────────────────── */
.cookie-top {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 20px;
}

.cookie-icon {
  font-size: 32px;
  line-height: 1;
  flex-shrink: 0;
  animation: wiggle 2.5s ease-in-out 1s infinite;
}

@keyframes wiggle {
  0%, 100% { transform: rotate(0deg); }
  20%       { transform: rotate(-8deg); }
  40%       { transform: rotate(8deg); }
  60%       { transform: rotate(-4deg); }
  80%       { transform: rotate(4deg); }
}

.cookie-text h2 {
  font-size: 1.2rem;
  font-weight: 700;
  margin-bottom: 6px;
  letter-spacing: -0.01em;
}

.cookie-text p {
  font-size: 0.84rem;
  line-height: 1.65;
  color: rgba(255, 255, 255, 0.5);
  font-weight: 300;
}

.cookie-text a {
  color: #f5c842;
  text-decoration: none;
  border-bottom: 1px solid rgba(245, 200, 66, 0.3);
  transition: border-color 0.2s;
}
.cookie-text a:hover { border-color: #f5c842; }

/* ── Options ──────────────────────────────────────────────────────────────── */
.cookie-options {
  display: flex;
  gap: 10px;
  margin-bottom: 22px;
  flex-wrap: wrap;
}

.cookie-option {
  display: flex;
  align-items: center;
  gap: 10px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 10px 14px;
  cursor: pointer;
  transition: border-color 0.2s, background 0.2s;
  flex: 1;
  min-width: 140px;
  user-select: none;
}
.cookie-option:hover:not(.disabled) {
  border-color: rgba(245, 200, 66, 0.3);
  background: rgba(245, 200, 66, 0.04);
}
.cookie-option.disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

/* Toggle pill */
.toggle {
  width: 36px;
  height: 20px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.12);
  position: relative;
  flex-shrink: 0;
  transition: background 0.3s;
}
.toggle::after {
  content: '';
  position: absolute;
  top: 3px;
  left: 3px;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: #fff;
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.toggle.on {
  background: #f5c842;
}
.toggle.on::after {
  transform: translateX(16px);
  background: #0e0e0e;
}
.toggle.muted.on {
  opacity: 0.5;
}

.option-label {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.option-label span:first-child {
  font-size: 0.78rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.85);
}
.option-label span:last-child {
  font-size: 0.7rem;
  color: rgba(255, 255, 255, 0.35);
}

/* ── Buttons ──────────────────────────────────────────────────────────────── */
.cookie-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.btn {
  border: none;
  border-radius: 10px;
  padding: 12px 20px;
  font-family: inherit;
  font-size: 0.84rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  letter-spacing: 0.01em;
}

.btn-accept {
  background: #f5c842;
  color: #0e0e0e;
  flex: 1;
}
.btn-accept:hover {
  background: #ffd84d;
  transform: translateY(-1px);
  box-shadow: 0 8px 24px rgba(245, 200, 66, 0.25);
}
.btn-accept:active { transform: translateY(0); }

.btn-selected {
  background: rgba(255, 255, 255, 0.06);
  color: rgba(255, 255, 255, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.08);
}
.btn-selected:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
}

.btn-reject {
  background: transparent;
  color: rgba(255, 255, 255, 0.35);
  border: 1px solid rgba(255, 255, 255, 0.06);
}
.btn-reject:hover {
  color: rgba(255, 255, 255, 0.6);
  border-color: rgba(255, 255, 255, 0.15);
}

/* ── Toast ────────────────────────────────────────────────────────────────── */
.cookie-toast {
  position: fixed;
  bottom: 32px;
  left: 50%;
  transform: translateX(-50%);
  background: #141414;
  border: 1px solid rgba(245, 200, 66, 0.2);
  border-radius: 14px;
  padding: 14px 22px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.84rem;
  color: rgba(255, 255, 255, 0.7);
  z-index: 10000;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  white-space: nowrap;
}

/* ── Transitions ──────────────────────────────────────────────────────────── */
.slide-up-enter-active {
  transition: opacity 0.4s ease, transform 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}
.slide-up-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.slide-up-enter-from {
  opacity: 0;
  transform: translateX(-50%) translateY(40px);
}
.slide-up-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(20px);
}

.pop-enter-active {
  transition: opacity 0.3s ease, transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.pop-leave-active {
  transition: opacity 0.4s ease;
}
.pop-enter-from {
  opacity: 0;
  transform: translateX(-50%) scale(0.85);
}
.pop-leave-to {
  opacity: 0;
  transform: translateX(-50%) scale(1);
}
</style>
