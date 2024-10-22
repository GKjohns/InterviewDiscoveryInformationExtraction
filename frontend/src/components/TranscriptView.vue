<!-- components/TranscriptView.vue -->
<template>
  <div class="transcript-container">
    <pre>{{ transcript }}</pre>
    <button @click="showFullScreen" class="fullscreen-button">Full Screen</button>
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
  height: 100%;
  overflow-y: auto;
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
