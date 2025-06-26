from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import random
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sakhibot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    language = db.Column(db.String(20), default='hindi')
    expenses = db.relationship('Expense', backref='user', lazy=True)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class QuizQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    options = db.Column(db.String(500), nullable=False)  # JSON string of options
    correct_answer = db.Column(db.String(200), nullable=False)
    language = db.Column(db.String(20), default='english')

# Create tables
with app.app_context():
    db.create_all()

    QuizQuestion.query.delete()
    db.session.commit()
       
    questions = [
        # Basic Financial Concepts
         {
            'question': 'What is the first step in creating a budget?',
            'options': ['Track your expenses', 'Set financial goals', 'Cut all spending', 'Invest in stocks'],
            'correct_answer': 'Track your expenses',
            'language': 'english'
            },
            {
            'question': 'Which of these is a need rather than a want?',
            'options': ['Eating out at a restaurant', 'New clothes', 'Rent payment', 'Movie tickets'],
            'correct_answer': 'Rent payment',
            'language': 'english'
            },
            {
            'question': 'What does "saving" mean?',
            'options': ['Spending all your money', 'Keeping money for future use', 'Borrowing money', 'Giving money to others'],
            'correct_answer': 'Keeping money for future use',
            'language': 'english'
            },
           
            # Budgeting Questions
            {
            'question': 'How much of your income should you ideally save?',
            'options': ['5-10%', '20-30%', '50%', "Don't save at all"],
            'correct_answer': '20-30%',
            'language': 'english'
            },
            {
            'question': 'बजट बनाने का पहला कदम क्या है?',
            'options': ['अपने खर्चों को ट्रैक करें', 'वित्तीय लक्ष्य निर्धारित करें', 'सभी खर्चों में कटौती करें', 'स्टॉक में निवेश करें'],
            'correct_answer': 'अपने खर्चों को ट्रैक करें',
            'language': 'hindi'
            },
            {
            'question': 'आपातकालीन फंड में आपके पास कितना पैसा होना चाहिए?',
            'options': [
                '1-2 महीने का खर्च',
                '3-6 महीने का खर्च',
                '1 साल का खर्च',
                'आपातकालीन फंड की आवश्यकता नहीं है'
            ],
            'correct_answer': '3-6 महीने का खर्च',
            'language': 'hindi'
            },
               
            # Banking Questions
            {
            'question': 'What is the benefit of having a bank account?',
            'options': [
                'Keeps money safe',
                'Earns interest',
                'Makes transactions easier',
                'All of the above'
            ],
            'correct_answer': 'All of the above',
            'language': 'english'
            },
            {
            'question': 'What is a common feature of a savings account?',
            'options': [
                'High risk investments',
                'Earning interest on deposits',
                'Unlimited free withdrawals',
                'No need for identity proof'
            ],
            'correct_answer': 'Earning interest on deposits',
            'language': 'english'
           },
       
        # Emergency Funds
            {
            'question': 'How much should you ideally have in an emergency fund?',
            'options': [
                '1-2 months of expenses',
                '3-6 months of expenses',
                '1 year of expenses',
                "Don't need an emergency fund"
            ],
            'correct_answer': '3-6 months of expenses',
            'language': 'english'
          },
       
        # Women-Specific Financial Questions
          {
            'question': 'Why is financial independence important for women?',
            'options': [
                'For personal security',
                'To make own decisions',
                'To support family needs',
                'All of the above'
            ],
            'correct_answer': 'All of the above',
            'language': 'english'
        },
        {
            'question': 'What is a Self-Help Group (SHG) in microfinance?',
            'options': [
                'A group that provides free money',
                'A collective savings and loan group',
                'A government welfare scheme',
                'A private bank'
            ],
            'correct_answer': 'A collective savings and loan group',
            'language': 'english'
        },
       
        # Practical Money Management
        {
            'question': 'What is the best way to track daily expenses?',
            'options': [
                'Remember them in your head',
                'Write them down daily',
                'Only track big expenses',
                "Don't track expenses"
            ],
            'correct_answer': 'Write them down daily',
            'language': 'english'
        },
        {
            'question': 'What should you do before making a big purchase?',
            'options': [
                'Compare prices',
                'Check if you really need it',
                'See if it fits your budget',
                'All of the above'
            ],
            'correct_answer': 'All of the above',
            'language': 'english'
        }
    ]
   
   
    for q in questions:
        question = QuizQuestion(
            question=q['question'],
            options=str(q['options']),
            correct_answer=q['correct_answer'],
            language=q['language']
        )
        db.session.add(question)
    db.session.commit()




