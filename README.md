# SakhiBot
🌸 SakhiBot – AI Voice Assistant for Women’s Financial Literacy & Budgeting
SakhiBot is a voice-enabled, Hindi/English conversational assistant designed to help women improve their financial literacy, track expenses, and access emergency support. Built with a simple and intuitive interface, this tool is tailored for first-time tech users, especially in underprivileged or rural contexts.

# Features
- 💬 Conversational Chatbot (English - text, Hindi - simulated voice)
- 🎤 Voice Input Support (simulated, extendable with APIs)
- 🧠 Financial Literacy Quiz (in both English and Hindi)
- 💡 Daily Financial Tips (randomized, language-sensitive)
- 📊 Expense Tracker (add/view recent expenses with category and description)
- 🚨 Emergency Help Button (trusted helpline contact display)

## 🧩 Tech Stack
- Backend: Python, Flask, SQLAlchemy
- Frontend: HTML, CSS (Bootstrap), JavaScript
- Database: SQLite
- Voice & Translation APIs: Simulated (extensible to real APIs like Google Speech, Microsoft Translator)

## 🔧 Setup Instructions

### 1. Create and Activate Virtual Environment (Optional but Recommended)
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# 2. Install Dependencies
pip install -r requirements.txt

# 4. Run the Flask App
python app.py

Visit `http://localhost:5000` in your browser.

# 📁 Project Structure
sakhibot/
├── app.py                  # Flask backend
├── templates/              # HTML templates
│   ├── index.html          # Main interface
│   ├── login.html          # Login page
│   └── register.html       # Registration page
├── static/                 # Static files
│   ├── css/
│   │   └── style.css       # Custom styles
│   ├── js/
│   │   └── script.js       # Frontend functionality
│   └── images/             # Any images/icons
└── requirements.txt        # Python dependencies

# 🚀 Future Enhancements

- Real-time Speech-to-Text and Text-to-Speech Integration
- Google Translate API for accurate multilingual translation
- SMS-based access for non-smartphone users
- Secure user authentication (password hashing, OAuth)
- Offline mode for low-connectivity regions
- Integration with local SHGs and financial services







