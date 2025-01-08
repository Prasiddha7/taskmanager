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
    QSpacerItem,  # Import QSpacerItem
    QSizePolicy 
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QDate
from models import TaskModel
from styles import apply_styles


class TaskManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Manager")
        # self.setGeometry(100, 100, 900, 600)

        self.showFullScreen()

        # Apply styles
        apply_styles(self)

        # Task Model
        self.task_model = TaskModel()

        # Central Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)


        # Welcome Layout with Padding
        self.welcome_layout = QVBoxLayout()

        # Welcome Layout with Padding
        self.welcome_layout = QVBoxLayout()

        # Add top padding using margins
        self.welcome_layout.setContentsMargins(0, 120, 0, 0)  # Add 100px padding at the top

        # Welcome Heading
        self.welcome_heading = QLabel("WELCOME TO TASK MANAGER")
        self.welcome_heading.setFont(QFont("Arial", 102, QFont.Bold))  # Increased font size
        self.welcome_heading.setAlignment(Qt.AlignCenter)  # Center alignment
        self.welcome_layout.addWidget(self.welcome_heading)

        # Add the welcome layout to the main layout
        self.layout.addLayout(self.welcome_layout)



        # Navigation
        self.nav_layout = QHBoxLayout()
        self.view_list_button = QPushButton("View Task List")
        self.view_list_button.setFixedSize(120, 30)  # Small, visually appealing button
        self.view_list_button.clicked.connect(self.show_list_page)
        self.nav_layout.addStretch()  # Push button to the right
        self.nav_layout.addWidget(self.view_list_button)
        self.layout.addLayout(self.nav_layout)

        # Stacked Widget for Pages
        self.pages = QStackedWidget()
        self.layout.addWidget(self.pages)

        # Create Task Page
        self.post_page = QWidget()
        self.post_layout = QVBoxLayout()


        # Create Task Heading
        self.create_task_heading = QLabel("Create A New Task")
        self.create_task_heading.setFont(QFont("Arial", 32, QFont.Bold))
        self.create_task_heading.setAlignment(Qt.AlignCenter)
        self.post_layout.addWidget(self.create_task_heading, alignment=Qt.AlignCenter)

        # Add a spacer to move the form closer to the heading
        self.post_layout.addSpacing(130)

        # Task Form Wrapper Layout
        self.task_form_wrapper = QVBoxLayout()
        self.task_form_wrapper.setAlignment(Qt.AlignCenter)  #place the form in center horizontally 

        # Task Form Layout
        self.task_form_layout = QVBoxLayout()
        self.form_widget = QWidget()
        self.form_widget.setLayout(self.task_form_layout)
        self.form_widget.setFixedWidth(self.width() // 3) 
        self.task_form_wrapper.addWidget(self.form_widget)

        # Add Spaceing below the form
        spacer = QSpacerItem(60, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.task_form_wrapper.addSpacerItem(spacer)

        # Adjust the margins to move everything slightly upward
        self.task_form_wrapper.setContentsMargins(100, -30, 100, 0)  # Reduce top and bottom margins

        # Category Field
        self.category_label = QLabel("Category:")
        self.category_label.setFont(QFont("Arial", 12)) 
        self.task_form_layout.addWidget(self.category_label)

        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("Enter Category")
        self.task_form_layout.addWidget(self.category_input)

        # Task Field
        self.task_label = QLabel("Task:")
        self.task_label.setFont(QFont("Arial", 12))
        self.task_form_layout.addWidget(self.task_label)

        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter Task")
        self.task_form_layout.addWidget(self.task_input)

        # Priority Dropdown
        self.priority_label = QLabel("Priority:")
        self.priority_label.setFont(QFont("Arial", 12))
        self.task_form_layout.addWidget(self.priority_label)

        self.priority_dropdown = QComboBox()
        self.priority_dropdown.addItems(["Low", "Medium", "High"])
        self.task_form_layout.addWidget(self.priority_dropdown)

        # Due Date Field
        self.due_date_label = QLabel("Due Date:")
        self.due_date_label.setFont(QFont("Arial", 12))
        self.task_form_layout.addWidget(self.due_date_label)

        self.due_date_input = QDateEdit()
        self.due_date_input.setDate(QDate.currentDate())
        self.due_date_input.setCalendarPopup(True)
        self.task_form_layout.addWidget(self.due_date_input)

        # Status Dropdown
        self.status_label = QLabel("Status:")
        self.status_label.setFont(QFont("Arial", 12))
        self.task_form_layout.addWidget(self.status_label)

        self.status_dropdown = QComboBox()
        self.status_dropdown.addItems(["Pending", "In Progress", "Completed"])
        self.task_form_layout.addWidget(self.status_dropdown)

        # Task Button
        self.add_button = QPushButton("Add Task")
        self.add_button.setFixedSize(120, 40)
        self.add_button.clicked.connect(self.add_task)
        self.task_form_layout.addWidget(self.add_button, alignment=Qt.AlignCenter)

        # Add the wrapper layout to the main layout
        self.post_layout.addLayout(self.task_form_wrapper)

        self.post_page.setLayout(self.post_layout)

        self.pages.addWidget(self.post_page)

        # Task List Page
        self.list_page = QWidget()
        self.list_layout = QVBoxLayout()

        # Back Button
        self.back_button = QPushButton("Back to Create Page")
        self.back_button.setFixedSize(180, 40) 
        self.back_button.clicked.connect(self.show_post_page)
        self.list_layout.addWidget(self.back_button, alignment=Qt.AlignRight)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Category", "Task", "Priority", "Due Date", "Status", "Actions"])
        self.list_layout.addWidget(self.tree)

        self.list_page.setLayout(self.list_layout)
        self.pages.addWidget(self.list_page)

        # Show Create Task Page by Default
        self.pages.setCurrentWidget(self.post_page)

    def show_list_page(self):
        """Show the Task List Page."""   
        self.populate_tree()
        self.pages.setCurrentWidget(self.list_page)

    def show_post_page(self):
        """Show the Create Task Page."""
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
        # Clear existing items
        self.tree.clear()

        # Get tasks grouped by category
        tasks_by_category = self.task_model.get_tasks_by_category()

        # Loop through each category and its tasks
        for category, tasks in tasks_by_category.items():
            # Create a parent item for the category
            category_item = QTreeWidgetItem([category])
            self.tree.addTopLevelItem(category_item)

            # Add tasks as children of the category item
            for task_details in tasks:
                task_item = QTreeWidgetItem([
                    "",  # Placeholder for the category column
                    task_details["task"],
                    task_details["priority"],
                    task_details["due_date"],
                    task_details["status"]
                ])
                category_item.addChild(task_item)

                # Add Edit and Delete buttons
                self.add_action_buttons(task_item)

        # Expand all items in the tree for visibility
        self.tree.expandAll()


    def add_action_buttons(self, item):
        """Add Edit and Delete buttons for each task in the tree."""
        edit_button = QPushButton("Edit")
        edit_button.setFixedSize(100, 30)  # Smaller buttons
        delete_button = QPushButton("Delete")
        delete_button.setFixedSize(100, 30)  # Smaller buttons

        delete_button.setStyleSheet("background-color: #FF0000; color: white; border: none; border-radius: 5px;")

        button_container = QWidget()
        button_layout = QHBoxLayout()
        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)
        button_layout.setContentsMargins(10, 0, 0, 10)  
        button_layout.setSpacing(75)  # Reduce spacing between buttons
        button_container.setLayout(button_layout)
        button_container.setFixedWidth(250) 

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
        new_task, ok = QInputDialog.getText(self, "Edit Task", "New Task:", text=old_task)
        if ok and new_task:
            try:
                self.task_model.update_task(old_task, new_task)
                self.populate_tree()
            except ValueError as e:
                QMessageBox.warning(self, "Update Error", str(e))
