<template>
  <div class="extractor-container">
    <div class="main-content">
      <div class="content">
        <h1>Customer Discovery Insights Extractor</h1>
        <input type="file" @change="handleFileUpload" accept=".txt" />
        <button @click="analyzeTranscript" :disabled="!file">Analyze Transcript</button>

        <div v-if="loading" class="loading">
          <p>Analyzing transcript... This should take about 10-15 seconds.</p>
          <p>Did you know? {{ currentFunFact }}</p>
          <div class="loading-animation">
            <div class="dot"></div>
            <div class="dot"></div>
            <div class="dot"></div>
          </div>
        </div>

        <div v-if="error" class="error">
          {{ error }}
        </div>
      </div>

      <div v-if="report" class="results">
        <div class="markdown-content" v-html="renderedReport"></div>
        
        <!-- Visual separator -->
        <hr class="separator" />

        <!-- Display extracted insights -->
        <div class="insights">
          <h2>User Problems</h2>
          <ul v-if="extractedInsights && extractedInsights.user_problems && extractedInsights.user_problems.length">
            <li v-for="(problem, index) in extractedInsights.user_problems" :key="index">
              <strong>{{ problem.problem }}</strong> {{ problem.context }}
            </li>
          </ul>
          <p v-else>No user problems identified.</p>

          <h2>Opportunities</h2>
          <ul v-if="extractedInsights && extractedInsights.opportunities && extractedInsights.opportunities.length">
            <li v-for="(opportunity, index) in extractedInsights.opportunities" :key="index">
              <strong>{{ opportunity.opportunity }}</strong> {{ opportunity.potential_impact }}
            </li>
          </ul>
          <p v-else>No opportunities identified.</p>

          <h2>User Motivations</h2>
          <ul v-if="extractedInsights && extractedInsights.user_motivations && extractedInsights.user_motivations.length">
            <li v-for="(motivation, index) in extractedInsights.user_motivations" :key="index">
              <strong>{{ motivation.motivation }}</strong> {{ motivation.underlying_need }}
            </li>
          </ul>
          <p v-else>No user motivations identified.</p>
        </div>
      </div>
    </div>

    <div v-if="isModalOpen" class="modal">
      <div class="modal-content">
        <button class="close-button" @click="closeModal">Close</button>
        <div class="markdown-content" v-html="renderedReport"></div>
      </div>
    </div>

    <div class="footer">
      Powered by 
      <img src="https://www.kylejohnson.ai/img/ara_logo.png" alt="Ara Platforms">
      <a href="https://www.ara.social" target="_blank" class="footer-link"> Ara Platforms</a>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { marked } from 'marked';

export default {
  name: 'ExtractorComponent',
  data() {
    const funFacts = [
      "The term 'startup' was first popularized during the dot-com bubble in the late 1990s.",
      "Amazon started as an online bookstore in Jeff Bezos's garage in 1994.",
      "The average age of successful startup founders is 45, according to a study by MIT.",
      "Airbnb's founders once sold branded cereal to keep their startup afloat.",
      "The 'lean startup' methodology was introduced by Eric Ries in 2008.",
      "Instagram was created in just 8 weeks before its launch in 2010.",
      "The first business incubator opened in Batavia, New York in 1959.",
      "The term 'unicorn' for billion-dollar startups was coined by Aileen Lee in 2013.",
      "About 90% of startups fail, with 10% failing within the first year.",
      "The fastest company to reach a $1 billion valuation was Niantic, the maker of Pokémon Go.",
      "GitHub was created as a side project for the founders to work on during weekends.",
      "The average successful startup raises $41 million in venture capital.",
      "Dropbox grew its user base by 3900% in 15 months using a referral program.",
      "The term 'bootstrapping' comes from the phrase 'pulling yourself up by your bootstraps'.",
      "Y Combinator, one of the most famous startup accelerators, was founded in 2005.",
      "The first venture capital firm, ARD, was founded in 1946.",
      "Slack started as an internal tool for a gaming company before pivoting to become a communication platform.",
      "The 'fail fast' philosophy encourages entrepreneurs to quickly test and learn from failures.",
      "The global startup economy is worth nearly $3 trillion.",
      "Sweden has the most billion-dollar startups per capita in the world after Silicon Valley.",
      "The term 'pitch deck' originated from the days when entrepreneurs would present their ideas on overhead projectors.",
      "Google's first office was a garage rented from Susan Wojcicki, who later became CEO of YouTube.",
      "The first crowdfunding platform, ArtistShare, was launched in 2003.",
      "The 'freemium' business model was coined by venture capitalist Fred Wilson in 2006.",
      "PayPal was voted as the worst business idea of 1999 by Time Magazine.",
      "The term 'growth hacking' was coined by Sean Ellis in 2010.",
      "Zappos offered new employees $2,000 to quit to ensure only committed people stayed.",
      "The 'elevator pitch' concept comes from the idea of pitching an idea in the time it takes to ride an elevator.",
      "Netflix's original business model was DVD rentals by mail.",
      "The world's first business plan competition was held at the University of Texas at Austin in 1984.",
      "The 'MVP' (Minimum Viable Product) concept was introduced by Frank Robinson in 2001.",
      "Airbnb's founders used to photograph every property themselves in the early days.",
      "The term 'solopreneur' was first used in 1996 by Terri Lonier.",
      "Facebook's iconic blue color was chosen because Mark Zuckerberg is red-green colorblind.",
      "The first coworking space opened in San Francisco in 2005.",
      "Uber was originally called 'UberCab' and was conceived as a luxury car service.",
      "The 'subscription box' business model was pioneered by Birchbox in 2010.",
      "Tesla was founded by Martin Eberhard and Marc Tarpenning, not Elon Musk.",
      "The term 'pivot' in business was popularized by Eric Ries in his book 'The Lean Startup'.",
      "Stripe was founded by two Irish brothers, Patrick and John Collison."
    ];
    return {
      file: null,
      report: '',
      extractedInsights: { user_problems: [], opportunities: [], user_motivations: [] },
      loading: false,
      error: '',
      renderedReport: '',
      isModalOpen: false,
      funFacts,
      currentFunFact: '',
    };
  },
  methods: {
    handleFileUpload(event) {
      this.file = event.target.files[0];
    },
    async analyzeTranscript() {
      if (!this.file) return;

      this.loading = true;
      this.error = '';
      this.report = '';
      this.extractedInsights = { user_problems: [], opportunities: [], user_motivations: [] };
      this.renderedReport = '';
      this.currentFunFact = this.getRandomFunFact();

      try {
        const transcript = await this.readFileContent(this.file);
        const response = await axios.post('http://localhost:5010/api/generate_report', {
          transcript,
        });

        this.report = response.data.summary;
        this.renderedReport = marked(this.report);
        this.extractedInsights = response.data.extracted_insights || this.extractedInsights;
      } catch (error) {
        this.error = 'An error occurred while analyzing the transcript. Please try again.';
        console.error('Error:', error);
      } finally {
        this.loading = false;
      }
    },
    readFileContent(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (event) => resolve(event.target.result);
        reader.onerror = (error) => reject(error);
        reader.readAsText(file);
      });
    },
    openModal() {
      this.isModalOpen = true;
    },
    closeModal() {
      this.isModalOpen = false;
    },

    getRandomFunFact() {
      const randomIndex = Math.floor(Math.random() * this.funFacts.length);
      return this.funFacts[randomIndex];
    },
  },
};
</script>

