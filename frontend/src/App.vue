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
          :class="{ 'active-button': isFileSelected, 'loading': loading }" 
          :disabled="!file || loading"
        >
          <span v-if="!loading">
            <span class="icon">↑</span> Analyze Transcript
          </span>
          <span v-else class="loading-dots">
            <span>.</span><span>.</span><span>.</span>
          </span>
        </button>

        <div v-if="loading" class="fun-fact">
          Did you know? {{ currentFunFact }}
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
      <div v-else class="empty-state">
        <div class="empty-state-content">
          <h2>Welcome to UX Interview Analyzer</h2>
          <p>Transform your user interview transcripts into actionable insights</p>
          
          <div class="steps-container">
            <div class="step">
              <div class="step-number">1</div>
              <div class="step-text">
                <h3>Upload Your Transcript</h3>
                <p>Select a .txt file containing your interview transcript</p>
              </div>
            </div>
            <div class="step">
              <div class="step-number">2</div>
              <div class="step-text">
                <h3>Analyze Content</h3>
                <p>Our AI will process your transcript and extract key insights</p>
              </div>
            </div>
            <div class="step">
              <div class="step-number">3</div>
              <div class="step-text">
                <h3>Review Insights</h3>
                <p>View the summary, key findings, and structured data</p>
              </div>
            </div>
          </div>
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

<style>
/* Global styles */
html, body {
  height: 100%;
  margin: 0;
  overflow: hidden;
}

/* Modify the .app-container */
.app-container {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
  display: flex;
  height: 100vh; /* Changed from 100% to 100vh */
  overflow: hidden;
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
  user-select: none;
  height: 100vh; /* Changed from 100% to 100vh */
}

.main-content {
  flex-grow: 1;
  padding: 20px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  height: 100vh; /* Changed from 100% to 100vh */
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
  position: relative;
  overflow: hidden;
}

.analyze-button.active-button {
  background-color: #5000b8;
}

.analyze-button:disabled {
  background-color: #808080;
  cursor: not-allowed;
}

.analyze-button.loading {
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
  height: 100%;
  max-height: calc(100vh - 80px); /* Changed from 40px to 80px to account for padding */
  padding-bottom: 30px; /* Explicitly set bottom padding */
  margin-bottom: 20px; /* Add margin at bottom */
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
  text-align: center;
  font-style: italic;
  color: #666;
  font-size: 14px;
  margin-top: 10px;
}

.error-message {
  color: #ff0000;
  margin-top: 20px;
  text-align: center;
}

.content-wrapper {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  overflow: hidden;
  padding: 20px; /* Changed from padding-bottom to full padding */
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

.loading-dots {
  display: flex;
  justify-content: center;
  align-items: center;
}

.loading-dots span {
  animation: loadingDots 1.4s infinite ease-in-out both;
  font-size: 24px;
  margin: 0 2px;
}

.loading-dots span:nth-child(1) {
  animation-delay: -0.32s;
}

.loading-dots span:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes loadingDots {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.file-input-label,
.analyze-button,
.tab-button,
.upload-prompt,
.tab-title {
  user-select: none; /* Make text non-highlightable */
}

/* Add these new styles */
.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  padding: 20px;
}

.empty-state-content {
  max-width: 800px;
  text-align: center;
  padding: 40px;
  background: white;
  border-radius: 8px;
  /* Removed: box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05); */
}

.empty-state-content h2 {
  font-size: 28px;
  color: #5000b8;
  margin-bottom: 12px;
}

.empty-state-content > p {
  font-size: 18px;
  color: #666;
  margin-bottom: 40px;
}

.steps-container {
  display: flex;
  gap: 30px;
  justify-content: center;
  flex-wrap: wrap;
}

.step {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  text-align: left;
  padding: 20px;
  background: white;  /* Changed from #f8f8f8 to white */
  border: 1px solid #e0e0e0;  /* Added border */
  border-radius: 8px;
  width: 280px;
  transition: box-shadow 0.2s ease;  /* Optional: adds subtle hover effect */
}

.step:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);  /* Optional: adds subtle hover effect */
}

.step-number {
  background: #5000b8;
  color: white;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  flex-shrink: 0;
}

.step-text h3 {
  font-size: 16px;
  margin: 0 0 8px 0;
  color: #333;
}

.step-text p {
  font-size: 14px;
  color: #666;
  margin: 0;
  line-height: 1.4;
}
</style>

