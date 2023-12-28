import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QGridLayout, QMessageBox, QStackedWidget
import hashlib
import re

class DatabaseHandler:
    def __init__(self, db_path='user_database.db'):
        self.db_path = db_path
        self.create_table()

    def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        '''
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(query)

    def add_user(self, username, password):
        if self.is_valid_username(username):
            hashed_password = self.hash_password(password)
            query = 'INSERT INTO users (username, password) VALUES (?, ?)'
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(query, (username, hashed_password))
                conn.commit()
        else:
            QMessageBox.warning(None, 'Invalid Username', 'Username contains invalid characters.')

    def validate_user(self, username, password):
        if self.is_valid_username(username):
            hashed_password = self.hash_password(password)
            query = 'SELECT * FROM users WHERE username=? AND password=?'
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(query, (username, hashed_password))
                return cursor.fetchone() is not None
        else:
            return False

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def is_valid_username(username):
        # Allow only alphanumeric characters and underscores
        return re.match("^[a-zA-Z0-9_]+$", username) is not None


class LoginPage(QWidget):
    def __init__(self, stacked_widget, database_handler):
        super().__init__()

        self.stacked_widget = stacked_widget
        self.database_handler = database_handler

        self.initUI()

    def initUI(self):
        # Create widgets
        self.username_label = QLabel('Username:')
        self.password_label = QLabel('Password:')
        self.username_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.login_button = QPushButton('Login', self)

        # Set password input to show dots instead of text
        self.password_input.setEchoMode(QLineEdit.Password)

        # Create grid layout
        layout = QGridLayout()
        layout.addWidget(self.username_label, 0, 0)
        layout.addWidget(self.username_input, 0, 1)
        layout.addWidget(self.password_label, 1, 0)
        layout.addWidget(self.password_input, 1, 1)
        layout.addWidget(self.login_button, 2, 0, 1, 2)

        # Center the form in the middle of the window
        central_widget = QWidget()
        central_widget.setLayout(layout)

        # Set the central widget for the main window
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(central_widget)

        # Connect the login button to the login function
        self.login_button.clicked.connect(self.login)

    def login(self):
        # Get the entered username and password
        username = self.username_input.text()
        password = self.password_input.text()

        # Validate user credentials using the database handler
        if self.database_handler.validate_user(username, password):
            QMessageBox.information(self, 'Login Successful', 'Welcome, {}'.format(username))
            # Switch to the next page (replace with the actual page you want to show)
            self.stacked_widget.setCurrentIndex(1)
        else:
            QMessageBox.warning(self, 'Login Failed', 'Invalid username or password')


class MainPage(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Create widgets for the main page
        label = QLabel('Welcome to the Main Page!', self)

        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(label)

        # Set the layout for the main window
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Create a stacked widget to switch between pages
    stacked_widget = QStackedWidget()

    # Create an instance of the database handler
    database_handler = DatabaseHandler()

    # Create instances of the login and main pages
    login_page = LoginPage(stacked_widget, database_handler)
    main_page = MainPage()

    # Add pages to the stacked widget
    stacked_widget.addWidget(login_page)
    stacked_widget.addWidget(main_page)

    # Create a main window (QMainWindow)
    main_window = QMainWindow()
    main_window.setCentralWidget(stacked_widget)
    main_window.setGeometry(300, 300, 300, 200)
    main_window.setWindowTitle('Web-like Login Page')

    # Maximize the window to full screen
    main_window.showMaximized()
    # Show the main window
    main_window.show()

    sys.exit(app.exec_())
