import os
import json
import requests
import google.generativeai as genai

def _get_mock_response(notes, difficulty, exam_mode):
    """Fallback method for when no API key is provided."""
    import time
    time.sleep(1)  # Simulate network delay
    return {
        "summary": "This is a mocked summary of your notes. Since no Gemini API key was provided, we're returning this dummy data. " + notes[:50] + "...",
        "top5": [
            {"concept": "Mock Concept 1", "explanation": "Explanation 1"},
            {"concept": "Mock Concept 2", "explanation": "Explanation 2"},
            {"concept": "Mock Concept 3", "explanation": "Explanation 3"},
            {"concept": "Mock Concept 4", "explanation": "Explanation 4"},
            {"concept": "Mock Concept 5", "explanation": "Explanation 5"},
        ],
        "quiz": [
            {"question": "What is 1 + 1?", "options": ["1", "2", "3", "4"], "answer": "2"}
        ] if exam_mode else [],
        "meme_suggestion": {
            "template_id": "112126428",  # Distracted Boyfriend
            "text0": "Me studying",
            "text1": "These mock notes"
        }
    }

def generate_study_material(notes, difficulty, exam_mode):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("WARNING: No GEMINI_API_KEY set. Returning mock response.")
        return _get_mock_response(notes, difficulty, exam_mode)

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""
You are an AI Study Assistant. Your job is to process student notes and output a JSON response containing: a summary, top 5 concepts, a quiz (if required), and a meme suggestion.

Difficulty level: {difficulty} (Adjust the language and depth of your explanations accordingly).
Exam Mode: {'ON. Include a 3-question multiple-choice quiz.' if exam_mode else 'OFF. Quiz is not required (return empty array).'}

Meme Suggestion: Choose ONE of the following Imgflip template IDs that best fits a humorous take on the notes:
- 181913649 (Drake Hotline Bling) -> text0: (top, reject), text1: (bottom, accept)
- 87743020 (Two Buttons) -> text0: (left button), text1: (right button)
- 112126428 (Distracted Boyfriend) -> text0: (girlfriend/distraction), text1: (guy)
- 129242436 (Change My Mind) -> text0: (banner text)
- 93895088 (Expanding Brain) -> text0: (small brain), text1: (bigger brain)
- 89370399 (Roll Safe Think About It) -> text0: (top), text1: (bottom)

Notes to process:

{notes}

Output ONLY a valid JSON object (no markdown, no code fences) in this format:
{{
    "summary": "A concise paragraph summarizing the notes.",
    "top5": [
        {{"concept": "Name of concept", "explanation": "Short explanation"}}
    ],
    "quiz": [
        {{"question": "Question text", "options": ["A", "B", "C", "D"], "answer": "Correct Option"}}
    ],
    "meme_suggestion": {{
        "template_id": "Chosen template ID string",
        "text0": "Text for box 1",
        "text1": "Text for box 2 (if applicable, else empty string)"
    }}
}}
"""

    response = model.generate_content(prompt)
    raw = response.text.strip()

    # Strip markdown code fences if Gemini wraps the JSON
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    return json.loads(raw)


def generate_meme(template_id, text0, text1):
    username = os.getenv("IMGFLIP_USERNAME")
    password = os.getenv("IMGFLIP_PASSWORD")

    if not username or not password:
        print("WARNING: IMGFLIP credentials not set. Returning a placeholder meme.")
        return "https://i.imgflip.com/1ur9b0.jpg"

    url = "https://api.imgflip.com/caption_image"

    data = {
        "template_id": template_id,
        "username": username,
        "password": password,
        "text0": text0,
        "text1": text1
    }

    response = requests.post(url, data=data)
    result = response.json()

    if result.get("success"):
        return result["data"]["url"]
    else:
        print("Imgflip Error:", result.get("error_message"))
        return None
