from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import sys
from pathlib import Path
from llm import extraction_chain, summary_chain  # Import the chains

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/', methods=['GET'])
def home():
    # Get the current date and time
    current_time = datetime.now().strftime("%A, %B %d, %Y %I:%M %p")
    return jsonify({'message': 'Server is working', 'current_time': current_time})

@app.route('/api/generate_report', methods=['POST'])
def generate_report():
    data = request.json
    transcript = data.get('transcript', '')

    if not transcript:
        return jsonify({'error': 'Transcript is required'}), 400

    try:
        extraction_output = extraction_chain.invoke({'transcript': transcript})
        summary_output = summary_chain.invoke({
            'transcript': transcript,
            'extracted_insights': extraction_output
        })

        return jsonify({
            'extracted_insights': extraction_output,
            'summary': summary_output['report'],
            'key_takeaway': summary_output['key_takeaway']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010)
