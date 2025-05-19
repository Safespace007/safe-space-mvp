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
        # Free public Hugging Face model (no token needed)
        hf_response = requests.post(
            "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium",
            json={"inputs": {
                "text": user_message
            }}
        )

        data = hf_response.json()

        # Extract generated text (fallback message included)
        reply = data.get("generated_text", "I'm here for you, but I didn’t quite understand that.")

        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
