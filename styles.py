def apply_styles(widget):
    widget.setStyleSheet("""
        QLabel {
            font-size: 16px;
            font-weight: bold;
            color: #333333;
        }
        QPushButton {
            background-color: #007BFF;
            color: white;
            border: 1px solid #0056b3;
            border-radius: 5px;
            padding: 5px 10px;
        }
        QPushButton:hover {
            background-color: #0056b3;
        }
        QTreeWidget {
            border: 1px solid #ccc;
        }
    """)
