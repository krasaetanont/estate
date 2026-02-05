<script setup lang="ts">
import { useRoute } from 'vue-router';
import estateData from '../components/estates.json';

const route = useRoute();
</script>
<template>
    <div class="each-estate-view">
        <div v-for="estate in estateData" :key="estate.id">
            <div v-if="estate.id === Number(route.params.id)">
                <h1>{{ estate.name }}</h1>
                <p>Location: {{ estate.location }}</p>
                <p>Price: {{ estate.price }}</p>
            </div>
        </div>
    </div>
</template>
