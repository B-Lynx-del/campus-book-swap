from flask import Flask, render_template, request, jsonify
import mysql.connector
from transformers import pipeline
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# MySQL connection
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        database=os.getenv('DB_NAME')
    )

# Hugging Face AI pipeline (question generation)
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    text = request.json['text']
    # Sample prompt engineering: Generate questions from text
    # In README: Prompt used - "Extract questions from: [text]"
    questions = []  # Simulate 5 questions (use AI to generate)
    for i in range(5):
        result = qa_pipeline(question=f"What is key point {i+1}?", context=text)
        questions.append({"question": f"Question {i+1} from text", "answer": result['answer']})
    
    # Save to DB (basic, for demo)
    conn = get_db_connection()
    cursor = conn.cursor()
    for q in questions:
        cursor.execute("INSERT INTO flashcards (question, answer) VALUES (%s, %s)", (q['question'], q['answer']))
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify(questions)

@app.route('/buy', methods=['POST'])
def buy():
    # Simulate InterSed payment
    book_id = request.json['book_id']
    # In real: Call InterSed API with os.getenv('INTERSED_API_KEY')
    return jsonify({"message": "Purchase processed via InterSed (5% fee applied)!"})

if __name__ == '__main__':
    app.run(debug=True)
