<template>
  <div class="insights-container">
    <div class="categories">
      <button
        v-for="(items, category) in formattedCategories"
        :key="category"
        @click="activeCategory = category"
        :class="['category-button', { active: activeCategory === category }]"
      >
        {{ formatTitle(category) }}
      </button>
    </div>

    <div class="insights-content">
      <h2>{{ formatTitle(activeCategory) }}</h2>
      <ul v-if="formattedCategories[activeCategory].length">
        <li v-for="(item, index) in formattedCategories[activeCategory]" :key="index">
          <strong>{{ getPrimaryText(item, activeCategory) }}</strong>
          <p>{{ getSecondaryText(item, activeCategory) }}</p>
        </li>
      </ul>
      <p v-else class="no-data">
        No {{ formatTitle(activeCategory).toLowerCase() }} identified.
      </p>
    </div>
    <button @click="showFullScreen" class="fullscreen-button">Full Screen</button>
  </div>
  <FullScreenModal v-if="isFullScreen" @close="isFullScreen = false">
    <div class="insights-container">
      <div class="categories">
        <button
          v-for="(items, category) in formattedCategories"
          :key="category"
          @click="activeCategory = category"
          :class="['category-button', { active: activeCategory === category }]"
        >
          {{ formatTitle(category) }}
        </button>
      </div>

      <div class="insights-content">
        <h2>{{ formatTitle(activeCategory) }}</h2>
        <ul v-if="formattedCategories[activeCategory].length">
          <li v-for="(item, index) in formattedCategories[activeCategory]" :key="index">
            <strong>{{ getPrimaryText(item, activeCategory) }}</strong>
            <p>{{ getSecondaryText(item, activeCategory) }}</p>
          </li>
        </ul>
        <p v-else class="no-data">
          No {{ formatTitle(activeCategory).toLowerCase() }} identified.
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

const activeCategory = ref('user_problems');

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

const isFullScreen = ref(false);

const showFullScreen = () => {
  isFullScreen.value = true;
};
</script>

<style scoped>
.insights-container {
  display: flex;
  height: 100%;
}

.categories {
  width: 200px;
  border-right: 1px solid #e0e0e0;
  padding-right: 15px;
}

.category-button {
  display: block;
  width: 100%;
  text-align: left;
  padding: 10px;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 14px;
}

.category-button.active {
  background-color: #f0f0f0;
  font-weight: 500;
}

.insights-content {
  flex-grow: 1;
  padding-left: 20px;
  overflow-y: auto;
}

h2 {
  font-size: 18px;
  margin-bottom: 15px;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin-bottom: 15px;
}

strong {
  display: block;
  margin-bottom: 5px;
}

.no-data {
  color: #666;
  font-style: italic;
}

.fullscreen-button {
  position: absolute;
  bottom: 10px;
  right: 10px;
  padding: 5px 10px;
  background-color: #5000b8;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>
