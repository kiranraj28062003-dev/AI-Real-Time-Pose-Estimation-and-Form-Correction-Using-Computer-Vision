import sqlite3

def init_db():
    conn = sqlite3.connect("workout.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS history(
        username TEXT,
        exercise TEXT,
        reps INTEGER,
        calories REAL,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()

def save_workout(user, ex, reps, cal, date):
    conn = sqlite3.connect("workout.db")
    c = conn.cursor()
    c.execute("INSERT INTO history VALUES (?,?,?,?,?)",
              (user, ex, reps, cal, date))
    conn.commit()
    conn.close()

def get_leaderboard():
    conn = sqlite3.connect("workout.db")
    c = conn.cursor()

    c.execute("""
    SELECT username, SUM(reps)
    FROM history
    GROUP BY username
    ORDER BY SUM(reps) DESC
    LIMIT 5
    """)

    data = c.fetchall()
    conn.close()
    return data

def get_all():
    conn = sqlite3.connect("workout.db")
    c = conn.cursor()
    c.execute("SELECT * FROM history")
    data = c.fetchall()
    conn.close()
    return data

init_db()