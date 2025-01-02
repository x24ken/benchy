<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import AppMultiAutocomplete from "./pages/AppMultiAutocomplete.vue";
import AppMultiToolCall from "./pages/AppMultiToolCall.vue";
import IsoSpeedBench from "./pages/IsoSpeedBench.vue";

const routes = {
  "/autocomplete": AppMultiAutocomplete,
  "/tool-call": AppMultiToolCall,
  "/iso-speed-bench": IsoSpeedBench,
};

const currentPath = ref(window.location.hash);

const currentView = computed(() => {
  if (!currentPath.value) {
    return null;
  }
  return routes[currentPath.value.slice(1) as keyof typeof routes] || null;
});

onMounted(() => {
  window.addEventListener("hashchange", () => {
    currentPath.value = window.location.hash;
  });
});

document.title = "BENCHY";
</script>

<template>
  <div class="app-container">
    <div class="home-container" v-if="!currentView">
      <h1 class="title">BENCHY</h1>
      <p class="subtitle">Interactive benchmarks you can <b>feel</b></p>
      <nav class="nav-buttons">
        <a href="#/autocomplete" class="nav-button">Multi Autocomplete</a>
        <a href="#/tool-call" class="nav-button">Long Tool Call</a>
        <a href="#/iso-speed-bench" class="nav-button">ISO Speed Bench</a>
      </nav>
    </div>
    <component :is="currentView" v-else />
  </div>
</template>

<style scoped>
.title {
  font-size: 5rem;
  font-weight: bold;
  background: linear-gradient(
    90deg,
    rgba(14, 68, 145, 1) 0%,
    rgba(0, 212, 255, 1) 100%
  );
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 0 30px rgba(0, 212, 255, 0.8);
  margin-bottom: 1rem;
}

.home-container {
  text-align: center;
  padding: 2rem;
}

.app-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.nav-buttons {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 2rem;
  /* background-color: #f5f5f5; */
}

.nav-button {
  padding: 1rem 2rem;
  border: 2px solid rgb(14, 68, 145);
  border-radius: 8px;
  color: rgb(14, 68, 145);
  text-decoration: none;
  font-weight: bold;
  transition: all 0.3s ease;
  width: 300px;
  height: 300px;
}

.nav-button:hover {
  background-color: rgb(14, 68, 145);
  color: white;
}

.router-link-active {
  background-color: rgb(14, 68, 145);
  color: white;
}
</style>
