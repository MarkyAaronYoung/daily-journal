from models.entries import Entries
from models.moods import Moods
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
            a.moodId,
            m.label label_mood
        FROM entries a
        JOIN moods m
            ON m.id = a.moodId
        """)

        entries = []

        dataset = db_cursor.fetchall()


        for row in dataset:

            entry = Entries(row['id'], row['concept'], row['entry'], row['date'], row['moodId'])
            mood = Moods(row['id'], row['label_mood'])
            entry.mood = mood.__dict__
            entries.append(entry.__dict__)

    return json.dumps(entries)

def get_single_entry(id):
    with sqlite3.connect("./daily-journal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            a.id,
            a.concept,
            a.entry,
            a.date,
            a.moodId
        FROM entries a
        WHERE a.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()

        entry = Entries(data['id'], data['concept'], data['entry'], data['date'], data['moodId'])

        return json.dumps(entry.__dict__)

def delete_entry(id):
    with sqlite3.connect("./daily-journal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM entries
        WHERE id = ?
        """, (id, ))

def get_entry_by_word(q):
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
        WHERE a.entry LIKE "%"||?||"%"
        """, (q, ))

        entries = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            entry = Entries(row["id"], row["concept"], row["entry"], row["date"], row["moodId"])
            entries.append(entry.__dict__)

    return json.dumps(entries)

def create_new_entry(new_entry):
    with sqlite3.connect("./daily-journal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO entries
            ( concept, entry, date, moodId )
        VALUES
            ( ?, ?, ?, ?);
        """, (new_entry['concept'], new_entry['entry'], new_entry['date'], new_entry['moodId'], ))

        id = db_cursor.lastrowid

        new_entry['id'] = id

    return json.dumps(new_entry)

def update_entry(id, new_entry):
    with sqlite3.connect("./daily-journal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE entries
            SET
                concept = ?,
                entry = ?,
                date = ?,
                moodId = ?
        WHERE id = ?
        """, (new_entry['concept'], new_entry['entry'], new_entry['date'], new_entry['moodId'], id, ))

        rows_affected = db_cursor.rowcount
    
    if rows_affected == 0:
        return False
    else:
        return True
