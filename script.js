document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const chatContainer = document.getElementById('chat-container');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-text');
    const startRecordingButton = document.getElementById('start-recording');
    const stopRecordingButton = document.getElementById('stop-recording');
    const dailyTipButton = document.getElementById('daily-tip');
    const takeQuizButton = document.getElementById('take-quiz');
    const emergencyButton = document.getElementById('emergency-btn');
    const expenseForm = document.getElementById('expense-form');
   
    // Initial welcome message
    addBotMessage("नमस्ते! मैं सखीबोट हूँ, आपकी वित्तीय सहायक। मैं आपको बजट बनाने, खर्चों को ट्रैक करने और वित्तीय साक्षरता सीखने में मदद कर सकती हूँ। आज मैं आपकी क्या मदद कर सकती हूँ?");
   
    // Load recent expenses
    loadExpenses();
   
    // Event Listeners
    sendButton.addEventListener('click', sendTextMessage);
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') sendTextMessage();
    });
   
    startRecordingButton.addEventListener('click', startRecording);
    stopRecordingButton.addEventListener('click', stopRecording);
   
    dailyTipButton.addEventListener('click', getDailyTip);
    takeQuizButton.addEventListener('click', startQuiz);
    emergencyButton.addEventListener('click', emergencyHelp);
   
    expenseForm.addEventListener('submit', addExpense);
   
    // Functions
    function addBotMessage(text) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', 'bot-message');
        messageDiv.textContent = text;
        chatContainer.appendChild(messageDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
   
    function addUserMessage(text) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', 'user-message');
        messageDiv.textContent = text;
        chatContainer.appendChild(messageDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
   
    function sendTextMessage() {
        const text = userInput.value.trim();
        if (text) {
            addUserMessage(text);
            userInput.value = '';
           
            // Simulate bot response (in a real app, this would call your backend)
            setTimeout(() => {
                // For demo purposes, respond based on some keywords
                if (text.toLowerCase().includes('hello') || text.toLowerCase().includes('hi') || text.toLowerCase().includes('नमस्ते')) {
                    addBotMessage("नमस्ते! आज मैं आपकी कैसे मदद कर सकती हूँ?");
                } else if (text.toLowerCase().includes('budget') || text.toLowerCase().includes('बजट')) {
                    addBotMessage("बजट बनाना एक अच्छी वित्तीय आदत है। आप अपने मासिक आय और खर्चों को लिखकर शुरुआत कर सकती हैं।");
                } else if (text.toLowerCase().includes('expense') || text.toLowerCase().includes('खर्च')) {
                    addBotMessage("आप नीचे दिए गए फॉर्म का उपयोग करके अपने खर्चों को रिकॉर्ड कर सकती हैं।");
                } else if (text.toLowerCase().includes('help') || text.toLowerCase().includes('मदद')) {
                    addBotMessage("मैं आपकी निम्नलिखित तरीकों से मदद कर सकती हूँ: 1) दैनिक वित्तीय सलाह 2) प्रश्नोत्तरी 3) खर्च ट्रैकिंग 4) आपातकालीन सहायता");
                } else {
                    addBotMessage("मैं आपके संदेश को समझ नहीं पाई। कृपया कोई अन्य प्रश्न पूछें या नीचे दिए गए बटनों का उपयोग करें।");
                }
            }, 1000);
        }
    }
   
    function startRecording() {
        // In a real app, this would use the Web Speech API
        addUserMessage("[Hindi voice message]");
        startRecordingButton.disabled = true;
        stopRecordingButton.disabled = false;
       
        // Simulate recording for 3 seconds
        setTimeout(() => {
            stopRecording();
        }, 3000);
    }
   
    function stopRecording() {
        startRecordingButton.disabled = false;
        stopRecordingButton.disabled = true;
       
        // Simulate processing the voice message
        setTimeout(() => {
            addBotMessage("मैंने आपका वॉयस मैसेज प्राप्त कर लिया है। आपने कहा: 'मैं अपने खर्चों को कैसे ट्रैक कर सकती हूँ?'");
           
            // Provide response to the simulated query
            setTimeout(() => {
                addBotMessage("आप नीचे दिए गए खर्च ट्रैकर का उपयोग करके अपने दैनिक खर्चों को रिकॉर्ड कर सकती हैं। प्रत्येक खर्च के लिए राशि, श्रेणी और विवरण दर्ज करें।");
            }, 1000);
        }, 1000);
    }
   
    function getDailyTip() {
        fetch('/api/get_tip')
            .then(response => response.json())
            .then(data => {
                addBotMessage(`आज की सलाह: ${data.tip}`);
            })
            .catch(error => {
                console.error('Error:', error);
                addBotMessage("माफ कीजिए, मैं अभी सलाह प्राप्त नहीं कर पाई। बाद में पुनः प्रयास करें।");
            });
    }
   
    function startQuiz() {
        fetch('/api/get_quiz')
            .then(response => response.json())
            .then(data => {
                addBotMessage(`प्रश्न: ${data.question}`);
               
                // Display options
                const optionsDiv = document.createElement('div');
                optionsDiv.classList.add('quiz-options');
               
                data.options.forEach(option => {
                    const optionBtn = document.createElement('button');
                    optionBtn.classList.add('quiz-option', 'btn', 'btn-outline-secondary', 'w-100', 'mb-2');
                    optionBtn.textContent = option;
                    optionBtn.addEventListener('click', function() {
                        checkAnswer(option, data.correct_answer);
                    });
                    optionsDiv.appendChild(optionBtn);
                });
               
                chatContainer.appendChild(optionsDiv);
                chatContainer.scrollTop = chatContainer.scrollHeight;
            })
            .catch(error => {
                console.error('Error:', error);
                addBotMessage("माफ कीजिए, मैं प्रश्नोत्तरी लोड नहीं कर पाई। बाद में पुनः प्रयास करें।");
            });
    }
   
    function checkAnswer(selected, correct) {
        const options = document.querySelectorAll('.quiz-option');
        options.forEach(option => {
            option.disabled = true;
            if (option.textContent === correct) {
                option.classList.add('correct');
            } else if (option.textContent === selected && selected !== correct) {
                option.classList.add('incorrect');
            }
        });
       
        if (selected === correct) {
            addBotMessage("बिल्कुल सही! आपको यह अच्छी तरह से पता है।");
        } else {
            addBotMessage(`गलत उत्तर। सही उत्तर है: ${correct}`);
        }
    }
   
    function emergencyHelp() {
        if (confirm("क्या आप वास्तव में आपातकालीन सहायता चाहती हैं?")) {
            fetch('/api/emergency', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    addBotMessage(`आपातकालीन सहायता: ${data.message}\nसंपर्क: ${data.contacts.join(', ')}`);
                })
                .catch(error => {
                    console.error('Error:', error);
                    addBotMessage("माफ कीजिए, मैं आपातकालीन सहायता नहीं भेज पाई। कृपया सीधे संपर्क करें: स्थानीय महिला हेल्पलाइन: 1091");
                });
        }
    }
   
    function addExpense(e) {
        e.preventDefault();
       
        const amount = document.getElementById('expense-amount').value;
        const category = document.getElementById('expense-category').value;
        const description = document.getElementById('expense-description').value;
       
        fetch('/api/add_expense', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                amount: parseFloat(amount),
                category: category,
                description: description
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("खर्च सफलतापूर्वक जोड़ा गया!");
                loadExpenses();
                document.getElementById('expense-form').reset();
            } else {
                alert("खर्च जोड़ने में त्रुटि: " + (data.error || 'अज्ञात त्रुटि'));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("खर्च जोड़ने में त्रुटि हो गई");
        });
    }
   
    function loadExpenses() {
        fetch('/api/get_expenses')
            .then(response => response.json())
            .then(data => {
                const expensesList = document.getElementById('expenses');
                expensesList.innerHTML = '';
               
                if (data.expenses && data.expenses.length > 0) {
                    data.expenses.forEach(expense => {
                        const li = document.createElement('li');
                        li.classList.add('list-group-item', 'expense-item');
                        li.innerHTML = `
                            <span class="expense-category">${expense.category}</span>
                            <span class="expense-description">${expense.description || ''}</span>
                            <span class="expense-amount">₹${expense.amount.toFixed(2)}</span>
                        `;
                        expensesList.appendChild(li);
                    });
                } else {
                    const li = document.createElement('li');
                    li.classList.add('list-group-item');
                    li.textContent = 'कोई खर्च दर्ज नहीं किया गया है';
                    expensesList.appendChild(li);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                const expensesList = document.getElementById('expenses');
                expensesList.innerHTML = '<li class="list-group-item">खर्च लोड करने में त्रुटि</li>';
            });
    }
});

