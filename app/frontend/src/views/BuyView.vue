<script setup lang="ts">
import estateData from '../components/estates.json';
import estateListings from '../components/esLists.vue';
import estateLocations from '../components/locations.json'
import { ref, computed } from 'vue';

interface Location {
  id: number;
  country: string;
  city: string;
  address: string;
  latitude: number;
  longitude: number;
}

// Convert object to array and extract unique locations
const locationsArray = Object.values(estateLocations) as Location[];
const uniqueLocations = Array.from(new Set(locationsArray.map(loc => `${loc.city}, ${loc.country}`)));

const isDropdownOpen = ref(false);
const searchQuery = ref('');
const selectedLocation = ref('All areas');

const filteredLocations = computed(() => {
  const q = searchQuery.value.trim().toLowerCase();
  if (!q) return uniqueLocations;
  return uniqueLocations.filter(loc => loc.toLowerCase().includes(q));
});

const selectLocation = (location: string) => {
  selectedLocation.value = location;
  isDropdownOpen.value = false;
  searchQuery.value = '';
};
</script>

<template>
    <div class="search">
        <p>Buy View</p>
        <div class="dropdown-container">
          <button @click="isDropdownOpen = !isDropdownOpen" class="dropdown-button">
            {{ selectedLocation }}
          </button>
          
          <div v-if="isDropdownOpen" class="dropdown-menu">
            <input 
              v-model="searchQuery"
              type="text" 
              placeholder="Search locations..." 
              class="search-input"
              @click.stop
            />
            <ul class="dropdown-list">
              <li @click="selectLocation('All areas')" class="dropdown-item">All areas</li>
              <li 
                v-for="location in filteredLocations" 
                :key="location"
                @click="selectLocation(location)"
                class="dropdown-item"
              >
                {{ location }}
              </li>
            </ul>
          </div>
        </div>

        <button>All types</button>
        <button>Select prices</button>
        <input type="text" placeholder="Search properties..." />
        <button>Search</button>
        <p>+filters</p>
        <p>clear</p>
        <button>Most Recent</button>
    </div>
    <!-- <estateListings :estates="estateData" :showButton="false" /> -->
</template>


<style scoped>
.search {
    margin-top:10vh;
}

.dropdown-container {
    position: relative;
    display: inline-block;
}

.dropdown-button {
    padding: 8px 12px;
    background-color: #f0f0f0;
    border: 1px solid #ccc;
    border-radius: 4px;
    cursor: pointer;
}

.dropdown-button:hover {
    background-color: #e0e0e0;
}

.dropdown-menu {
    position: absolute;
    top: 100%;
    left: 0;
    background-color: white;
    border: 1px solid #ccc;
    border-radius: 4px;
    margin-top: 4px;
    min-width: 200px;
    z-index: 10;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.search-input {
    width: 100%;
    padding: 8px;
    border: none;
    border-bottom: 1px solid #ccc;
    box-sizing: border-box;
    border-radius: 4px 4px 0 0;
}

.dropdown-list {
    list-style: none;
    padding: 0;
    margin: 0;
    max-height: 200px;
    overflow-y: auto;
}

.dropdown-item {
    padding: 10px 12px;
    cursor: pointer;
    transition: background-color 0.2s;
}

.dropdown-item:hover {
    background-color: #f5f5f5;
}
</style>