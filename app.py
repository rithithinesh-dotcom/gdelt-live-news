import os
import sqlite3
import datetime
from flask import Flask, render_template, request, jsonify, Response, redirect, url_for, send_file

from news_collector import fetch_gdelt_news
from sentiment_analysis import analyze_sentiment
from trend_analysis import (
    DEFAULT_CATEGORIES_STATS,
    get_mentions_over_time,
    get_sentiment_overview_stats,
    get_word_cloud_keywords
)
from export_utils import generate_csv_report, generate_excel_report, generate_pdf_report
from make_zip import create_project_zip

app = Flask(__name__)

DB_DIR = os.path.join(app.root_path, 'data')
DB_PATH = os.path.join(DB_DIR, 'news.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            headline TEXT NOT NULL,
            snippet TEXT,
            source TEXT,
            category TEXT,
            url TEXT,
            image_url TEXT,
            pub_date TEXT,
            sentiment_label TEXT,
            polarity REAL,
            subjectivity REAL,
            trend_score REAL,
            is_bookmarked INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY DEFAULT 1,
            dark_mode INTEGER DEFAULT 1,
            refresh_interval INTEGER DEFAULT 60,
            theme_color TEXT DEFAULT 'purple',
            sources_enabled TEXT DEFAULT 'all',
            api_key TEXT DEFAULT ''
        )
    ''')

    cursor.execute('SELECT COUNT(*) FROM settings')
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO settings (id, dark_mode, refresh_interval) VALUES (1, 1, 60)')

    cursor.execute('SELECT COUNT(*) FROM articles')
    if cursor.fetchone()[0] == 0:
        seed_news = fetch_gdelt_news()
        for item in seed_news:
            cursor.execute('''
                INSERT INTO articles (headline, snippet, source, category, url, image_url, pub_date, sentiment_label, polarity, subjectivity, trend_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                item['headline'], item['snippet'], item['source'], item['category'],
                item['url'], item['image_url'], item['pub_date'], item['sentiment_label'],
                item['polarity'], item['subjectivity'], item['trend_score']
            ))

    cursor.execute("UPDATE articles SET url = 'https://techcrunch.com' WHERE url = '#' OR url IS NULL OR url = ''")
    conn.commit()
    conn.close()

def fetch_articles_from_db(query=None, category=None, sentiment=None, sort_by='newest', limit=100, bookmarked_only=False):
    conn = get_db()
    cursor = conn.cursor()
    sql = "SELECT * FROM articles WHERE 1=1"
    params = []

    if query:
        sql += " AND (headline LIKE ? OR snippet LIKE ? OR source LIKE ?)"
        pattern = f"%{query}%"
        params.extend([pattern, pattern, pattern])

    if category and category != 'All':
        sql += " AND category = ?"
        params.append(category)

    if sentiment and sentiment != 'All':
        sql += " AND sentiment_label = ?"
        params.append(sentiment)

    if bookmarked_only:
        sql += " AND is_bookmarked = 1"

    if sort_by == 'trending':
        sql += " ORDER BY trend_score DESC, pub_date DESC"
    elif sort_by == 'positive':
        sql += " ORDER BY polarity DESC"
    elif sort_by == 'negative':
        sql += " ORDER BY polarity ASC"
    else:
        sql += " ORDER BY pub_date DESC, id DESC"

    if limit:
        sql += " LIMIT ?"
        params.append(limit)

    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.route('/')
@app.route('/dashboard')
def dashboard():
    articles = fetch_articles_from_db(limit=10)
    sentiment_stats = get_sentiment_overview_stats(articles)
    last_updated = datetime.datetime.now().strftime("%b %d, %Y • %I:%M %p")
    return render_template('dashboard.html', articles=articles, categories=DEFAULT_CATEGORIES_STATS, sentiment_stats=sentiment_stats, last_updated=last_updated, active_page='dashboard')

@app.route('/collected')
@app.route('/articles')
def collected():
    category = request.args.get('category', 'All')
    sentiment = request.args.get('sentiment', 'All')
    articles = fetch_articles_from_db(category=category, sentiment=sentiment, limit=100)
    return render_template('collected.html', articles=articles, category=category, sentiment=sentiment, total_count=len(articles), active_page='collected')

@app.route('/download-project-zip')
def download_project_zip():
    zip_path = create_project_zip()
    return send_file(zip_path, as_attachment=True, download_name='TrendWatch_Project.zip')

if __name__ == '__main__':
    import sys
    init_db()
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5050
    try:
        app.run(host='0.0.0.0', port=port, debug=False)
    except OSError:
        app.run(host='0.0.0.0', port=5055, debug=False)
