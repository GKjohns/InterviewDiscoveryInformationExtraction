<!-- App.vue -->
<template>
  <div class="app-container">
    <div class="sidebar">
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

      <div class="analyze-section">
        <button 
          @click="analyzeTranscript" 
          class="analyze-button" 
          :class="{ 'active-button': isFileSelected }" 
          :disabled="!file"
        >
          <span class="icon">↑</span> Analyze Transcript
        </button>

        <div v-if="loading" class="loading-indicator">
          <div class="loading-spinner"></div>
          <div class="loading-text">
            <p>Analyzing transcript...</p>
            <p class="fun-fact">{{ currentFunFact }}</p>
          </div>
        </div>
      </div>

      <div v-if="transcript" class="tab-container">
        <h3 class="tab-title">View Options</h3>
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
      </div>

      <div v-if="error" class="error-message">
        {{ error }}
      </div>

      <div v-if="!transcript" class="upload-prompt">
        <p>Upload a transcript file to begin analysis.</p>
      </div>
    </div>

    <div class="main-content">
      <div v-if="transcript" class="content-wrapper">
        <div class="content-area">
          <!-- <h2>{{ activeTab === 'transcript' ? 'Original Transcript' : activeTab === 'summary' ? 'Summary' : 'Structured Data' }}</h2> -->
          <TranscriptView v-if="activeTab === 'transcript'" :transcript="transcript" />
          <ReportView v-else-if="activeTab === 'summary'" :report="report" />
          <InsightsView v-else :insights="extractedInsights" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
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

const isFileSelected = computed(() => !!file.value);
</script>

<style scoped>
.app-container {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
  display: flex;
  height: 100vh;
}

.sidebar {
  width: 250px;
  min-width: 250px;
  padding: 20px;
  background-color: #f8f8f8;
  border-right: 1px solid #e0e0e0;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

.main-content {
  flex-grow: 1;
  padding: 20px;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

.title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 30px;
}

.file-input-container {
  margin-bottom: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
}

.file-input-label {
  background-color: #f0e6ff;
  color: #5000b8;
  padding: 12px 20px;
  cursor: pointer;
  font-weight: 500;
  font-size: 16px;
  display: block;
}

.file-input {
  display: none;
}

.file-name {
  padding: 10px;
  color: #666;
  font-size: 14px;
  display: block;
}

.analyze-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 30px;
}

.analyze-button {
  background-color: #808080;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  transition: background-color 0.3s ease;
  flex-shrink: 0;
  width: 100%;
}

.analyze-button.active-button {
  background-color: #5000b8;
}

.analyze-button:disabled {
  background-color: #808080;
  cursor: not-allowed;
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
  padding: 12px 15px;
  cursor: pointer;
  font-size: 16px;
}

.tab-button.active {
  background-color: #f0f0f0;
  font-weight: 500;
}

.content-area {
  background-color: #ffffff;
  padding: 30px;
  border-radius: 4px;
  flex-grow: 1;
  overflow-y: auto;
  border: 1px solid #e0e0e0;
}

.content-area h2 {
  font-size: 20px;
  margin-bottom: 20px;
}

.loading-indicator {
  display: flex;
  align-items: center;
  padding: 10px;
  background-color: #f0f0f0;
  border-radius: 4px;
  flex-shrink: 0;
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
  display: flex;
  flex-direction: column;
  height: 100%;
}

.upload-prompt {
  margin-top: auto;
  text-align: center;
  padding: 20px;
  background-color: #f0f0f0;
  border-radius: 4px;
}

.upload-prompt p {
  font-size: 16px;
  color: #666;
}

.tab-container {
  margin-top: 20px;
}

.tab-title {
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 10px;
}

.tabs {
  display: flex;
  flex-direction: column;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
}

.tab-button {
  background: none;
  border: none;
  padding: 12px 15px;
  cursor: pointer;
  font-size: 14px;
  text-align: left;
  border-bottom: 1px solid #e0e0e0;
}

.tab-button:last-child {
  border-bottom: none;
}

.tab-button.active {
  background-color: #f0e6ff;
  color: #5000b8;
  font-weight: 500;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
