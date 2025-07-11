"""
###Это приложение которое работает через браузер
from flask import Flask, request, jsonify, render_template, redirect, url_for
import sqlite3
from datetime import datetime
#import os

app = Flask(__name__)
DB_NAME = 'reviews.db'

# --- Инициализация БД ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            sentiment TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# --- Простая функция анализа тональности ---
def analyze_sentiment(text):
    text_lower = text.lower()
    positive_words = ['хорош', 'люблю', 'супер']
    negative_words = ['плохо', 'ненавиж', 'ужасно']
    if any(word in text_lower for word in positive_words):
        return 'positive'
    elif any(word in text_lower for word in negative_words):
        return 'negative'
    else:
        return 'neutral'

# --- Главная страница с HTML ---
@app.route('/')
def index():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, text, sentiment, created_at FROM reviews ORDER BY created_at DESC')
    reviews = cursor.fetchall()
    conn.close()
    return render_template('index.html', reviews=reviews)

# --- Обработка формы POST ---
@app.route('/submit', methods=['POST'])
def submit_review():
    text = request.form.get('text')
    if not text:
        return redirect(url_for('index'))

    sentiment = analyze_sentiment(text)
    created_at = datetime.utcnow().isoformat()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO reviews (text, sentiment, created_at) VALUES (?, ?, ?)',
        (text, sentiment, created_at)
    )
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)"""

from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_NAME = 'reviews.db'

# --- Инициализация БД ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            sentiment TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# --- Простая функция анализа тональности ---
def analyze_sentiment(text):
    text_lower = text.lower()
    positive_words = ['хорош', 'люблю', 'отлич']
    negative_words = ['плохо', 'ненавиж', 'ужас']

    if any(word in text_lower for word in positive_words):
        return 'positive'
    elif any(word in text_lower for word in negative_words):
        return 'negative'
    else:
        return 'neutral'

# --- POST /reviews ---
@app.route('/reviews', methods=['POST'])
def add_review():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Missing "text" in request'}), 400

    text = data['text']
    sentiment = analyze_sentiment(text)
    created_at = datetime.utcnow().isoformat()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO reviews (text, sentiment, created_at) VALUES (?, ?, ?)',
        (text, sentiment, created_at)
    )
    review_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return jsonify({
        'id': review_id,
        'text': text,
        'sentiment': sentiment,
        'created_at': created_at
    }), 201

# --- GET /reviews ---
@app.route('/reviews', methods=['GET'])
def get_reviews():
    sentiment = request.args.get('sentiment')
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    if sentiment:
        cursor.execute(
            'SELECT id, text, sentiment, created_at FROM reviews WHERE sentiment = ?',
            (sentiment,)
        )
    else:
        cursor.execute('SELECT id, text, sentiment, created_at FROM reviews')

    rows = cursor.fetchall()
    conn.close()

    result = []
    for row in rows:
        result.append({
            'id': row[0],
            'text': row[1],
            'sentiment': row[2],
            'created_at': row[3]
        })

    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)
