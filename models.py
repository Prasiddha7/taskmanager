from database import Database

class TaskModel:
    def __init__(self, db_name="tasks.db"):
        self.db = Database(db_name)

    def add_task(self, category, task, priority, due_date, status):
        if not category or not task:
            raise ValueError("Both category and task are required.")
        self.db.add_task(category, task, priority, due_date, status)

    def get_tasks_by_category(self):
        tasks = self.db.get_tasks()
        grouped_tasks = {}
        for category, task, priority, due_date, status in tasks:
            if category not in grouped_tasks:
                grouped_tasks[category] = []
            grouped_tasks[category].append({
                "task": task,
                "priority": priority,
                "due_date": due_date,
                "status": status
            })
        return grouped_tasks

    def delete_task(self, task):
        self.db.delete_task(task)

    def update_task(self, old_task, new_task):
        self.db.update_task(old_task, new_task)
