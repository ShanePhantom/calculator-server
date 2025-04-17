import os
from flask import Flask, request, jsonify
from gemini_api import get_gemini_response

app = Flask(__name__)

def clean_gemini_response(raw_response: str):
    lines = raw_response.strip().split('\n')
    steps = [line.strip() for line in lines if line.strip()]
    steps = [step for step in steps if len(step) <= 30]
    return steps

@app.route("/")
def home():
    return "Hello! Calculator backend is running 🧠⚡"

@app.route("/solve", methods=["POST"])
def solve():
    equation = request.json.get("equation", "")
    prompt = f"""
Solve the following equation step by step.
Display only the working steps and the final answer.
Do not explain anything or label the steps.
Each step should be on a new line.
Keep each step under 30 characters.
Equation: {equation}
"""
    raw_response = get_gemini_response(prompt)
    steps = clean_gemini_response(raw_response)
    return jsonify({"response": steps})

if __name__ == "__main__":
    app.run()app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

