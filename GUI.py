import sys
from PyQt5.QtWidgets import QApplication, QWidget

def main():
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("Music Database GUI")
    window.setGeometry(100, 100, 400, 300)  # x, y, width, height
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
