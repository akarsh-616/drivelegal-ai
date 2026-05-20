from flask import Flask, render_template, request, jsonify
from rapidfuzz import fuzz
from googletrans import Translator
import google.generativeai as genai
import pytesseract
from PIL import Image
import speech_recognition as sr
import requests
import json
import os
import re
import spacy

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# =====================================================
# FLASK APP
# =====================================================

app = Flask(__name__)

# =====================================================
# GEMINI AI SETUP
# =====================================================

# Replace with your Gemini API Key
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

# =====================================================
# TESSERACT OCR PATH
# =====================================================

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# =====================================================
# SPACY NLP MODEL
# =====================================================

nlp = spacy.load("en_core_web_sm")

# =====================================================
# TRANSLATOR
# =====================================================

translator = Translator()

# =====================================================
# BASE DIRECTORY
# =====================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# =====================================================
# LOAD RULES
# =====================================================

RULES_PATH = os.path.join(BASE_DIR, "rules.json")

with open(RULES_PATH, "r", encoding="utf-8") as f:

    rules = json.load(f)

# =====================================================
# TRAINING DATASET
# =====================================================

training_sentences = {

    "helmet": [

        "no helmet",
        "helmet nahi pehna",
        "forgot helmet",
        "without helmet",
        "bina helmet",
        "helmet missing",
        "helmet bhool gaya"
    ],

    "signal_jump": [

        "jumped red light",
        "signal break",
        "signal tod diya",
        "crossed red signal",
        "red light jump",
        "traffic signal break"
    ],

    "drunk_driving": [

        "drink and drive",
        "drunk driving",
        "alcohol driving",
        "pee kar gaadi chalana",
        "drunk drive"
    ],

    "license": [

        "without license",
        "license nahi hai",
        "forgot driving license",
        "no license"
    ],

    "triple_riding": [

        "3 people on bike",
        "three riding",
        "triple riding"
    ]
}

# =====================================================
# CLEAN TEXT
# =====================================================

def clean_text(text):

    # remove emojis
    text = re.sub(r'[^\w\s]', ' ', text)

    # lowercase
    text = text.lower()

    # remove extra spaces
    text = " ".join(text.split())

    return text

# =====================================================
# TRANSLATE TO ENGLISH
# =====================================================

def translate_to_english(text):

    try:

        translated = translator.translate(
            text,
            dest='en'
        )

        return translated.text.lower()

    except:

        return text.lower()

# =====================================================
# NLP INTENT DETECTION
# =====================================================

def detect_intent(user_text):

    best_intent = None

    best_score = 0

    for intent, examples in training_sentences.items():

        for example in examples:

            vectorizer = TfidfVectorizer()

            vectors = vectorizer.fit_transform(
                [user_text, example]
            )

            similarity = cosine_similarity(
                vectors[0:1],
                vectors[1:2]
            )[0][0]

            if similarity > best_score:

                best_score = similarity

                best_intent = intent

    if best_score > 0.3:

        return best_intent

    return None

# =====================================================
# HOME ROUTE
# =====================================================

@app.route("/")
def home():

    return render_template("index.html")

# =====================================================
# CHATBOT ROUTE
# =====================================================

@app.route("/chat", methods=["POST"])
def chat():

    data = request.json

    message = data.get("message", "")

    # clean text
    message = clean_text(message)

    # translate to english
    message = translate_to_english(message)

    # NLP intent detection
    matched_rule = detect_intent(message)

    # =================================================
    # LOCAL RULE ENGINE
    # =================================================

    if matched_rule:

        fine = rules.get(matched_rule, 1000)

        reply = f"""
🚨 Violation Detected

📌 Violation:
{matched_rule.replace('_', ' ').title()}

💰 Estimated Fine:
₹{fine}

⚖️ Please follow traffic rules carefully.
"""

        return jsonify({
            "reply": reply
        })

    # =================================================
    # GEMINI AI FALLBACK
    # =================================================

    try:

        prompt = f"""
You are DriveLegal AI.

Answer traffic law questions simply.

User Question:
{message}
"""

        response = model.generate_content(prompt)

        return jsonify({
            "reply": response.text
        })

    except Exception as e:

        return jsonify({
            "reply": f"AI Error: {str(e)}"
        })

# =====================================================
# OCR IMAGE READER
# =====================================================

@app.route("/ocr", methods=["POST"])
def ocr():

    try:

        image = request.files["image"]

        upload_folder = os.path.join(
            BASE_DIR,
            "uploads"
        )

        if not os.path.exists(upload_folder):

            os.makedirs(upload_folder)

        image_path = os.path.join(
            upload_folder,
            image.filename
        )

        image.save(image_path)

        img = Image.open(image_path)

        extracted_text = pytesseract.image_to_string(img)

        return jsonify({
            "text": extracted_text
        })

    except Exception as e:

        return jsonify({
            "text": f"OCR Error: {str(e)}"
        })

# =====================================================
# VOICE RECOGNITION
# =====================================================

@app.route("/voice", methods=["POST"])
def voice():

    try:

        recognizer = sr.Recognizer()

        audio_file = request.files["audio"]

        upload_folder = os.path.join(
            BASE_DIR,
            "uploads"
        )

        if not os.path.exists(upload_folder):

            os.makedirs(upload_folder)

        audio_path = os.path.join(
            upload_folder,
            audio_file.filename
        )

        audio_file.save(audio_path)

        with sr.AudioFile(audio_path) as source:

            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio)

        return jsonify({
            "text": text
        })

    except Exception as e:

        return jsonify({
            "text": f"Voice Error: {str(e)}"
        })

# =====================================================
# GPS LOCATION DETECTION
# =====================================================

@app.route("/location", methods=["POST"])
def location():

    data = request.json

    latitude = data.get("latitude")
    longitude = data.get("longitude")

    try:

        url = (
            f"https://nominatim.openstreetmap.org/reverse"
            f"?format=json&lat={latitude}&lon={longitude}"
        )

        headers = {
            "User-Agent": "DriveLegalAI"
        }

        response = requests.get(
            url,
            headers=headers
        )

        location_data = response.json()

        address = location_data.get(
            "address",
            {}
        )

        city = (
            address.get("city")
            or address.get("town")
            or address.get("village")
            or "Unknown City"
        )

        state = address.get(
            "state",
            "Unknown State"
        )

        country = address.get(
            "country",
            "Unknown Country"
        )

        return jsonify({
            "city": city,
            "state": state,
            "country": country
        })

    except Exception as e:

        return jsonify({
            "city": "Unknown",
            "state": "Unknown",
            "country": "Unknown",
            "error": str(e)
        })

# =====================================================
# TEST ROUTE
# =====================================================

@app.route("/test")
def test():

    return "DriveLegal AI Running Successfully ✅"

# =====================================================
# RUN APP
# =====================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )