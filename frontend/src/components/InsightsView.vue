<template>
  <div class="insights-container">
    <div v-for="(items, category) in formattedCategories" :key="category" class="category-section">
      <h2>{{ formatTitle(category) }}</h2>
      <ul v-if="items.length">
        <li v-for="(item, index) in items" :key="index">
          <div class="insight-content">
            <h3>{{ getPrimaryText(item, category) }}</h3>
            <p>{{ getSecondaryText(item, category) }}</p>
          </div>
        </li>
      </ul>
      <p v-else class="no-data">
        No {{ formatTitle(category).toLowerCase() }} identified.
      </p>
    </div>
    <button @click="showFullScreen" class="fullscreen-button">Full Screen</button>
  </div>
  <FullScreenModal v-if="isFullScreen" @close="isFullScreen = false">
    <div class="insights-container">
      <div v-for="(items, category) in formattedCategories" :key="category" class="category-section">
        <h2>{{ formatTitle(category) }}</h2>
        <ul v-if="items.length">
          <li v-for="(item, index) in items" :key="index">
            <div class="insight-content">
              <h3>{{ getPrimaryText(item, category) }}</h3>
              <p>{{ getSecondaryText(item, category) }}</p>
            </div>
          </li>
        </ul>
        <p v-else class="no-data">
          No {{ formatTitle(category).toLowerCase() }} identified.
        </p>
      </div>
    </div>
  </FullScreenModal>
</template>

<script setup>
import { ref, computed } from 'vue';
import { defineProps } from 'vue';
import FullScreenModal from './FullScreenModal.vue';

const props = defineProps({
  insights: {
    type: Object,
    required: true,
    default: () => ({
      user_problems: [],
      opportunities: [],
      user_motivations: []
    })
  }
});

const isFullScreen = ref(false);

const showFullScreen = () => {
  isFullScreen.value = true;
};

const formattedCategories = computed(() => ({
  user_problems: props.insights.user_problems || [],
  opportunities: props.insights.opportunities || [],
  user_motivations: props.insights.user_motivations || []
}));

const formatTitle = (str) => {
  return str
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
};

const getPrimaryText = (item, category) => {
  const mappings = {
    user_problems: 'problem',
    opportunities: 'opportunity',
    user_motivations: 'motivation'
  };
  return item[mappings[category]] || '';
};

const getSecondaryText = (item, category) => {
  const mappings = {
    user_problems: 'context',
    opportunities: 'potential_impact',
    user_motivations: 'underlying_need'
  };
  return item[mappings[category]] || '';
};
</script>

<style scoped>
.insights-container {
  padding: 20px;
  position: relative; /* For fullscreen button positioning */
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  color: #333;
  line-height: 1.6;
}

.category-section {
  margin-bottom: 40px;
}

h2 {
  font-size: 22px;
  margin-bottom: 20px;
  color: #5000b8;
  font-weight: 600;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin-bottom: 24px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.insight-content {
  padding: 20px;
}

h3 {
  font-size: 18px;
  margin-bottom: 8px;
  color: #333;
  font-weight: 600;
}

p {
  margin: 0;
  color: #555;
  font-size: 14px;
}

.no-data {
  color: #888;
  font-style: italic;
  font-size: 14px;
}

.fullscreen-button {
  position: fixed; /* Changed back to fixed */
  bottom: 20px;
  right: 20px;
  padding: 10px 20px;
  background-color: #5000b8;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.2s ease;
  z-index: 100; /* Added to ensure button stays above content */
}

.fullscreen-button:hover {
  background-color: #4000a0;
}
</style>
