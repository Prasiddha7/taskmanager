import sqlite3


class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self.create_table()

    def create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    task TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    due_date TEXT NOT NULL,
                    status TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def insert_task(self, category, task, priority, due_date, status):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO tasks (category, task, priority, due_date, status)
                VALUES (?, ?, ?, ?, ?)
                """,
                (category, task, priority, due_date, status),
            )
            conn.commit()

    def fetch_tasks(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT category, task, priority, due_date, status
                FROM tasks
                """
            )
            columns = [desc[0] for desc in cursor.description]
            tasks = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return tasks

    def delete_task(self, task):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE task = ?", (task,))
            conn.commit()

    def update_task(self, old_task, new_task):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE tasks SET task = ? WHERE task = ?", (new_task, old_task)
            )
            conn.commit()
