import sys
from PyQt6.QtWidgets import QApplication
from auth.auth import login_window

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = login_window()
    window.show()
    sys.exit(app.exec())
