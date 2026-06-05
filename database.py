import sqlite3
from datetime import datetime

DB_PATH = "quotes.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the quotes table if it doesn't exist."""
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS quotes (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            text     TEXT    NOT NULL,
            author   TEXT    NOT NULL,
            category TEXT    NOT NULL,
            liked    INTEGER NOT NULL DEFAULT 0,
            saved_at TEXT    NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_quote(text: str, author: str, category: str) -> int:
    """Insert a new quote and return its id."""
    conn = get_connection()
    cur = conn.execute(
        "INSERT INTO quotes (text, author, category, liked, saved_at) VALUES (?, ?, ?, 0, ?)",
        (text, author, category, datetime.now().isoformat())
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def get_all_quotes() -> list[dict]:
    """Return all quotes ordered by newest first."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM quotes ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def delete_quote(quote_id: int):
    """Delete a quote by id."""
    conn = get_connection()
    conn.execute("DELETE FROM quotes WHERE id = ?", (quote_id,))
    conn.commit()
    conn.close()


def toggle_like(quote_id: int, liked: bool):
    """Set the liked status for a quote."""
    conn = get_connection()
    conn.execute(
        "UPDATE quotes SET liked = ? WHERE id = ?",
        (1 if liked else 0, quote_id)
    )
    conn.commit()
    conn.close()


def clear_all_quotes():
    """Delete all quotes from the database."""
    conn = get_connection()
    conn.execute("DELETE FROM quotes")
    conn.commit()
    conn.close()
