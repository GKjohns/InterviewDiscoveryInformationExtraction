<!-- components/TranscriptView.vue -->
<template>
  <div class="transcript-container">
    <div class="transcript-header">
      <h2>Uploaded Transcript</h2>
    </div>
    <div class="transcript-content">
      <pre>{{ transcript }}</pre>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TranscriptView',
  props: {
    transcript: {
      type: String,
      required: true,
      default: ''
    }
  }
};
</script>

<style>
.transcript-container {
  background-color: white;
  border-radius: 0.5rem;
  overflow: hidden;
}

.transcript-header {
  padding: 1rem 1.5rem;
  background-color: #f9fafb;
  border-bottom: 1px solid var(--border-color);
}

.transcript-header h2 {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-color);
  margin: 0;
}

.transcript-content {
  padding: 1.5rem;
}

.transcript-content pre {
  white-space: pre-wrap;
  font-size: 0.875rem;
  color: var(--text-color);
  background-color: #f9fafb;
  border-radius: 0.375rem;
  padding: 1rem;
  overflow: auto;
  max-height: 400px;
  border: 1px solid var(--border-color);
}
</style>
