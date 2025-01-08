import sqlite3

class Database:
    def __init__(self, db_name="tasks.db"):
        self.db_name = db_name
        self.create_table()

    def create_table(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            # Create table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    task TEXT NOT NULL
                )
            """)
            # Add missing columns
            try:
                cursor.execute("ALTER TABLE tasks ADD COLUMN priority TEXT DEFAULT 'Medium'")
            except sqlite3.OperationalError:
                pass  # Column already exists
            try:
                cursor.execute("ALTER TABLE tasks ADD COLUMN due_date TEXT DEFAULT ''")
            except sqlite3.OperationalError:
                pass  # Column already exists
            try:
                cursor.execute("ALTER TABLE tasks ADD COLUMN status TEXT DEFAULT 'Pending'")
            except sqlite3.OperationalError:
                pass  # Column already exists
            conn.commit()

    def add_task(self, category, task, priority, due_date, status):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO tasks (category, task, priority, due_date, status)
                VALUES (?, ?, ?, ?, ?)
            """, (category, task, priority, due_date, status))
            conn.commit()

    def get_tasks(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT category, task, priority, due_date, status FROM tasks")
            return cursor.fetchall()

    def delete_task(self, task):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE task = ?", (task,))
            conn.commit()

    def update_task(self, old_task, new_task):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE tasks SET task = ? WHERE task = ?", (new_task, old_task))
            conn.commit()
