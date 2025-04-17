import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "mistralai/mixtral-8x7b-instruct"  # You can also try "anthropic/claude-3-haiku"

@app.route("/")
def index():
    return "LLM Equation Solver API is Live!"

@app.route("/solve", methods=["POST"])
def solve_equation():
    try:
        data = request.get_json()
        eqn = data.get("equation", "")
        
        prompt = prompt = f"""
Solve the following equation step by step.
Display only the working steps and the final answer.
Do not explain anything or label the steps.
Each step should be on a new line.
Keep each step under 30 characters.
Equation: {eqn}
""" 

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
        )

        res_json = response.json()
        answer = res_json["choices"][0]["message"]["content"]

        return jsonify({"steps": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)

   
