<script setup lang="ts">
import welcomeVideo from '../assets/WelcomeVideo.mp4';
</script>

<template>
  <div class="welcome-container">
    <video
      class="welcome-video"
      :src="welcomeVideo"
      autoplay
      loop
      muted
      playsinline
    ></video>
  </div>
</template>

<style scoped>
.welcome-container {
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  position: relative;
}
</style>