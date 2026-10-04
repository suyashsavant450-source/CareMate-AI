# CareMate AI 🩺

**AI-Powered Medical Report Simplifier & Personal Health Companion**

CareMate AI is a smart healthcare assistance application designed to help users understand their medical reports in simple language and manage their daily health routines from one platform.

## 🚀 Features

* 🔐 User Registration & Secure Login
* 📄 Medical Report Upload
* 🔍 OCR-based Text Extraction
* 🤖 AI-powered Medical Report Analysis
* 📋 Patient-friendly Report Simplification
* ⚠️ Abnormal Values Detection
* 💊 Medicine & Tablet Reminders
* ⏰ Health Routine Reminders
* 💧 Water Intake Tracking
* 😴 Sleep Reminders
* 🏃 Exercise Reminders
* 🥗 Personalized Diet Guidance
* 💬 AI Health Assistant
* 👨‍👩‍👧 Caregiver Mode
* 📈 Health Progress Tracking
* 📑 Medical Report PDF Generation
* 🔊 Text-to-Speech Support
* 📱 SMS Reminder Support

## 🏗️ System Architecture

```text
User
  ↓
Registration / Login
  ↓
CareMate AI Dashboard
  ↓
┌─────────────────────────────────────┐
│                                     │
│  Medical Report Upload              │
│          ↓                          │
│  OCR + AI Text Extraction           │
│          ↓                          │
│  AI Medical Analysis                │
│          ↓                          │
│  Simplified Report                  │
│          ↓                          │
│  Abnormal Values Detection          │
│                                     │
└─────────────────────────────────────┘

          ↓

Personal Health Management
  ├── Medicine Reminders
  ├── Diet Guidance
  ├── Water Tracking
  ├── Sleep Reminders
  ├── Exercise Reminders
  ├── Health Routine
  └── Health Progress

          ↓

AI Health Assistant
          +
Caregiver Mode
```

## 🛠️ Technologies Used

### Frontend

* Streamlit
* HTML
* CSS

### Backend

* Python
* SQLite

### Artificial Intelligence

* Groq API
* AI-based medical text analysis
* AI-powered health assistance

### Document & OCR Processing

* PDF Processing
* OCR
* Medical report text extraction

### Additional Tools

* Text-to-Speech
* SMS Notification
* PDF Generation
* Python-dotenv

## 📁 Project Structure

```text
CareMate_AI/
│
├── app.py
├── database.py
├── requirements.txt
├── .gitignore
│
├── ai/
│   ├── analyzer.py
│   └── prompts.py
│
├── ocr/
│   └── extractor.py
│
├── pages/
│   ├── login.py
│   ├── register.py
│   ├── dashboard.py
│   ├── upload_report.py
│   ├── caremate.py
│   ├── medicines.py
│   ├── reminders.py
│   ├── caregiver.py
│   ├── progress.py
│   ├── profile.py
│   └── forgot_password.py
│
├── utils/
│   ├── helpers.py
│   ├── navigation.py
│   ├── pdf_generator.py
│   ├── theme.py
│   └── tts.py
│
└── data/
```

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/suyashsavant450-source/CareMate-AI.git
```

Go to the project directory:

```bash
cd CareMate-AI
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 🔑 Environment Variables

Create a `.env` file in the project root and add your own API credentials.

Example:

```env
GROQ_API_KEY=your_api_key_here
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_twilio_number
```

**Never upload your `.env` file or API keys to GitHub.**

## ▶️ Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at:

```text
http://localhost:8501
```

## 🔐 Privacy & Security

CareMate AI is designed with user-specific data separation.

* Each user has a separate account.
* Health data is associated with the respective user account.
* Medical reports are stored according to the user.
* API keys are stored locally using environment variables.
* Sensitive credentials are excluded from GitHub.

## 🎯 Project Objective

The main objective of CareMate AI is to make medical information easier to understand and provide users with a single platform for managing important daily health activities.

> **CareMate AI — Understand Your Health. Manage Your Care.**

## ⚠️ Disclaimer

CareMate AI is an academic/project-based healthcare assistance system. It is intended to help users understand health information and manage routines. It does not replace professional medical advice, diagnosis, or treatment from a qualified healthcare professional.

## 👨‍💻 Developer

**Suyash Mahesh Savant**

B.E. Computer Science & Engineering

GitHub: [suyashsavant450-source](https://github.com/suyashsavant450-source)
