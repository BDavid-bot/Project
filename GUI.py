import sys
import os
import sqlite3
import subprocess
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTabWidget, QTableView,
    QPushButton, QLabel, QDialog, QLineEdit, QFormLayout, QHBoxLayout
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

            with open("insert.sql", "w") as f:
                f.truncate(0)
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

            with open("insert.sql", "w") as f:
                f.truncate(0)
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

        add_button = QPushButton("Add User")
        add_button.clicked.connect(self.add_user_dialog)

        delete_button = QPushButton("Delete User")
        delete_button.clicked.connect(lambda: self.delete_selected_row(users_view))

        edit_button = QPushButton("Edit User")
        edit_button.clicked.connect(lambda: self.edit_selected_user(users_view))

        layout.addWidget(users_view)
        layout.addWidget(add_button)
        layout.addWidget(delete_button)
        layout.addWidget(edit_button)

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

    def edit_selected_user(self, view):
        model = view.model()
        selected_indexes = view.selectionModel().selectedRows()

        if not selected_indexes:
            print("No user selected for editing.")
            return

        index = selected_indexes[0]
        row = index.row()
        user_id = model.data(model.index(row, 0))
        current_username = model.data(model.index(row, 1))
        current_email = model.data(model.index(row, 2))

        dialog = QDialog(self)
        dialog.setWindowTitle("Edit User")

        form = QFormLayout()
        username_input = QLineEdit(current_username)
        email_input = QLineEdit(current_email)
        form.addRow("Username:", username_input)
        form.addRow("Email:", email_input)

        save_button = QPushButton("Save")
        save_button.clicked.connect(lambda: self.save_user_changes(dialog, model, row, user_id, username_input.text(), email_input.text()))

        form.addWidget(save_button)
        dialog.setLayout(form)
        dialog.exec_()

    def save_user_changes(self, dialog, model, row, user_id, new_username, new_email):
        model.setData(model.index(row, 1), new_username)
        model.setData(model.index(row, 2), new_email)
        if model.submitAll():
            print("User info updated in DB.")
            self.update_users_json(user_id, new_username, new_email)
        else:
            print("Failed to update DB.")
        dialog.accept()
        model.select()

    def update_users_json(self, user_id, new_username, new_email):
        try:
            with open("users.json", "r") as f:
                users = json.load(f)
        except FileNotFoundError:
            users = []

        for user in users:
            if user.get("UserID") == user_id:
                user["username"] = new_username
                user["email"] = new_email
                break

        with open("users.json", "w") as f:
            json.dump(users, f, indent=4)
        print("users.json updated.")

    def add_user_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add User")

        form = QFormLayout()
        username_input = QLineEdit()
        email_input = QLineEdit()
        form.addRow("Username:", username_input)
        form.addRow("Email:", email_input)

        save_button = QPushButton("Add")
        save_button.clicked.connect(lambda: self.add_user(dialog, username_input.text(), email_input.text()))
        form.addWidget(save_button)

        dialog.setLayout(form)
        dialog.exec_()

    def add_user(self, dialog, username, email):
        try:
            with open("users.json", "r") as f:
                users = json.load(f)
        except FileNotFoundError:
            users = []

        existing_ids = [user["UserID"] for user in users]
        new_id = max(existing_ids) + 1 if existing_ids else 1

        new_user = {
            "UserID": new_id,
            "username": username,
            "email": email,
            "join_date": "04-12-2025"
        }
        users.append(new_user)

        with open("users.json", "w") as f:
            json.dump(users, f, indent=4)

        print("New user added to users.json.")
        dialog.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MusicLibraryApp()
    window.show()
    sys.exit(app.exec_())
