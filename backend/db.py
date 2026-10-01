import sqlite3
import os

DB_NAME = os.path.join(os.path.dirname(__file__), "additives.db")

def get_additive(code):
    """
    Retrieves an additive by its INS code from the SQLite database.
    Returns a dictionary of column-value pairs if found, or None.
    """
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            """
            SELECT id, code, ins_number, additive_name, category, description, risk_score, high_risk_flag, risk_score_reason
            FROM additives
            WHERE code = ?
            """,
            (str(code),)
        )
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        conn.close()