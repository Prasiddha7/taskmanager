from database import Database

class TaskModel:
    def __init__(self, db_path):
        self.db = Database(db_path)

    def add_task(self, category, task, priority, due_date, status):
        if not category or not task or not priority or not due_date or not status:
            raise ValueError("All fields must be filled out.")
        self.db.insert_task(category, task, priority, due_date, status)

    def get_tasks_by_category(self):
        tasks = self.db.fetch_tasks()
        tasks_by_category = {}
        for task in tasks:
            category = task["category"]
            if category not in tasks_by_category:
                tasks_by_category[category] = []
            tasks_by_category[category].append(task)
        return tasks_by_category

    def delete_task(self, task):
        if not task:
            raise ValueError("Task description cannot be empty.")
        self.db.delete_task(task)

    def update_task(self, old_task, new_task):
        if not old_task or not new_task:
            raise ValueError("Both old and new task descriptions must be provided.")
        self.db.update_task(old_task, new_task)
