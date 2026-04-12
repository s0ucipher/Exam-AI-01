import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from services import generate_study_material, generate_meme

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/process-notes', methods=['POST'])
def process_notes():
    data = request.json
    if not data or not data.get('notes'):
        return jsonify({"error": "No notes provided"}), 400
    
    notes = data.get('notes')
    difficulty = data.get('difficulty', 'Medium')
    exam_mode = data.get('examMode', False)
    
    try:
        # 1. Ask OpenAI to extract summary, top 5, quiz, and recommend meme text + template
        ai_response = generate_study_material(notes, difficulty, exam_mode)
        
        meme_url = None
        # 2. Call Imgflip using the recommended template and text
        if ai_response.get("meme_suggestion"):
            meme_sugg = ai_response["meme_suggestion"]
            template_id = meme_sugg.get("template_id")
            text0 = meme_sugg.get("text0", "")
            text1 = meme_sugg.get("text1", "")
            
            if template_id:
                meme_url = generate_meme(template_id, text0, text1)
                
        ai_response["meme_url"] = meme_url

        return jsonify(ai_response)
    except Exception as e:
        print(f"Error processing notes: {str(e)}")
        return jsonify({"error": "An error occurred while processing notes."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