<style scoped>
.extractor-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  box-sizing: border-box;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.content {
  flex-shrink: 0;
}

.results {
  flex-grow: 1;
  overflow-y: auto;
  margin-top: 20px;
}

.separator {
  margin: 20px 0;
  border: none;
  border-top: 1px solid #eaecef;
}

.insights {
  text-align: left; /* Ensure left alignment */
}

.footer {
  position: fixed;
  bottom: 0;
  right: 0;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding: 10px;
  background-color: white;
  z-index: 1000;
}

.footer img {
  height: 16px;
  margin-left: 5px;
  margin-right: 5px; /* Add this line to create space between the logo and the text */
}

h1, h2 {
  margin-bottom: 20px;
}

input[type="file"] {
  margin-bottom: 10px;
}

button {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.loading, .error {
  margin-top: 20px;
  font-weight: bold;
}

.error {
  color: red;
}

.results h2 {
  margin-top: 20px;
  margin-bottom: 15px;
}

.markdown-content {
  line-height: 1.6;
  font-size: 16px;
  text-align: left;
}

.markdown-content h1,
.markdown-content h2,
.markdown-content h3,
.markdown-content h4,
.markdown-content h5,
.markdown-content h6 {
  margin-top: 24px;
  margin-bottom: 16px;
  font-weight: 600;
  line-height: 1.25;
}

.markdown-content h1 {
  font-size: 2em;
  border-bottom: 1px solid #eaecef;
  padding-bottom: 0.3em;
}

.markdown-content h2 {
  font-size: 1.5em;
  border-bottom: 1px solid #eaecef;
  padding-bottom: 0.3em;
}

.markdown-content p {
  margin-bottom: 16px;
}

.markdown-content ul,
.markdown-content ol {
  padding-left: 2em;
  margin-bottom: 16px;
}

.markdown-content li {
  margin-bottom: 8px;
}

.markdown-content code {
  padding: 0.2em 0.4em;
  margin: 0;
  font-size: 85%;
  background-color: rgba(27,31,35,0.05);
  border-radius: 3px;
}

.json-content {
  background-color: #f4f4f4;
  padding: 15px;
  overflow-x: auto;
  white-space: pre-wrap;
  word-wrap: break-word;
  font-size: 14px;
  line-height: 1.5;
  border-radius: 4px;
  text-align: left;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}

.modal-content {
  background-color: white;
  padding: 20px;
  max-width: 90%;
  max-height: 90%;
  overflow-y: auto;
  border-radius: 8px;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: #f44336;
  color: white;
  border: none;
  padding: 10px;
  cursor: pointer;
  border-radius: 5px;
}

@media (max-width: 768px) {
  .extractor-container {
    padding: 10px;
  }

  h1 {
    font-size: 24px;
  }

  h2 {
    font-size: 20px;
  }

  button {
    width: 100%;
  }
}

.footer-link {
  color: inherit;
  text-decoration: none;
  transition: color 0.3s ease, text-decoration 0.3s ease;
}

.footer-link:hover {
  background: linear-gradient(90deg, #4A7A9D, #A3D5E0, #F8C2C9);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-decoration: underline;
}

.loading {
  margin-top: 20px;
  text-align: center;
}

.loading p {
  margin-bottom: 10px;
  font-weight: bold;
}

.loading-animation {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.dot {
  width: 10px;
  height: 10px;
  background-color: #4CAF50;
  border-radius: 50%;
  margin: 0 5px;
  animation: bounce 1.4s infinite ease-in-out both;
}

.dot:nth-child(1) {
  animation-delay: -0.32s;
}

.dot:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes bounce {
  0%, 80%, 100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}
</style>

