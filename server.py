import os
import requests
from flask import Flask, request, jsonify, render_template_string
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
latest_expression = "No input received yet"

@app.route("/")
def index():
    return "LLM Equation Solver API is Live!"

@app.route('/test', methods=['POST'])
def test_post():
    global latest_expression
    data = request.get_json()
    latest_expression = data.get('expression', 'No expression received')
    return {"status": "received", "expression": latest_expression}

@app.route('/test', methods=['GET'])
def test_get():
    return render_template_string(f"""
        <html>
            <head><title>ESP32 Input</title></head>
            <body>
                <h2>Received Expression:</h2>
                <p style='font-size:24px; color:blue;'>{latest_expression}</p>
            </body>
        </html>
    """)

@app.route('/solve', methods=['POST'])
def solve_equation():
    data = request.get_json()
    user_equation = data.get('equation', '')

    prompt = f"""
You are a step-by-step math solver. Your task is to solve engineering-level math equations by showing only the working steps required to reach the final answer.

- Do not include explanations or final answers.
- Break every step into small parts and write one operation per line.
- Do not skip algebraic simplifications or rearrangements.
- Do not include the word "Answer" or "= Final Result".
- The format should look like a chalkboard or exam working.
- Use plain text with one step per line.

Now solve: {user_equation}
"""

    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

    response = requests.post(gemini_url, headers=headers, json=payload)

    try:
        raw_text = response.json()['candidates'][0]['content']['parts'][0]['text']
        lines = raw_text.strip().split('\n')
        steps = [line.strip() for line in lines if line.strip() and "=" in line and not any(kw in line.lower() for kw in ['answer', 'final'])]

        return jsonify({"steps": steps})

    except Exception as e:
        return jsonify({"error": str(e), "raw_response": response.text})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
