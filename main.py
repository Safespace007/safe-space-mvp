from flask import Flask, request, render_template, jsonify
import requests
import os

app = Flask(__name__)

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_message = request.json["message"]

    try:
        response = requests.post(
            "https://api.together.xyz/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {TOGETHER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
                "messages": [
                    {"role": "system", "content": "You are Safe Space, a warm, emotionally intelligent AI who helps people reflect, feel heard, and make peace with their thoughts."},
                    {"role": "user", "content": user_message}
                ],
                "max_tokens": 512,
                "temperature": 0.8
            }
        )

        reply = response.json()["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
