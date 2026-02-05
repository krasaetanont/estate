<script setup lang="ts">
    import { RouterLink, RouterView } from 'vue-router'
    import estateListings from '../components/esLists.vue';
    import welcome from './Welcome.vue';
    import Hero from '../components/Hero.vue';
</script>

<template>
    <welcome class="welcome" />
    <Hero
        title="Find Your Dream Home"
        subtitle="Browse premium properties with verified listings and real photos."
        image="/src/assets/hero.jpg"
        >
        <template>
            <button class="btn">Browse Listings</button>
        </template>
    </Hero>
    <Hero
        title="Find Your Dream Home"
        subtitle="Browse premium properties with verified listings and real photos."
        image="/src/assets/hero.jpg"
        >
        <template>
            <button class="btn">Browse Listings</button>
        </template>
    </Hero>
    <div>
        <h2>Latest Listings</h2>
        <estateListings />
    </div>
</template>

<style scoped>
.welcome {
    margin-top: -85px;
}
h2 {
    margin: 20px 0;
    font-size: 1.8em;
    color: var(--vt-c-black);
}
</style>