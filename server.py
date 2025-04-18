import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "google/gemini-pro"  # You can also try "mistralai/mixtral-8x7b-instruct"/"anthropic/claude-3-haiku"

@app.route("/")
def index():
    return "LLM Equation Solver API is Live!"

@app.route("/solve", methods=["POST"])
def solve_equation():
    try:
        data = request.get_json()
        eqn = data.get("equation", "")
        
        prompt = f"""
You are a step-by-step math solver. Your task is to solve engineering-level math equations by showing only the working steps required to reach the final answer.

- Do not include explanations or final answers.
- Break every step into small parts and write one operation per line.
- Do not skip algebraic simplifications or rearrangements.
- Do not include the word "Answer" or "= Final Result".
- The format should look like a chalkboard or exam working.
- Use LaTeX-like formatting for fractions, powers, and roots where needed, but keep it readable in plain text.

Now solve: {eqn}
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

   
