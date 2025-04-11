import sys
import os
import sqlite3
import subprocess
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTabWidget, QTableView,
    QPushButton, QLabel, QDialog, QLineEdit, QFormLayout
)
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel


class MusicLibraryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Music Library")
        self.setGeometry(100, 100, 800, 600)

        self.db_path = "music_service.db"
        self.init_db()
        self.init_ui()

    def init_db(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(self.db_path)
        if not self.db.open():
            print("Failed to connect to database.")
            sys.exit(1)

    def reset_database(self):
        print("Resetting database...")

        self.db.close()
        QSqlDatabase.removeDatabase("qt_sql_default_connection")

        if os.path.exists(self.db_path):
            os.remove(self.db_path)

        try:
            with open("create.sql", "r") as f:
                create_sql = f.read()

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.executescript(create_sql)
            conn.commit()
            conn.close()
            print("Database reset successfully.")
        except Exception as e:
            print(f"Error resetting database: {e}")
            return

        self.init_db()
        self.refresh_models()

    def sync_music_data(self):
        try:
            print("Running Metadata.py...")
            subprocess.run(["python", "Metadata.py"], check=True)

            print("Running InsertIntoDB.py...")
            subprocess.run(["python", "InsertIntoDB.py"], check=True)

            # Clear insert.sql after execution
            with open("insert.sql", "w") as f:
                f.truncate(0)  # Clear the file content
            print("insert.sql cleared.")

            self.refresh_models()
            print("Music data synced successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error running script: {e}")

    def sync_users_data(self):
        try:
            print("Running users.py...")
            subprocess.run(["python", "users.py"], check=True)

            print("Running InsertIntoDB.py...")
            subprocess.run(["python", "InsertIntoDB.py"], check=True)

            # Clear insert.sql after execution
            with open("insert.sql", "w") as f:
                f.truncate(0)  # Clear the file content
            print("insert.sql cleared.")

            self.refresh_models()
            print("Users data synced successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error running script: {e}")

    def refresh_models(self):
        self.songs_model.select()
        self.artists_model.select()
        self.albums_model.select()
        self.users_model.select()

    def init_ui(self):
        layout = QVBoxLayout()
        self.tabs = QTabWidget()

        # Main tab
        main_tab = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setSpacing(1)
        main_layout.setContentsMargins(0, 0, 0, 0)

        reset_button = QPushButton("Reset Database")
        reset_button.clicked.connect(self.reset_database)

        sync_music_button = QPushButton("Sync Music Data")
        sync_music_button.clicked.connect(self.sync_music_data)

        sync_users_button = QPushButton("Sync Users Data")
        sync_users_button.clicked.connect(self.sync_users_data)

        main_layout.addWidget(reset_button)
        main_layout.addWidget(sync_music_button)
        main_layout.addWidget(sync_users_button)

        main_tab.setLayout(main_layout)
        self.tabs.insertTab(0, main_tab, "Main")

        # Table views
        self.songs_view, self.songs_model = self.create_table_view("Songs")
        self.artists_view, self.artists_model = self.create_table_view("Artists")
        self.albums_view, self.albums_model = self.create_table_view("Albums")
        self.users_view, self.users_model, users_tab = self.create_users_tab()

        self.tabs.addTab(self.songs_view, "Songs")
        self.tabs.addTab(self.artists_view, "Artists")
        self.tabs.addTab(self.albums_view, "Albums")
        self.tabs.addTab(users_tab, "Users")

        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def create_table_view(self, table_name):
        model = QSqlTableModel(self)
        model.setTable(table_name)
        model.select()

        view = QTableView()
        view.setModel(model)
        view.resizeColumnsToContents()
        return view, model

    def create_users_tab(self):
        layout = QVBoxLayout()
        model = QSqlTableModel(self)
        model.setTable("Users")
        model.select()

        users_view = QTableView()
        users_view.setModel(model)
        users_view.resizeColumnsToContents()

        delete_button = QPushButton("Delete User")
        delete_button.clicked.connect(lambda: self.delete_selected_row(users_view))

        add_user_button = QPushButton("Add User")
        add_user_button.clicked.connect(self.add_user_popup)

        layout.addWidget(users_view)
        layout.addWidget(delete_button)
        layout.addWidget(add_user_button)

        container = QWidget()
        container.setLayout(layout)
        return users_view, model, container

    def delete_selected_row(self, view):
        model = view.model()
        selected_indexes = view.selectionModel().selectedRows()

        if selected_indexes:
            for index in selected_indexes:
                model.removeRow(index.row())
            if not model.submitAll():
                print("Failed to submit deletion.")
            else:
                model.select()
        else:
            print("No row selected for deletion.")

    def add_user_popup(self):
        # Popup to add new user
        self.dialog = QDialog(self)
        self.dialog.setWindowTitle("Add New User")

        form_layout = QFormLayout()
        self.username_input = QLineEdit()
        self.email_input = QLineEdit()

        form_layout.addRow("Username:", self.username_input)
        form_layout.addRow("Email:", self.email_input)

        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.add_new_user)
        form_layout.addRow(submit_button)

        self.dialog.setLayout(form_layout)
        self.dialog.exec_()

    def add_new_user(self):
        # Get user input from popup
        username = self.username_input.text()
        email = self.email_input.text()

        if not username or not email:
            print("Username and Email cannot be empty.")
            return

        # Insert the user into the database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Users (Username, Email, JoinDate) VALUES (?, ?, ?)",
                       (username, email, "2025-04-11"))  # Use current date or timestamp
        conn.commit()

        # Get the new user data and update users.json
        new_user = {"UserID": cursor.lastrowid, "Username": username, "Email": email, "JoinDate": "2025-04-11"}
        self.add_user_to_json(new_user)

        # Close dialog and refresh users table
        self.dialog.accept()
        self.users_view.model().select()

    def add_user_to_json(self, new_user):
        # Read the current users from users.json
        try:
            with open("users.json", "r", encoding="utf-8") as f:
                users = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            users = []

        # Append the new user to the list
        users.append(new_user)

        # Write the updated list back to users.json
        with open("users.json", "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MusicLibraryApp()
    window.show()
    sys.exit(app.exec_())
