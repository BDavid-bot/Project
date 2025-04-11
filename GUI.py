import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTabWidget, QTableView, QLabel
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
        main_layout.setContentsMargins(0,0,0,0)

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

        self.tabs.addTab(self.songs_view, "Songs")
        self.tabs.addTab(self.artists_view, "Artists")
        self.tabs.addTab(self.albums_view, "Albums")

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MusicLibraryApp()
    window.show()
    sys.exit(app.exec_())
