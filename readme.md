#  JanSahayak AI+

**JanSahayak AI+** is an AI-powered citizen assistance platform that empowers Indian citizens to get intelligent support in reporting civic issues, predicting health risks, understanding legal documents, planning finances, and managing reports — all through a modular, Flask-based system.

---

## 🚀 Modules Overview

| # | Module | Description | Tech Stack |
|---|--------|-------------|------------|
| 1 | **Smart Issue Reporting** | Users report civic issues → AI classifies the complaint into predefined categories. | Flask · Hugging Face BART (text classification) |
| 2 | **Health Risk Predictor** | Predicts likely disease using an RNN model trained on medical data, with NLP-based keyword extraction from user input. | Flask · RNN · Medical Dataset · NLP |
| 3 | **LegalEase AI** | Users upload legal PDFs and ask legal questions about them via chat. | Flask · Gemini Flash API · PyMuPDF |
| 4 | **Admin Dashboard** | Admin interface to monitor, review, and manage all complaints and AI-generated predictions. | Flask · SQLite |
| 5 | **Financial Guide AI** | Generates a personalized monthly budget and savings roadmap using Gemini. | Flask · Gemini Flash API · markdown2 · Bootstrap |

---

## 🔧 Tech Stack

- **Backend**: Python · Flask
- **Frontend**: HTML · CSS · Bootstrap 5
- **AI Models**:
  - Hugging Face BART (for issue classification)
  - RNN (for disease prediction)
  - Gemini Flash (for legal & financial modules)
- **PDF Handling**: PyMuPDF (`fitz`)
- **NLP**: Simple keyword extraction for health module
- **Markdown Rendering**: `markdown2` for converting Gemini output

---

## 🧠 How It Works

### 🛠️ 1. Smart Issue Reporting
- User enters a civic complaint.
- Hugging Face BART model classifies it into categories (e.g., Sanitation, Road, Water Supply).
  
### ❤️ 2. Health Risk Predictor
- User enters a sentence describing symptoms or health concerns.
- NLP is used to extract keywords → passed to RNN model.
- Predicts most likely disease or health condition using deep learning(keras)

### 📄 3. LegalEase AI
- User uploads a legal PDF.
- They can ask legal questions (about the doc or general).
- Gemini Flash responds with AI-powered legal answers.

### 🧑‍💼 4. Admin Dashboard
- Admin can review all user inputs, predictions, and module usage.
- Flask-based dashboard with SQLite storage.

### 💰 5. Financial Guide AI
- User enters income, expenses, and a savings goal.
- Gemini Flash returns:
  - A financial health verdict
  - Personalized budget table
  - Savings goal feasibility
  - Actionable tips
- Markdown output rendered beautifully using `markdown2` + Bootstrap.

---

### 🎥 Demo Video

Watch a full walkthrough of JanSahayak AI+ in action:  
👉 [Click to Watch Demo](https://drive.google.com/file/d/1wMyKR4REDuy67GqMggpLKYSxFnZxnOX4/view?usp=sharing)

---

## 🧑‍💻 Developed By

**Atharva J** — Final Year CSE Student, PCE 
> 💡 Guided by a mission to blend AI with public benefit

---

## 📌 License

This project is for academic, research, and demo purposes only.

---

