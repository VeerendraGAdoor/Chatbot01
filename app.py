import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

app = Flask(__name__)

# Configure Gemini Model
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")  # text model

@app.route("/", methods=["GET"])
def home():
    return "Webhook is running ✅", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(force=True)

    # Extract user message from Dialogflow
    user_message = req["queryResult"]["queryText"]

    # Generate response using Gemini
    response = model.generate_content(user_message)
    bot_reply = response.text

    # Return to Dialogflow
    return jsonify({"fulfillmentText": bot_reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
