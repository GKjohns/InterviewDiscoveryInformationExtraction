<!-- App.vue -->
<template>
  <div class="app-container">
    <nav class="app-nav">
      <div class="nav-content">
        <h1 class="app-title">Customer Discovery Insights</h1>
      </div>
    </nav>

    <main class="app-main">
      <div class="upload-section">
        <input type="file" @change="handleFileUpload" accept=".txt" class="file-input" ref="fileInput" />
        <button @click="$refs.fileInput.click()" class="upload-button">
          Upload Transcript
        </button>
      </div>

      <div class="content-container">
        <div class="tabs">
          <button
            v-for="tab in tabs"
            :key="tab.name"
            @click="activeTab = tab.id"
            :class="['tab-button', { active: activeTab === tab.id }]"
          >
            <i :class="tab.icon"></i>
            {{ tab.name }}
          </button>
        </div>

        <div class="tab-content">
          <div v-if="loading" class="loading-container">
            <div class="loading-spinner"></div>
            <p class="loading-text">{{ currentFunFact }}</p>
          </div>

          <div v-else-if="error" class="error-message">
            {{ error }}
          </div>

          <div v-else>
            <TranscriptView
              v-if="activeTab === 'transcript'"
              :transcript="transcript"
            />
            <ReportView
              v-if="activeTab === 'report'"
              :report="report"
            />
            <InsightsView
              v-if="activeTab === 'insights'"
              :insights="insights"
            />
          </div>
        </div>
      </div>
    </main>

    <footer class="app-footer">
      <div class="footer-content">
        Powered by
        <a href="https://www.ara.social" target="_blank" class="footer-link">
          Ara Platforms
        </a>
      </div>
    </footer>
  </div>
</template>

<script>
import { ref, computed } from 'vue';
import axios from 'axios';
import TranscriptView from './components/TranscriptView.vue';
import ReportView from './components/ReportView.vue';
import InsightsView from './components/InsightsView.vue';
import { funFacts } from './utils/funFacts';

export default {
  name: 'App',
  components: {
    TranscriptView,
    ReportView,
    InsightsView
  },
  setup() {
    const activeTab = ref('transcript');
    const transcript = ref('');
    const report = ref('');
    const insights = ref({
      user_problems: [],
      opportunities: [],
      user_motivations: []
    });
    const loading = ref(false);
    const error = ref('');
    const currentFunFact = ref('');

    const tabs = computed(() => [
      { id: 'transcript', name: 'Transcript', icon: 'fas fa-file-alt' },
      { id: 'report', name: 'Analysis Report', icon: 'fas fa-chart-bar' },
      { id: 'insights', name: 'Extracted Insights', icon: 'fas fa-list' }
    ]);

    const handleFileUpload = async (event) => {
      const file = event.target.files[0];
      if (!file) return;

      loading.value = true;
      error.value = '';
      currentFunFact.value = funFacts[Math.floor(Math.random() * funFacts.length)];

      try {
        const reader = new FileReader();
        const fileContent = await new Promise((resolve, reject) => {
          reader.onload = (e) => resolve(e.target.result);
          reader.onerror = reject;
          reader.readAsText(file);
        });

        transcript.value = fileContent;

        const response = await axios.post('http://localhost:5010/api/generate_report', {
          transcript: fileContent,
        });

        report.value = response.data.summary;
        insights.value = response.data.extracted_insights || {
          user_problems: [],
          opportunities: [],
          user_motivations: []
        };

        activeTab.value = 'report';
      } catch (e) {
        error.value = 'An error occurred while analyzing the transcript. Please try again.';
        console.error('Error:', e);
      } finally {
        loading.value = false;
      }
    };

    return {
      activeTab,
      transcript,
      report,
      insights,
      loading,
      error,
      currentFunFact,
      tabs,
      handleFileUpload
    };
  }
};
</script>

<style>
:root {
  --primary-color: #3b82f6;
  --primary-dark: #2563eb;
  --background-color: #f3f4f6;
  --text-color: #1f2937;
  --text-light: #6b7280;
  --border-color: #e5e7eb;
}

body {
  font-family: 'Inter', sans-serif;
  background-color: var(--background-color);
  color: var(--text-color);
  margin: 0;
  padding: 0;
}

.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.app-nav {
  background-color: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.nav-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
}

.app-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--primary-color);
  margin: 0;
}

.app-main {
  flex-grow: 1;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.upload-section {
  margin-bottom: 2rem;
}

.file-input {
  display: none;
}

.upload-button {
  background-color: var(--primary-color);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: 500;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.upload-button:hover {
  background-color: var(--primary-dark);
}

.content-container {
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.tabs {
  display: flex;
  border-bottom: 1px solid var(--border-color);
}

.tab-button {
  flex-grow: 1;
  padding: 1rem;
  font-size: 1rem;
  font-weight: 500;
  color: var(--text-light);
  background-color: transparent;
  border: none;
  cursor: pointer;
  transition: color 0.2s, border-color 0.2s;
}

.tab-button.active {
  color: var(--primary-color);
  border-bottom: 2px solid var(--primary-color);
}

.tab-button i {
  margin-right: 0.5rem;
}

.tab-content {
  padding: 2rem;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 200px;
}

.loading-spinner {
  border: 4px solid var(--border-color);
  border-top: 4px solid var(--primary-color);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-text {
  margin-top: 1rem;
  color: var(--text-light);
}

.error-message {
  color: #dc2626;
  text-align: center;
}

.app-footer {
  background-color: white;
  border-top: 1px solid var(--border-color);
  padding: 1rem;
  text-align: center;
}

.footer-content {
  font-size: 0.875rem;
  color: var(--text-light);
}

.footer-link {
  color: var(--primary-color);
  text-decoration: none;
}

.footer-link:hover {
  text-decoration: underline;
}
</style>
