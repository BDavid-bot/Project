import sys
import os
import sqlite3
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTabWidget, QTableView,
    QPushButton, QLabel, QComboBox, QDialog, QFormLayout, QLineEdit, QDialogButtonBox
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

    def refresh_models(self):
        self.songs_model.select()
        self.artists_model.select()
        self.albums_model.select()
        self.users_model.select()

    def refresh_artist_names(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM Artists")
            artist_names = [row[0] for row in cursor.fetchall()]
            conn.close()

            self.search_combo.clear()  # Clear existing items
            self.search_combo.addItems(artist_names)  # Add new artist names
        except Exception as e:
            print(f"Error fetching artist names: {e}")

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

        main_layout.addWidget(reset_button)
        main_layout.addWidget(sync_music_button)

        main_tab.setLayout(main_layout)
        self.tabs.insertTab(0, main_tab, "Main")

        # Table views
        self.songs_view, self.songs_model = self.create_table_view("Songs")
        self.artists_view, self.artists_model = self.create_table_view("Artists")
        self.albums_view, self.albums_model = self.create_table_view("Albums")
        self.users_view, self.users_model, users_tab = self.create_users_tab()
        search_tab = self.create_search_tab()

        self.tabs.addTab(self.songs_view, "Songs")
        self.tabs.addTab(self.artists_view, "Artists")
        self.tabs.addTab(self.albums_view, "Albums")
        self.tabs.addTab(users_tab, "Users")
        self.tabs.addTab(search_tab, "Search")

        layout.addWidget(self.tabs)
        self.setLayout(layout)

        # Connect the tab change event to refresh the search combo box
        self.tabs.currentChanged.connect(self.on_tab_changed)

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

        add_button = QPushButton("Add User")
        add_button.clicked.connect(self.open_add_user_dialog)

        edit_button = QPushButton("Edit Selected User")
        edit_button.clicked.connect(lambda: self.open_edit_user_dialog(users_view))

        layout.addWidget(users_view)
        layout.addWidget(delete_button)
        layout.addWidget(add_button)
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

    def open_add_user_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add New User")

        layout = QFormLayout(dialog)
        username_input = QLineEdit()
        email_input = QLineEdit()

        layout.addRow("Username:", username_input)
        layout.addRow("Email:", email_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(buttons)

        buttons.accepted.connect(lambda: self.add_user(username_input.text(), email_input.text(), dialog))
        buttons.rejected.connect(dialog.reject)

        dialog.exec_()

    def add_user(self, username, email, dialog):
        from datetime import datetime

        new_user = {
            "Username": username,
            "Email": email,
            "JoinDate": datetime.now().strftime("%Y-%m-%d")
        }

        # Add user directly to the database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Users (Username, Email, JoinDate) VALUES (?, ?, ?)",
                       (username, email, new_user["JoinDate"]))
        conn.commit()
        conn.close()

        self.refresh_models()
        dialog.accept()

    def open_edit_user_dialog(self, view):
        model = view.model()
        selected_indexes = view.selectionModel().selectedRows()

        if not selected_indexes:
            print("No user selected for editing.")
            return

        selected_row = selected_indexes[0].row()
        user_id = model.data(model.index(selected_row, 0))
        current_username = model.data(model.index(selected_row, 1))
        current_email = model.data(model.index(selected_row, 2))

        dialog = QDialog(self)
        dialog.setWindowTitle("Edit User")

        layout = QFormLayout(dialog)
        username_input = QLineEdit(current_username)
        email_input = QLineEdit(current_email)

        layout.addRow("Username:", username_input)
        layout.addRow("Email:", email_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(buttons)

        def save_changes():
            new_username = username_input.text()
            new_email = email_input.text()

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("UPDATE Users SET username = ?, email = ? WHERE UserID = ?", (new_username, new_email, user_id))
            conn.commit()
            conn.close()

            self.refresh_models()
            dialog.accept()

        buttons.accepted.connect(save_changes)
        buttons.rejected.connect(dialog.reject)

        dialog.exec_()

    def create_search_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.search_combo = QComboBox()
        self.search_table = QTableView()

        search_button = QPushButton("Search Songs by Artist")
        search_button.clicked.connect(self.load_songs_by_artist)

        layout.addWidget(QLabel("Select Artist:"))
        layout.addWidget(self.search_combo)
        layout.addWidget(search_button)
        layout.addWidget(self.search_table)

        tab.setLayout(layout)
        return tab

    def on_tab_changed(self, index):
        if index == 4:  # "Search" tab index
            self.refresh_artist_names()

    def load_songs_by_artist(self):
        selected_artist = self.search_combo.currentText()

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            query = f"""
            SELECT Songs.Title, Albums.Title AS Album, Songs.Duration
            FROM Songs
            JOIN Albums ON Songs.AlbumID = Albums.AlbumID
            JOIN Artists ON Albums.ArtistID = Artists.ArtistID
            WHERE Artists.Name = '{selected_artist}';
            """

            cursor.execute(query)
            results = cursor.fetchall()
            conn.close()

            from PyQt5.QtGui import QStandardItemModel, QStandardItem
            model = QStandardItemModel()
            model.setHorizontalHeaderLabels(["Title", "Album", "Duration (sec)"])
            for row in results:
                items = [QStandardItem(str(field)) for field in row]
                model.appendRow(items)
            self.search_table.setModel(model)
            self.search_table.resizeColumnsToContents()

        except Exception as e:
            print(f"Error loading songs: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MusicLibraryApp()
    window.show()
    sys.exit(app.exec_())
