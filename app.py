from flask import Flask, render_template, request, redirect, url_for,jsonify
import sqlite3
from transformers import pipeline
from db import init_db
import markdown2
# ===== Disease Predictor Setup =====
from keras.models import load_model
import joblib
import numpy as np
import google.generativeai as genai
import os
from dotenv import load_dotenv
import fitz  # PyMuPDF
from flask import send_file
import csv
import io

# Initialize DB
init_db()

# Flask app
app = Flask(__name__)
# ===== issue categoriser Setup =====
# Load model once
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", framework="pt")
labels = ["Road Issue", "Water Supply", "Electricity", "Sanitation", "Healthcare", "Safety", "Others"]

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/report-issue')
def report_issue():
    return render_template("report_issue.html")

@app.route('/submit', methods=['POST'])
def submit_complaint():
    name = request.form['name']
    email = request.form['email']
    complaint = request.form['complaint']
    location = request.form['location']

    result = classifier(complaint, candidate_labels=labels)
    category = result['labels'][0]

    conn = sqlite3.connect('complaints.db')
    c = conn.cursor()
    c.execute('INSERT INTO complaints (name, email, complaint, category, location) VALUES (?, ?, ?, ?, ?)',
              (name, email, complaint, category, location))
    conn.commit()
    conn.close()

    return render_template("thanks.html", category=category)


# ===== legal ease ai Setup =====

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)



# PDF to text
def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Gemini legal answer generator
def generate_legal_answer(user_msg, pdf_text=""):
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    chat = model.start_chat()

    if pdf_text.strip():
        prompt = f"""
You are LegalEase AI, a helpful legal assistant.
The user has uploaded a legal document. Use this to answer their question.

Document Content:
\"\"\"{pdf_text}\"\"\"

User Question:
{user_msg}
"""
    else:
        prompt = f"""
You are LegalEase AI, a helpful legal assistant. Answer the following legal question clearly, in plain English, based on Indian legal context if relevant and try to be short:

Question: {user_msg}
"""
    response = chat.send_message(prompt)
    return response.text.strip()

# Routes
@app.route('/legal-chat')
def legal_chat():
    return render_template("legal_chat.html")

@app.route('/ask-legal', methods=["POST"])
def ask_legal():
    user_msg = request.form.get("message", "").strip()
    pdf_file = request.files.get("pdf")
    print("user_msg:", repr(user_msg))  # Shows if it's blank or not

    if not user_msg:
        return jsonify({"response": "⚠️ Please type your legal question."})

    pdf_text = ""
    if pdf_file and pdf_file.filename.endswith(".pdf"):
        try:
            pdf_text = extract_text_from_pdf(pdf_file)
        except Exception as e:
            print("PDF error:", e)
            return jsonify({"response": "❌ Error reading PDF."})
    try:
            markdown_text = generate_legal_answer(user_msg, pdf_text)   # <-- get raw Markdown
            html_answer  = markdown2.markdown(markdown_text, extras=["tables"])
            return jsonify({"response": html_answer})                   # <-- send HTML back
    except Exception as e:
            print("Gemini error:", e)
            return jsonify({"response": "❌ Gemini API Error. Try again later."})
    

# ===== volunteers panel Setup =====

@app.route('/admin')
def admin_dashboard():
    conn = sqlite3.connect('complaints.db')
    c = conn.cursor()
    c.execute("SELECT id, name, email, complaint, category, location, date, status FROM complaints ORDER BY date DESC")
    data = c.fetchall()
    conn.close()
    return render_template("admin.html", complaints=data)

@app.route('/update_status/<int:complaint_id>', methods=["POST"])
def update_status(complaint_id):
    new_status = request.form["status"]
    conn = sqlite3.connect("complaints.db")
    c = conn.cursor()
    c.execute("UPDATE complaints SET status=? WHERE id=?", (new_status, complaint_id))
    conn.commit()
    conn.close()
    return redirect(url_for("admin_dashboard"))

@app.route('/delete/<int:complaint_id>', methods=["POST"])
def delete_complaint(complaint_id):
    conn = sqlite3.connect('complaints.db')
    c = conn.cursor()
    c.execute("DELETE FROM complaints WHERE id=?", (complaint_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("admin_dashboard"))


@app.route('/download_csv')
def download_csv():
    conn = sqlite3.connect('complaints.db')
    c = conn.cursor()
    c.execute("SELECT id, name, email, complaint, category, location, date, status FROM complaints")
    rows = c.fetchall()
    conn.close()

    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Name', 'Email', 'Complaint', 'Category', 'Location', 'Date', 'Status'])  # header
    writer.writerows(rows)
    output.seek(0)

    return send_file(
        io.BytesIO(output.read().encode('utf-8')),
        mimetype='text/csv',
        download_name='complaints_data.csv',
        as_attachment=True
    )

# ===== Disease Predictor Setup =====


# Load disease model and files only once
disease_model = load_model("disease_model.keras")
disease_symptoms = joblib.load("selected_symptoms.pkl")
disease_labels = joblib.load("disease_labels.pkl")

def extract_disease_symptoms(text):
    text = text.lower()
    matched = [sym for sym in disease_symptoms if sym.replace("_", " ") in text]
    return matched

@app.route('/disease-predictor')
def disease_input():
    return render_template("disease_predictor.html")

@app.route('/predict-disease', methods=['POST'])
def predict_disease():
    user_text = request.form['user_input']
    matched_symptoms = extract_disease_symptoms(user_text)

    input_vector = [1 if sym in matched_symptoms else 0 for sym in disease_symptoms]
    prediction = disease_model.predict(np.array([input_vector]))[0]
    predicted_disease = disease_labels[np.argmax(prediction)]

    return render_template("disease_predictor.html",
                           result=predicted_disease,
                           user_input=user_text,
                           matched=matched_symptoms)


# =====Budget Planner Setup =====

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
fin_model = genai.GenerativeModel("gemini-1.5-flash-latest")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/budget", methods=["GET", "POST"])
def budget():
    if request.method == "POST":
        income = request.form.get("income", "0")
        expenses = request.form.get("expenses", "0")
        debt = request.form.get("debt", "0")
        goal = request.form.get("goal", "")
        months = request.form.get("months", "0")

        prompt = f"""
You are a personal finance coach for Indian citizens.

User details:
- Monthly income: ₹{income}
- Monthly expenses: ₹{expenses}
- Monthly debt/EMI: ₹{debt}
- Goal: "{goal}" in {months} months

Return the following:
1. **Financial health verdict**
2. **Recommended Monthly Budget Table (₹)** with realistic categories
3. **Monthly savings needed** to reach the goal and whether it's realistic
4. **3-5 actionable tips** to stay on track

Use clear language and Markdown formatting (bold text, tables, bullet points).
        """

        try:
            gemini_response = fin_model.generate_content(prompt)
            markdown_text = gemini_response.text
            html_answer = markdown2.markdown(markdown_text, extras=["tables"])  # ✅ Convert + render tables
        except Exception as e:
            print("Gemini error:", e)
            html_answer = "<p>Sorry, Gemini AI is currently unavailable.</p>"

        return render_template("budget_result.html", ai_answer=html_answer)

    return render_template("budget_form.html")


if __name__ == "__main__":
    app.run(debug=True)