import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import mysql.connector
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
import requests

load_dotenv()
app = Flask(__name__)
app.secret_key = 'secret_key'  # Change in production

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        database=os.getenv('DB_NAME')
    )

# Load model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Paystack payment processing
def initialize_paystack_payment(email, amount, reference):
    paystack_secret_key = os.getenv('PAYSTACK_SECRET_KEY')
    if not paystack_secret_key:
        return {"success": False, "message": "Paystack secret key not configured"}
    url = "https://api.paystack.co/transaction/initialize"
    headers = {"Authorization": f"Bearer {paystack_secret_key}", "Content-Type": "application/json"}
    payload = {
        "email": email,  # Use logged-in user's email from session or form
        "amount": int(amount * 100),  # Amount in kobo (NGN subunit), multiply by 100
        "reference": reference,  # Unique transaction reference
        "currency": "NGN"  # Default to NGN; adjust based on region
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"success": False, "message": f"Paystack initialization failed: {str(e)}"}

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', books=books)

# Other routes (login, register, post, recommend, message) remain unchanged

@app.route('/buy', methods=['POST'])
def buy():
    if 'user_id' not in session:
        return jsonify({"error": "Login required"}), 401
    data = request.json
    book_id = data.get('book_id')
    payment_method = data.get('payment_method', 'paystack')  # Default to Paystack

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT price, owner_id FROM books WHERE id = %s", (book_id,))
    book = cursor.fetchone()
    cursor.close()
    conn.close()

    if not book or session['user_id'] == book['owner_id']:  # Prevent self-buy
        return jsonify({"error": "Invalid book or self-purchase"}), 400
    amount = book['price'] * 1.05  # 5% fee
    reference = f"ref_{book_id}_{session['user_id']}_{int(time.time())}"  # Unique reference

    # Get user email (simplified; use real email from users table in production)
    user_email = "user@example.com"  # Replace with session/email lookup

    # Initialize Paystack payment
    payment_response = initialize_paystack_payment(user_email, amount, reference)
    if payment_response.get('status') and payment_response.get('data', {}).get('authorization_url'):
        return jsonify({
            "message": "Redirecting to Paystack for payment",
            "authorization_url": payment_response['data']['authorization_url'],
            "reference": reference
        })
    else:
        return jsonify({"error": payment_response.get('message', "Payment initialization failed")})

if __name__ == '__main__':
    import time  # Added for reference timestamp
    app.run(debug=True)
