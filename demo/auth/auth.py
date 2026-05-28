from PyQt6.QtWidgets import QMainWindow, QMessageBox

from database.db import check_login
from ui.mainwindow import Ui_MainWindow
from users.admin import admin_window
from users.client import client_window
from users.manager import manager_window


class login_window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.user_window = None
        self.pushButtonLogin.clicked.connect(self.login)
        self.lineEditPassword.returnPressed.connect(self.login)

    def login(self):
        username = self.lineEditLogin.text().strip()
        password = self.lineEditPassword.text().strip()
        user = check_login(username, password)

        if not user:
            QMessageBox.warning(self, 'Ошибка', 'Неверный логин или пароль')
            return

        if user['role_name'] == 'client':
            self.user_window = client_window(user['user_id'], user['full_name'])
        elif user['role_name'] == 'manager':
            self.user_window = manager_window(user['full_name'])
        elif user['role_name'] == 'admin':
            self.user_window = admin_window(user['full_name'])
        else:
            QMessageBox.warning(self, 'Ошибка', 'Неизвестная роль')
            return

        self.user_window.show()
        self.close()
