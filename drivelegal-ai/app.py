from flask import Flask, render_template, request, jsonify
import os
import re
import pytesseract
from PIL import Image
from werkzeug.utils import secure_filename
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# =========================================================
# FLASK APP
# =========================================================

app = Flask(__name__)

# =========================================================
# UPLOAD FOLDER
# =========================================================

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# =========================================================
# TESSERACT PATH
# =========================================================

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# =========================================================
# LEGAL DATASET
# =========================================================

legal_questions = [
    "what is fir",
    "how to file fir",
    "what is cyber crime",
    "what is ipc section 420",
    "women safety laws",
    "traffic challan rules",
    "consumer court",
    "online fraud",
    "divorce law",
    "property dispute",
    "cyber bullying",
    "helmet challan",
    "police complaint",
    "loan fraud",
    "domestic violence"
]

legal_answers = [
    "FIR means First Information Report. It is registered by police for a cognizable offence.",

    "You can file FIR by visiting nearest police station or using your state police online portal.",

    "Cyber crime includes hacking, online scams, phishing, identity theft and cyber bullying.",

    "IPC Section 420 relates to cheating and dishonestly inducing delivery of property.",

    "Women safety laws include Domestic Violence Act, POSH Act and IPC protections.",

    "Traffic challan penalties apply for no helmet, no seatbelt, overspeeding and signal jumping.",

    "Consumer court helps consumers resolve disputes against defective products or poor services.",

    "Online fraud can be reported at cybercrime.gov.in or nearest cyber police station.",

    "Divorce laws in India depend on religion and personal laws under Indian legal system.",

    "Property disputes can be resolved through civil court or mutual settlement.",

    "Cyber bullying is harassment using internet platforms, social media or messaging apps.",

    "Helmet challan is issued if rider or passenger is not wearing helmet while driving.",

    "Police complaint can be filed at nearest police station or online grievance portal.",

    "Loan fraud includes fake loan apps, phishing links and illegal recovery threats.",

    "Domestic violence includes physical, emotional, verbal and financial abuse."
]

# =========================================================
# NLP MODEL
# =========================================================

vectorizer = TfidfVectorizer()

X = vectorizer.fit_transform(legal_questions)

# =========================================================
# STATES & CITIES
# =========================================================

states = [
    "uttar pradesh",
    "maharashtra",
    "delhi",
    "bihar",
    "gujarat",
    "rajasthan",
    "west bengal",
    "madhya pradesh",
    "tamil nadu",
    "karnataka"
]

cities = [
    "varanasi",
    "lucknow",
    "mumbai",
    "surat",
    "patna",
    "jaipur",
    "kolkata",
    "bhopal",
    "chennai",
    "bangalore",
    "delhi"
]

# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():
    return render_template("index.html")

# =========================================================
# CHATBOT ROUTE
# =========================================================

@app.route("/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json()

        user_message = data.get("message", "").lower()

        # =====================================================
        # REMOVE EMOJIS
        # =====================================================

        user_message = re.sub(r'[^\w\s]', '', user_message)

        # =====================================================
        # NLP RESPONSE
        # =====================================================

        user_vector = vectorizer.transform([user_message])

        similarity = cosine_similarity(user_vector, X)

        best_match = similarity.argmax()

        response = legal_answers[best_match]

        # =====================================================
        # LOCATION DETECTION
        # =====================================================

        detected_state = None
        detected_city = None

        for state in states:
            if state in user_message:
                detected_state = state.title()

        for city in cities:
            if city in user_message:
                detected_city = city.title()

        # =====================================================
        # FINAL RESPONSE
        # =====================================================

        return jsonify({
            "reply": response,
            "state": detected_state,
            "city": detected_city
        })

    except Exception as e:

        return jsonify({
            "reply": f"Error: {str(e)}"
        })

# =========================================================
# OCR ROUTE
# =========================================================

@app.route("/ocr", methods=["POST"])
def ocr():

    try:

        if "image" not in request.files:
            return jsonify({
                "text": "No image uploaded"
            })

        file = request.files["image"]

        if file.filename == "":
            return jsonify({
                "text": "No selected image"
            })

        filename = secure_filename(file.filename)

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        file.save(filepath)

        image = Image.open(filepath)

        extracted_text = pytesseract.image_to_string(image)

        return jsonify({
            "text": extracted_text
        })

    except Exception as e:

        return jsonify({
            "text": f"OCR Error: {str(e)}"
        })

# =========================================================
# RUN APP
# =========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )