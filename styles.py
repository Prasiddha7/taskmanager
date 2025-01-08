def apply_styles(window):
    window.setStyleSheet("""
        QMainWindow {
            background-color: #f5f5f5;
        }
        QLabel {
            font-size: 16px;
            font-weight: bold;
            color: #333;
            margin-block:auto;
        }
        QLineEdit, QComboBox, QDateEdit {
            padding: 5px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        QPushButton {
            padding: 10px;
            background-color: #4caf50;
            color: white;
            border: none;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QTreeWidget {
            border: 1px solid #ccc;
            background-color: #fff;
        }
                        
    """)
