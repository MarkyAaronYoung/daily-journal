from models.entries import Entries
import sqlite3
import json

def get_all_entries():
    with sqlite3.connect("./daily-journal.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.concept,
            a.entry,
            a.date,
            a.moodId
        FROM entries a
        """)

        entries = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            entry = Entries(row['id'], row['concept'], row['entry'], row['date'], row['moodId'])

            entries.append(entry.__dict__)
    
    return json.dumps(entries)
