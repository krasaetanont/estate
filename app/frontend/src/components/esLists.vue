<script setup lang="ts">
import { useRouter } from 'vue-router';
import estateData from './estates.json';
const router = useRouter();

console.log(estateData);
</script>
<template>
    <div class="estate-list">
        <div v-for="estate in estateData" :key="estate.id" class="estate-item">
            <h2>{{ estate.title }}</h2>
            <p>{{ estate.location.city }}</p>
            <p>Price: {{ estate.price }}</p>
            <RouterLink :to="{ name: 'each-estate', params: { id: estate.id } }" class="btn">
                <p>View Details</p>
            </RouterLink>
        </div>
    </div>
</template> 

<style scoped>
.estate-list {
    background-color: var(--background-light);
    height: 50vh;
    padding: 20px;
    border-radius: 8px;
    display: flex;
    flex-direction: row;
    gap: 20px;
}
.estate-item {
    background-color: var(--vt-c-black-mute);
    border: 1px solid var(--vt-c-gray-200);
    padding: 15px;
    border-radius: 10px;
    width: 200px;
    display: flex;
    flex-direction: column;
}
.estate-item h2 {
    margin: 0 0 10px 0;
    font-size: 1.2em;
    color: var(--vt-c-white);
}
.estate-item p {
    margin: 5px 0;
    color: var(--vt-c-white);
}
.btn {
    position: relative;
    margin-top: auto;
}
</style>