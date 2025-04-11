import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTabWidget, QTableView,
    QLabel, QPushButton, QHBoxLayout
)
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel


class MusicLibraryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Music Library")
        self.setGeometry(100, 100, 800, 600)

        self.init_db()
        self.init_ui()

    def init_db(self):
        self.db_path = "music_service.db"
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(self.db_path)
        if not self.db.open():
            print("Failed to connect to database.")
            sys.exit(1)

    def get_summary_counts(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM Songs")
            song_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM Artists")
            artist_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM Albums")
            album_count = cursor.fetchone()[0]
            conn.close()
            return song_count, artist_count, album_count
        except Exception as e:
            print(f"Error retrieving summary stats: {e}")
            return 0, 0, 0

    def init_ui(self):
        layout = QVBoxLayout()
        self.tabs = QTabWidget()

        # Main tab with summary stats
        main_tab = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setSpacing(1)
        main_layout.setContentsMargins(0, 0, 0, 0)

        song_count, artist_count, album_count = self.get_summary_counts()
        main_layout.addWidget(QLabel(f"Songs: {song_count}"))
        main_layout.addWidget(QLabel(f"Artists: {artist_count}"))
        main_layout.addWidget(QLabel(f"Albums: {album_count}"))

        main_tab.setLayout(main_layout)
        self.tabs.insertTab(0, main_tab, "Main")

        # Table views
        self.songs_view = self.create_table_view("Songs")
        self.artists_view = self.create_table_view("Artists")
        self.albums_view = self.create_table_view("Albums")
        self.users_view, users_tab = self.create_users_tab()

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
        return view

    def create_users_tab(self):
        layout = QVBoxLayout()
        self.users_model = QSqlTableModel(self)
        self.users_model.setTable("Users")
        self.users_model.select()

        users_view = QTableView()
        users_view.setModel(self.users_model)
        users_view.resizeColumnsToContents()
        self.users_view_ref = users_view  # store reference for deletion

        delete_button = QPushButton("Delete User")
        delete_button.clicked.connect(lambda: self.delete_selected_row(users_view))

        layout.addWidget(users_view)
        layout.addWidget(delete_button)

        container = QWidget()
        container.setLayout(layout)
        return users_view, container

    def delete_selected_row(self, view):
        model = view.model()
        selected_indexes = view.selectionModel().selectedRows()

        if selected_indexes:
            for index in selected_indexes:
                model.removeRow(index.row())
            if not model.submitAll():
                print("Failed to submit deletion.")
            else:
                model.select()  # Refresh view
        else:
            print("No row selected for deletion.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MusicLibraryApp()
    window.show()
    sys.exit(app.exec_())
