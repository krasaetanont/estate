<script setup lang="ts">
import PropertyList from '../components/property/PropertyList.vue';
import Hero from '../components/common/Hero.vue';
</script>

<template>
  <div class="home-view">
    <Hero 
        title="Find Your Dream Home"
        subtitle="Browse thousands of properties"
        videoSrc="../src/assets/WelcomeVideo.mp4"
        :showSearch="false"
        />
    <PropertyList :jsonPath="'../src/example.json'" :filterStatus="'available'" :limit="3" />
  </div>
</template>