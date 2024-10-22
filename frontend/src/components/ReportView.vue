<!-- components/ReportView.vue -->
<template>
  <div class="report-container">
    <div class="report-header">
      <h2>Analysis Report</h2>
    </div>
    <div class="report-content">
      <div v-html="renderedReport" class="markdown-content"></div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue';
import { marked } from 'marked';

export default {
  name: 'ReportView',
  props: {
    report: {
      type: String,
      required: true,
      default: ''
    }
  },
  setup(props) {
    const renderedReport = computed(() => marked(props.report));
    return { renderedReport };
  }
};
</script>

<style>
.report-container {
  background-color: white;
  border-radius: 0.5rem;
  overflow: hidden;
}

.report-header {
  padding: 1rem 1.5rem;
  background-color: #f9fafb;
  border-bottom: 1px solid var(--border-color);
}

.report-header h2 {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-color);
  margin: 0;
}

.report-content {
  padding: 1.5rem;
}

.markdown-content h1,
.markdown-content h2,
.markdown-content h3,
.markdown-content h4,
.markdown-content h5,
.markdown-content h6 {
  font-weight: 600;
  color: var(--text-color);
  margin-top: 1.5rem;
  margin-bottom: 1rem;
}

.markdown-content p {
  margin-bottom: 1rem;
  color: var(--text-color);
}

.markdown-content ul,
.markdown-content ol {
  margin-bottom: 1rem;
  padding-left: 1.5rem;
}

.markdown-content li {
  margin-bottom: 0.5rem;
}

.markdown-content a {
  color: var(--primary-color);
  text-decoration: none;
}

.markdown-content a:hover {
  text-decoration: underline;
}
</style>
