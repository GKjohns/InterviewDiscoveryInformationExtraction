<template>
  <div class="modal-overlay" @click="$emit('close')">
    <div class="modal-content" @click.stop>
      <button class="close-button" @click="$emit('close')">×</button>
      <div class="modal-inner">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { defineEmits } from 'vue';
  defineEmits(['close']);
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  width: 90%;
  height: 90%;
  overflow-y: auto;
  position: relative;
  max-width: 1200px; /* Limit maximum width for better readability */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.modal-inner {
  max-width: 800px; /* Paper-like width */
  margin: 0 auto;
  padding: 40px;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 24px;
  background: none;
  border: none;
  cursor: pointer;
}
</style>

