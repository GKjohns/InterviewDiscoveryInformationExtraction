<template>
  <div class="insights-container">
    <section v-for="(items, category) in formattedCategories" :key="category" class="insight-section">
      <div class="insight-header">
        <h2>{{ formatTitle(category) }}</h2>
      </div>
      <div class="insight-content">
        <ul v-if="items.length" class="insight-list">
          <li v-for="(item, index) in items" :key="index" class="insight-item">
            <div class="insight-item-content">
              <h3>{{ getPrimaryText(item, category) }}</h3>
              <p>{{ getSecondaryText(item, category) }}</p>
            </div>
          </li>
        </ul>
        <p v-else class="no-insights">No {{ formatTitle(category).toLowerCase() }} identified.</p>
      </div>
    </section>
  </div>
</template>

<script>
import { computed } from 'vue';

export default {
  name: 'InsightsView',
  props: {
    insights: {
      type: Object,
      required: true,
      default: () => ({
        user_problems: [],
        opportunities: [],
        user_motivations: []
      })
    }
  },
  setup(props) {
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

    return {
      formattedCategories,
      formatTitle,
      getPrimaryText,
      getSecondaryText
    };
  }
};
</script>

<style>
.insights-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.insight-section {
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
  overflow: hidden;
}

.insight-header {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.insight-header h2 {
  font-size: 1.125rem;
  font-weight: 500;
  color: #111827;
  margin: 0;
}

.insight-content {
  padding: 1rem 1.5rem;
}

.insight-list {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.insight-item {
  padding: 1rem 0;
  border-bottom: 1px solid #e5e7eb;
}

.insight-item:last-child {
  border-bottom: none;
}

.insight-item-content h3 {
  font-size: 0.875rem;
  font-weight: 500;
  color: #111827;
  margin: 0 0 0.25rem 0;
}

.insight-item-content p {
  font-size: 0.875rem;
  color: #6b7280;
  margin: 0;
}

.no-insights {
  font-size: 0.875rem;
  color: #6b7280;
  font-style: italic;
}
</style>
