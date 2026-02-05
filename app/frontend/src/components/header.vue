<script setup lang="ts">
import { RouterLink } from 'vue-router';
import { ref } from 'vue';
import logo from '../assets/logo.svg';
const isMenuOpen = ref(false);
function toggleMenu() {
    isMenuOpen.value = !isMenuOpen.value;
}
</script>
<template>
    <div class="wrapper">
        <RouterLink :to="{ name: 'home' }">
            <img :src="logo" alt="EstatePro Logo" class="logo" />
        </RouterLink>
        <nav class="nav" :class="{ open: isMenuOpen }">
            <RouterLink :to="{ name: 'buy' }">Buy</RouterLink>
            <RouterLink :to="{ name: 'seller' }">Sell</RouterLink>
            <RouterLink :to="{ name: 'rent' }">Rent</RouterLink>
            <RouterLink :to="{ name: 'about' }">About</RouterLink>
            <RouterLink :to="{ name: 'contact' }">Contact</RouterLink>
        </nav>
        <div class="toggle" v-if="isMenuOpen">
            <RouterLink :to="{ name: 'buy' }">Buy</RouterLink>
            <RouterLink :to="{ name: 'seller' }">Sell</RouterLink>
            <RouterLink :to="{ name: 'rent' }">Rent</RouterLink>
            <RouterLink :to="{ name: 'about' }">About</RouterLink>
            <RouterLink :to="{ name: 'contact' }">Contact</RouterLink>
        </div>
        <button class="hamburger" @click="toggleMenu">
            &#9776;
        </button>
    </div>
</template>

<style scoped>
.logo {
    height: 40px;
}
.wrapper {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    position: absolute;
    top: 0;
    z-index: 10;
}
@media (max-width: 768px) {
    .nav {
        display: none;
    }
    .hamburger {
        display: block;
    }
}
@media (min-width: 769px) {
    .hamburger {
        display: none;
    }
}
</style>