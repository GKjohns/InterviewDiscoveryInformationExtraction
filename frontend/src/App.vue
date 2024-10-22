<!-- App.vue -->
<template>
  <div class="app-container">
    <h1 class="title">UX Interview Analyzer</h1>
    
    <div class="file-input-container">
      <label for="file-upload" class="file-input-label">
        Choose File
      </label>
      <input 
        id="file-upload" 
        type="file" 
        @change="handleFileUpload" 
        accept=".txt"
        class="file-input"
      >
      <span class="file-name">{{ fileName || 'No file chosen' }}</span>
    </div>

    <button @click="analyzeTranscript" class="analyze-button" :disabled="!file">
      <span class="icon">↑</span> Analyze Transcript
    </button>

    <div v-if="loading" class="loading-indicator">
      <div class="loading-spinner"></div>
      <div class="loading-text">
        <p>Analyzing transcript...</p>
        <p class="fun-fact">{{ currentFunFact }}</p>
      </div>
    </div>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <div v-if="transcript" class="content-wrapper">
      <div class="tabs">
        <button 
          v-for="tab in tabs" 
          :key="tab.id"
          @click="activeTab = tab.id"
          :class="['tab-button', { active: activeTab === tab.id }]"
        >
          {{ tab.name }}
        </button>
      </div>

      <div class="content-area">
        <h2>{{ activeTab === 'transcript' ? 'Original Transcript' : activeTab === 'summary' ? 'Summary' : 'Structured Data' }}</h2>
        <TranscriptView v-if="activeTab === 'transcript'" :transcript="transcript" />
        <ReportView v-else-if="activeTab === 'summary'" :report="report" />
        <InsightsView v-else :insights="extractedInsights" />
      </div>
    </div>

    <div v-else class="upload-prompt">
      <p>Upload a transcript file to begin analysis.</p>
    </div>
    
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import TranscriptView from './components/TranscriptView.vue';
import ReportView from './components/ReportView.vue';
import InsightsView from './components/InsightsView.vue';

const file = ref(null);
const fileName = ref('');
const transcript = ref('');
const report = ref('');
const extractedInsights = ref({ user_problems: [], opportunities: [], user_motivations: [] });
const activeTab = ref('transcript');
const loading = ref(false);
const error = ref('');
const currentFunFact = ref('');

const tabs = [
  { id: 'transcript', name: 'Original Transcript' },
  { id: 'summary', name: 'Summary' },
  { id: 'structured', name: 'Structured Data' },
];

const handleFileUpload = (event) => {
  file.value = event.target.files[0];
  fileName.value = file.value ? file.value.name : '';
};

const analyzeTranscript = async () => {
  if (!file.value) return;

  loading.value = true;
  error.value = '';
  report.value = '';
  extractedInsights.value = { user_problems: [], opportunities: [], user_motivations: [] };
  currentFunFact.value = getRandomFunFact();

  try {
    transcript.value = await readFileContent(file.value);
    const response = await axios.post('http://localhost:5010/api/generate_report', {
      transcript: transcript.value,
    });

    report.value = response.data.summary;
    extractedInsights.value = response.data.extracted_insights || extractedInsights.value;
    activeTab.value = 'summary';
  } catch (err) {
    error.value = 'An error occurred while analyzing the transcript. Please try again.';
    console.error('Error:', err);
  } finally {
    loading.value = false;
  }
};

const readFileContent = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = (event) => resolve(event.target.result);
    reader.onerror = (error) => reject(error);
    reader.readAsText(file);
  });
};

const getRandomFunFact = () => {
  const funFacts = [
    "Did you know? The first computer bug was an actual bug!",
    "The term 'debugging' originated from removing an actual moth from a computer.",
    "The first computer mouse was made of wood!",
    "The first programmer in the world was a woman named Ada Lovelace.",
    "The first computer virus was created in 1983 as an experiment.",
  ];
  return funFacts[Math.floor(Math.random() * funFacts.length)];
};
</script>

<style scoped>
.app-container {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
}

.file-input-container {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
}

.file-input-label {
  background-color: #f0e6ff;
  color: #5000b8;
  padding: 10px 15px;
  cursor: pointer;
  font-weight: 500;
}

.file-input {
  display: none;
}

.file-name {
  padding: 0 15px;
  color: #666;
}

.analyze-button {
  background-color: #808080;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  font-size: 14px;
  margin-bottom: 20px;
}

.icon {
  margin-right: 8px;
}

.tabs {
  display: flex;
  margin-bottom: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
}

.tab-button {
  flex: 1;
  background: none;
  border: none;
  padding: 10px;
  cursor: pointer;
  font-size: 14px;
}

.tab-button.active {
  background-color: #f0f0f0;
  font-weight: 500;
}

.content-area {
  background-color: #f8f8f8;
  padding: 20px;
  border-radius: 4px;
  height: 400px; /* Set a fixed height */
  overflow-y: auto; /* Enable vertical scrolling */
}

.content-area h2 {
  font-size: 18px;
  margin-bottom: 10px;
}

.transcript, .summary, .structured-data {
  font-family: monospace;
  white-space: pre-wrap;
  word-break: break-word;
}

.loading-indicator {
  display: flex;
  align-items: center;
  margin-top: 10px;
  padding: 10px;
  background-color: #f0f0f0;
  border-radius: 4px;
}

.loading-spinner {
  border: 2px solid #f3f3f3;
  border-top: 2px solid #3498db;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  animation: spin 1s linear infinite;
  margin-right: 10px;
}

.loading-text {
  flex: 1;
}

.loading-text p {
  margin: 0;
  font-size: 14px;
}

.fun-fact {
  font-style: italic;
  color: #666;
  font-size: 12px;
}

.error-message {
  color: #ff0000;
  margin-top: 20px;
  text-align: center;
}

.content-wrapper {
  margin-top: 20px;
}

.upload-prompt {
  text-align: center;
  margin-top: 40px;
  padding: 20px;
  background-color: #f8f8f8;
  border-radius: 4px;
}

.upload-prompt p {
  font-size: 16px;
  color: #666;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
