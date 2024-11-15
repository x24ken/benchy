<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import AppMultiAutocomplete from "./pages/AppMultiAutocomplete.vue";
import AppMultiToolCall from "./pages/AppMultiToolCall.vue";

const routes = {
  "/autocomplete": AppMultiAutocomplete,
  "/tool-call": AppMultiToolCall,
};

const currentPath = ref(window.location.hash);

console.log(`currentPath`, currentPath);

const currentView = computed(() => {
  // @ts-ignore
  return routes[currentPath.value.slice(1) || "/"];
});

onMounted(() => {
  window.addEventListener("hashchange", () => {
    currentPath.value = window.location.hash;
  });
});
</script>

<template>
  <div class="app-container">
    <div class="home-container" v-if="currentPath == ''">
      <h1>Benchy</h1>
      <p>Benchmarks you can feel.</p>
    </div>
    <nav class="nav-buttons" v-if="currentPath == ''">
      <a href="#/autocomplete" class="nav-button">Multi Autocomplete</a>
      <a href="#/tool-call" class="nav-button">Tool Call Demo</a>
    </nav>
    <component :is="currentView" v-else />
  </div>
</template>

<style scoped>
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
  background-color: #f5f5f5;
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
