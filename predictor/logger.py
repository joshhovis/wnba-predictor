import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'db.sqlite')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Table for storing predictions
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        game_id TEXT,
        date TEXT,
        team_home TEXT,
        team_away TEXT,
        sportsbook TEXT,
        line REAL,
        predicted_total REAL,
        prediction TEXT,  -- 'Over' or 'Under'
        confidence REAL,
        injury_notes TEXT,
        placed INTEGER DEFAULT 0,
        result TEXT
    );
    """)

    # Table for caching team IDs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teams (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        short_name TEXT,
        logo_url TEXT,
        country TEXT
    );
    """)

    conn.commit()
    conn.close()
