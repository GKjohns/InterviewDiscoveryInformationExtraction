<!-- components/TranscriptView.vue -->
<template>
  <div class="transcript-container" v-if="transcript.trim()">
    <pre>{{ transcript }}</pre>
    <button @click="showFullScreen" class="fullscreen-button">Full Screen</button>
  </div>
  <div v-else class="empty-state">
    <div class="empty-icon">📄</div>
    <h3>No Transcript Available</h3>
    <p>Upload a transcript file to see its contents here.</p>
  </div>
  <FullScreenModal v-if="isFullScreen" @close="isFullScreen = false">
    <pre>{{ transcript }}</pre>
  </FullScreenModal>
</template>

<script setup>
import { defineProps, ref } from 'vue';
import FullScreenModal from './FullScreenModal.vue';

defineProps({
  transcript: {
    type: String,
    required: true,
    default: ''
  }
});

const isFullScreen = ref(false);

const showFullScreen = () => {
  isFullScreen.value = true;
};
</script>

<style scoped>
.transcript-container {
  height: auto;
  padding: 20px;
  background-color: #f8f8f8;
  border-radius: 4px;
}

pre {
  white-space: pre-wrap;
  word-wrap: break-word;
  font-family: 'Courier New', Courier, monospace;
  font-size: 14px;
  line-height: 1.5;
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
  margin-bottom: 8px;
  color: #333;
}

.empty-state p {
  font-size: 14px;
  color: #666;
}
</style>
