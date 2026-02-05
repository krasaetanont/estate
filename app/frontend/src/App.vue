<script setup lang="ts">
import { RouterView } from 'vue-router'
import Header from './components/header.vue'
</script>

<template>
  <Header class="header" />
  <main>
    <RouterView :key="$route.fullPath" />
  </main>
  <footer>
    <p>&copy; 2024 EstatePro. All rights reserved.</p>
  </footer>
</template>


<style scoped>
.header {
  position: sticky;
}
</style>