# Routes
@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            session['language'] = user.language
            return redirect(url_for('home'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            return render_template('register.html', error='Username already exists')
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        session['username'] = user.username
        session['language'] = user.language
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# API Endpoints
@app.route('/api/translate', methods=['POST'])
def translate():
    # In a real app, you would integrate with a translation API like Google Translate
    # For this demo, we'll just return placeholder translations
    data = request.json
    text = data.get('text', '')
    to_lang = data.get('to', 'hindi')
   
    # Simple placeholder translations
    translations = {
        'hello': 'नमस्ते',
        'how are you': 'आप कैसे हैं',
        'what is your name': 'आपका नाम क्या है',
        'budget': 'बजट',
        'expense': 'खर्च',
        'savings': 'बचत',
        'emergency': 'आपातकालीन',
        'help': 'मदद',
        'today\'s tip': 'आज की सलाह',
        'quiz': 'प्रश्नोत्तरी',
        'track expense': 'खर्च रिकॉर्ड करें'
    }
   
    translated = translations.get(text.lower(), f"[Translation: {text} to {to_lang}]")
    return jsonify({'translation': translated})

@app.route('/api/process_voice', methods=['POST'])
def process_voice():
    # In a real app, you would integrate with a speech-to-text API
    # For this demo, we'll simulate processing
    audio_file = request.files.get('audio')
    language = request.form.get('language', 'hindi')
   
    # Simulate processing
    if language == 'hindi':
        text = "यह एक हिंदी वॉयस इनपुट का सिमुलेशन है"
    else:
        text = "This is a simulation of an English voice input"
   
    return jsonify({'text': text, 'language': language})

hindi_tips = [
    "छोटी-छोटी बचत से बड़ा कोष बनता है - रोज़ के 10 रुपये भी साल के 3,650 रुपये बनते हैं!",
    "हर महीने आय का कम से कम 10% बचत के लिए अलग रखें।",
    "किसी भी दस्तावेज़ पर बिना पढ़े हस्ताक्षर या अंगूठा न लगाएं।",
    "अलग-अलग लक्ष्यों के लिए अलग बचत खाते बनाएं (जैसे शिक्षा, आपातकाल, त्योहार)",
    "रोज़ के खर्चों को डायरी में लिखें - यह आपको अनावश्यक खर्चों से बचाएगा।",
    "बड़ी खरीदारी से पहले कम से कम 24 घंटे सोचें।",
    "मौसमी फल-सब्ज़ियां खरीदें - यह सस्ती और ताज़ा होती हैं।",
    "जन धन योजना खाते में आप 10,000 रुपये तक का मुफ्त बीमा पा सकती हैं।",
    "बैंक स्टेटमेंट नियमित चेक करें - गलतियों को तुरंत ठीक करवाएं।",
    "UPI पिन किसी के साथ भी साझा न करें, यहां तक कि परिवार वालों के साथ भी नहीं।",
    "सुकन्या समृद्धि योजना में निवेश करके बेटी के भविष्य को सुरक्षित करें।",
    "महिला स्वयं सहायता समूह (SHG) में शामिल हों - सामूहिक बचत और ऋण के लाभ उठाएं।",
    "घर की छोटी-छोटी चीजें बेचकर (पुराने सामान, हस्तशिल्प) अतिरिक्त आय कमाएं।",
    "कम से कम 3-6 महीने के खर्च के बराबर आपातकालीन फंड जमा करें।",
    "घर में कुछ नकदी और जरूरी दस्तावेज हमेशा सुरक्षित जगह रखें।",
    "महिला हेल्पलाइन नंबर 1091 को अपने फोन में सेव करें।",
    "मोबाइल बैंकिंग ऐप पर टू-फैक्टर ऑथेंटिकेशन जरूर लगाएं।",
    "कभी भी लिंक पर क्लिक करके OTP शेयर न करें - बैंक ऐसा नहीं मांगते।","पब्लिक वाई-फाई पर बैंकिंग न करें - मोबाइल डेटा का उपयोग करें।"
]
english_tips = [
        "Always track your daily expenses, no matter how small.",
        "Try to save at least 10% of your income every month.",
        "Create separate savings for different goals like education, emergencies, etc.",
        "Compare prices before making big purchases.",
        "Avoid taking loans for things that lose value quickly.",
        "Start with small savings goals - even ₹50 daily adds up to ₹1500 monthly!",
        "Use government schemes like Sukanya Samriddhi Yojana for girls' education savings.",
        "Plan meals weekly to reduce food waste and grocery bills.",
        "Keep some emergency cash hidden at home in case digital payments aren't possible.",
        "Never sign blank documents or put thumbprints without understanding them.",
        "Invest in learning new skills - education gives the highest long-term returns.",
        "Join a women's Self-Help Group (SHG) to access microloans and collective savings.",
        "Follow the 24-hour rule: Wait a day before making unplanned purchases."
    ]

@app.route('/api/get_tip', methods=['GET'])
def get_tip():
    # Combine English and Hindi tips
    all_tips = english_tips + hindi_tips  # Make sure english_tips is defined
   
    # Or serve based on user's language preference
    #user_language = session.get('language', 'hindi')
    #tips = hindi_tips if user_language == 'hindi' else english_tips
   
    tip = random.choice(all_tips)
    return jsonify({'tip': tip})
   

@app.route('/api/get_quiz', methods=['GET'])
def get_quiz():
    try:
        # Get all questions from database
        all_questions = QuizQuestion.query.all()
       
        if not all_questions:
            return jsonify({'error': 'No questions available'}), 404
       
        # Select a random question
        question = random.choice(all_questions)
       
        return jsonify({
            'question': question.question,
            'options': eval(question.options),  # Convert string back to list
            'correct_answer': question.correct_answer,
            'language': question.language
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/debug/questions', methods=['GET'])
def debug_questions():
    questions = QuizQuestion.query.all()
    return jsonify({
        'count': len(questions),
        'questions': [{
            'id': q.id,
            'question': q.question,
            'language': q.language
        } for q in questions]
    })

@app.route('/api/add_expense', methods=['POST'])
def add_expense():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
   
    data = request.json
    try:
        expense = Expense(
            amount=float(data['amount']),
            category=data['category'],
            description=data.get('description', ''),
            user_id=session['user_id']
        )
        db.session.add(expense)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/get_expenses', methods=['GET'])
def get_expenses():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
   
    expenses = Expense.query.filter_by(user_id=session['user_id']).order_by(Expense.date.desc()).limit(10).all()
    return jsonify({
        'expenses': [{
            'amount': e.amount,
            'category': e.category,
            'description': e.description,
            'date': e.date.strftime('%Y-%m-%d')
        } for e in expenses]
    })

@app.route('/api/emergency', methods=['POST'])
def emergency():
    # In a real app, this would connect to emergency services or trusted contacts
    return jsonify({
        'message': 'Emergency alert sent to your trusted contacts',
        'contacts': ['Local Women\'s Helpline: 1091', 'Police: 100', 'Ambulance: 108']
    })

if __name__ == '__main__':
    app.run(debug=True)
