<template>
  <div class="insights-container" v-if="hasInsights">
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
  <div v-else class="empty-state">
    <div class="empty-icon">💡</div>
    <h3>No Insights Generated Yet</h3>
    <p>After analysis, you'll see structured insights here, including:</p>
    <ul class="empty-list">
      <li>
        <span class="list-icon">⚠️</span>
        <span>User Problems & Pain Points</span>
      </li>
      <li>
        <span class="list-icon">🎯</span>
        <span>Opportunities for Improvement</span>
      </li>
      <li>
        <span class="list-icon">🔍</span>
        <span>User Motivations & Needs</span>
      </li>
    </ul>
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

// Add this computed property
const hasInsights = computed(() => {
  return Object.values(formattedCategories.value).some(arr => arr.length > 0);
});
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
  border-left: 4px solid #5000b8;
  background-color: white;
  padding-left: 16px;
}

.insight-content {
  padding: 16px 0;
}

h3 {
  font-size: 18px;
  margin-bottom: 12px;
  color: #333;
  font-weight: 600;
  line-height: 1.4;
}

p {
  margin: 0;
  color: #666;
  font-size: 15px;
  line-height: 1.6;
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

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #666;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.empty-state h3 {
  font-size: 18px;
  margin-bottom: 16px;
  color: #333;
}

.empty-state p {
  font-size: 14px;
  color: #666;
  margin-bottom: 24px;
}

.empty-list {
  list-style: none;
  padding: 0;
  max-width: 300px;
  margin: 0 auto;
  text-align: left;
}

.empty-list li {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
  background: none;
  box-shadow: none;
  font-size: 14px;
  color: #555;
}

.list-icon {
  margin-right: 12px;
  font-size: 16px;
}
</style>
