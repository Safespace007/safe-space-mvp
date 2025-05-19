from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_message = request.json["message"]

    try:
        prompt = f"""<|system|>
You are Safe Space, a calm, thoughtful, emotionally supportive AI that helps users feel understood and guided when they express emotional conflict.
</s>
<|user|>
{user_message}
</s>
<|assistant|>"""

        hf_response = requests.post(
            "https://api-inference.huggingface.co/models/OpenAssistant/oasst-sft-6-llama-30b",
            headers={"Accept": "application/json"},
            json={"inputs": prompt}
        )

        data = hf_response.json()

        reply = data.get("generated_text", "I'm listening. Tell me more about how you feel.")

        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
