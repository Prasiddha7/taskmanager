from PyQt5.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QTreeWidget,
    QTreeWidgetItem,
    QWidget,
    QMessageBox,
    QInputDialog,
    QComboBox,
    QDateEdit,
    QStackedWidget,
    QFormLayout,
    QApplication,
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QDate
from models import TaskModel
from styles import apply_styles
import sys
import os



class TaskManager(QMainWindow):
    def __init__(self, **kwargs):
        super().__init__()
        self.setWindowTitle("Task Manager")
        self.showFullScreen()

        # Handle PyInstaller's temporary directory for bundled resources
        if hasattr(sys, "_MEIPASS"):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")

        # Determine the database path
        db_path = kwargs.get("db_path", os.path.join(base_path, "tasks.db"))

        # Apply external styles
        apply_styles(self)

        # Pass the resolved db_path directly to TaskModel
        self.task_model = TaskModel(db_path)

        # Central Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Welcome Section
        self.setup_welcome_section()

        # Navigation Bar
        self.setup_navigation_bar()

        # Stacked Widget for Pages
        self.pages = QStackedWidget()
        self.layout.addWidget(self.pages)

        # Create Task Page
        self.setup_create_task_page()

        # Task List Page
        self.setup_task_list_page()

        # Show Create Task Page by Default
        self.pages.setCurrentWidget(self.post_page)

    def setup_welcome_section(self):
        """Sets up the welcome heading."""
        self.welcome_layout = QVBoxLayout()
        self.welcome_heading = QLabel("WELCOME TO TASK MANAGER")
        self.welcome_heading.setFont(QFont("Arial", 102, QFont.Bold))  # Large font size
        self.welcome_heading.setAlignment(Qt.AlignCenter)  # Center alignment
        self.welcome_layout.addWidget(self.welcome_heading)
        self.welcome_layout.setContentsMargins(0, 120, 0, 0)  # Padding from top
        self.layout.addLayout(self.welcome_layout)

    def setup_navigation_bar(self):
        """Sets up the navigation bar."""
        self.nav_layout = QHBoxLayout()
        self.view_list_button = QPushButton("View Task List")
        self.view_list_button.setFixedSize(120, 30)  # Button dimensions
        self.view_list_button.clicked.connect(self.show_list_page)
        self.nav_layout.addStretch()  # Push button to the right
        self.nav_layout.addWidget(self.view_list_button)
        self.layout.addLayout(self.nav_layout)

    def setup_create_task_page(self):
        """Sets up the Create Task page."""
        self.post_page = QWidget()
        self.post_layout = QVBoxLayout()

        # Heading
        self.create_task_heading = QLabel("Create A New Task")
        self.create_task_heading.setFont(QFont("Arial", 32, QFont.Bold))
        self.create_task_heading.setAlignment(Qt.AlignCenter)
        self.post_layout.addWidget(self.create_task_heading, alignment=Qt.AlignCenter)

        # Reduce the spacer between the heading and form
        self.post_layout.addSpacing(-110)

        # Form Wrapper Layout
        self.task_form_wrapper = QVBoxLayout()
        self.task_form_wrapper.setAlignment(Qt.AlignCenter)

        input_field_width = 500 

        # Task Form Layout
        self.task_form_layout = QFormLayout()
        self.task_form_layout.setContentsMargins(100, -30, 100, 0)  # Adjust margins
        self.task_form_layout.setHorizontalSpacing(20)
        self.task_form_layout.setVerticalSpacing(15)

        # Category Input
        self.category_input = QLineEdit()
        self.category_input.setFixedSize(input_field_width, 40) 
        self.category_input.setPlaceholderText("Enter Category")
        self.task_form_layout.addRow(QLabel("Category:"), self.category_input)

        # Task Input
        self.task_input = QLineEdit()
        self.task_input.setFixedSize(input_field_width,40)
        self.task_input.setPlaceholderText("Enter Task")
        self.task_form_layout.addRow(QLabel("Task:"), self.task_input)

        # Priority Dropdown
        self.priority_dropdown = QComboBox()
        self.priority_dropdown.setFixedSize(input_field_width,40)
        self.priority_dropdown.addItems(["Low", "Medium", "High"])
        self.task_form_layout.addRow(QLabel("Priority:"), self.priority_dropdown)

        # Due Date Field
        self.due_date_input = QDateEdit()
        self.due_date_input.setFixedSize(input_field_width,40)
        self.due_date_input.setDate(QDate.currentDate())
        self.due_date_input.setCalendarPopup(True)
        self.task_form_layout.addRow(QLabel("Due Date:"), self.due_date_input)

        # Status Dropdown
        self.status_dropdown = QComboBox()
        self.status_dropdown.setFixedSize(input_field_width,40)
        self.status_dropdown.addItems(["Pending", "In Progress", "Completed"])
        self.task_form_layout.addRow(QLabel("Status:"), self.status_dropdown)

        # Add Button
        self.add_button = QPushButton("Add Task")
        self.add_button.setFixedSize(120, 40)
        self.add_button.clicked.connect(self.add_task)

        # Center align the Add Task button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.add_button)
        button_layout.addStretch()
        self.task_form_layout.addRow("", button_layout)

        self.post_layout.addLayout(self.task_form_layout)
        self.post_page.setLayout(self.post_layout)
        self.pages.addWidget(self.post_page)


    def setup_task_list_page(self):
        """Sets up the Task List page."""
        self.list_page = QWidget()
        self.list_layout = QVBoxLayout()

        # Back Button
        self.back_button = QPushButton("Back to Create Page")
        self.back_button.setFixedSize(180, 40)
        self.back_button.clicked.connect(self.show_post_page)
        self.list_layout.addWidget(self.back_button, alignment=Qt.AlignRight)

        # Task Tree Widget
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Category", "Task", "Priority", "Due Date", "Status", "Actions"])
        self.list_layout.addWidget(self.tree)

        self.list_page.setLayout(self.list_layout)
        self.pages.addWidget(self.list_page)

    def show_list_page(self):
        """Switch to the Task List page."""
        self.populate_tree()
        self.pages.setCurrentWidget(self.list_page)

    def show_post_page(self):
        """Switch to the Create Task page."""
        self.pages.setCurrentWidget(self.post_page)

    def add_task(self):
        """Add a new task to the database."""
        category = self.category_input.text().strip()
        task = self.task_input.text().strip()
        priority = self.priority_dropdown.currentText()
        due_date = self.due_date_input.date().toString("yyyy-MM-dd")
        status = self.status_dropdown.currentText()

        try:
            self.task_model.add_task(category, task, priority, due_date, status)
            QMessageBox.information(self, "Success", "Task added successfully!")
            self.category_input.clear()
            self.task_input.clear()
            self.priority_dropdown.setCurrentIndex(0)
            self.due_date_input.setDate(QDate.currentDate())
            self.status_dropdown.setCurrentIndex(0)
        except ValueError as e:
            QMessageBox.warning(self, "Input Error", str(e))

    def populate_tree(self):
        """Populate the task list in the tree widget."""
        self.tree.clear()
        tasks_by_category = self.task_model.get_tasks_by_category()

        for category, tasks in tasks_by_category.items():
            category_item = QTreeWidgetItem([category])
            self.tree.addTopLevelItem(category_item)

            for task_details in tasks:
                task_item = QTreeWidgetItem([
                    "", task_details["task"], task_details["priority"],
                    task_details["due_date"], task_details["status"]
                ])
                category_item.addChild(task_item)

                self.add_action_buttons(task_item)

    def add_action_buttons(self, item):
        """Add Edit and Delete buttons for each task in the tree."""
        edit_button = QPushButton("Edit")
        edit_button.setFixedSize(100, 30)
        edit_button.clicked.connect(lambda: self.edit_task(item))

        delete_button = QPushButton("Delete")
        delete_button.setFixedSize(100, 30)
        delete_button.setStyleSheet("background-color: #FF0000; color: white;")
        delete_button.clicked.connect(lambda: self.delete_task(item))

        button_container = QWidget()
        button_layout = QHBoxLayout() 
        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)
        button_layout.setContentsMargins(10, 0, 0,10)
        button_layout.setSpacing(-25)
        button_container.setLayout(button_layout)

        self.tree.setItemWidget(item, 5, button_container)

    def delete_task(self, item):
        """Delete a task from the database."""
        task = item.text(1)
        try:
            self.task_model.delete_task(task)
            self.populate_tree()
        except ValueError as e:
            QMessageBox.warning(self, "Delete Error", str(e))

    def edit_task(self, item):
        """Edit a task in the database."""
        old_task = item.text(1)
        new_task, ok = QInputDialog.getText(self, "Edit Task", "Update Task:", text=old_task)
        if ok and new_task:
            try:
                self.task_model.update_task(old_task, new_task)
                self.populate_tree()
            except ValueError as e:
                QMessageBox.warning(self, "Edit Error", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TaskManager()
    window.show()
    sys.exit(app.exec_())
