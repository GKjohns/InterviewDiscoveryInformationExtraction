<!-- components/ReportView.vue -->
<template>
  <div class="report-container">
    <div v-html="renderedReport" class="markdown-content"></div>
    <button @click="showFullScreen" class="fullscreen-button">Full Screen</button>
  </div>
  <FullScreenModal v-if="isFullScreen" @close="isFullScreen = false">
    <div v-html="renderedReport" class="markdown-content"></div>
  </FullScreenModal>
</template>

<script setup>
import { computed, ref } from 'vue';
import { marked } from 'marked';
import { defineProps } from 'vue';
import FullScreenModal from './FullScreenModal.vue';

const props = defineProps({
  report: {
    type: String,
    required: true,
    default: ''
  }
});

const renderedReport = computed(() => marked(props.report));
const isFullScreen = ref(false);

const showFullScreen = () => {
  isFullScreen.value = true;
};
</script>

<style scoped>
.report-container {
  padding: 20px;
  position: relative; /* For fullscreen button positioning */
}

.markdown-content {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
  color: #333;
  line-height: 1.6;
}

.markdown-content h1,
.markdown-content h2,
.markdown-content h3,
.markdown-content h4,
.markdown-content h5,
.markdown-content h6 {
  margin-top: 2rem;
  margin-bottom: 1rem;
  font-weight: 600;
  line-height: 1.25;
}

.markdown-content h1 {
  font-size: 2.5rem;
}

.markdown-content h2 {
  font-size: 2rem;
}

.markdown-content h3 {
  font-size: 1.75rem;
}

.markdown-content p {
  margin-bottom: 1.5rem;
  font-size: 1.1rem;
}

.markdown-content ul,
.markdown-content ol {
  margin-bottom: 1.5rem;
  padding-left: 1.5rem;
}

.markdown-content li {
  margin-bottom: 0.5rem;
}

.markdown-content a {
  color: #5000b8;
  text-decoration: none;
}

.markdown-content a:hover {
  text-decoration: underline;
}

.markdown-content pre,
.markdown-content code {
  background-color: #f0f0f0;
  border-radius: 4px;
  padding: 0.2em 0.4em;
  font-family: 'Courier New', Courier, monospace;
}

.markdown-content pre {
  padding: 1em;
  overflow-x: auto;
}

.fullscreen-button {
  position: fixed;
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
  z-index: 100;
}

.fullscreen-button:hover {
  background-color: #4000a0;
}
</style>
