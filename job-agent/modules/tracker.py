import sqlite3
import json

DB_PATH = "applications.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT,
            title TEXT,
            url TEXT,
            match_score INTEGER,
            match_reason TEXT,
            missing_skills TEXT,
            cover_letter TEXT,
            tailored_bullets TEXT,
            status TEXT DEFAULT 'pending',
            applied_date TEXT DEFAULT (date('now'))
        )
    """)
    conn.commit()
    conn.close()
    print("Database ready")

def save_application(job, match_result, content_result):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        INSERT INTO applications 
        (company, title, url, match_score, match_reason, 
         missing_skills, cover_letter, tailored_bullets)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        job["company"],
        job["title"],
        job["url"],
        match_result["match_score"],
        match_result["match_reason"],
        json.dumps(match_result["missing_skills"]),
        content_result["cover_letter"],
        json.dumps(content_result["tailored_bullets"])
    ))
    conn.commit()
    conn.close()

def get_all_applications():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("""
        SELECT id, company, title, match_score, status, applied_date 
        FROM applications 
        ORDER BY match_score DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


