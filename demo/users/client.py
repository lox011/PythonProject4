from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTableWidgetItem, QMessageBox
from database.db import all_items, one_item, orders_by_user
from dialogs.order_dialog import order_dialog
from ui.client_window import Ui_ClientWindow
from users.product_card import product_card


class client_window(QMainWindow, Ui_ClientWindow):
    def __init__(self, user_id, full_name):
        super().__init__()
        self.setupUi(self)
        self.user_id = user_id
        self.images_dir = 'resources/images'

        self.labelCurrentUser.setText(f'Клиент: {full_name}')

        self.cards_widget = QWidget()
        self.cards_layout = QVBoxLayout(self.cards_widget)
        self.scrollAreaProducts.setWidget(self.cards_widget)

        self.tableWidgetOrders.setColumnCount(8)
        self.tableWidgetOrders.setHorizontalHeaderLabels([
            'ID', 'Дата', 'Товар', 'Кол-во', 'Куда', 'Адрес/место', 'Сумма', 'Статус'
        ])

        self.pushButtonRefreshProducts.clicked.connect(self.load_items)
        self.pushButtonRefreshOrders.clicked.connect(self.load_orders)
        self.pushButtonLogout.clicked.connect(self.back_to_login)

        self.load_items()
        self.load_orders()

    def clear_cards(self):
        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def load_items(self):
        self.clear_cards()
        rows = all_items()
        for row in rows:
            card = product_card(row, self.images_dir)
            card.clicked.connect(self.open_order_dialog)
            self.cards_layout.addWidget(card)
        self.statusbar.showMessage(f'Товаров: {len(rows)}')

    def open_order_dialog(self, item_id):
        item = one_item(item_id)
        if not item:
            QMessageBox.warning(self, 'Ошибка', 'Товар не найден')
            return

        dialog = order_dialog(self.user_id, item, self)
        if dialog.exec():
            self.load_orders()
            self.tabWidget.setCurrentIndex(1)

    def load_orders(self):
        rows = orders_by_user(self.user_id)
        self.tableWidgetOrders.setRowCount(len(rows))
        for i, row in enumerate(rows):
            self.tableWidgetOrders.setItem(i, 0, QTableWidgetItem(str(row['order_id'])))
            self.tableWidgetOrders.setItem(i, 1, QTableWidgetItem(str(row['order_date'])))
            self.tableWidgetOrders.setItem(i, 2, QTableWidgetItem(row['item_name']))
            self.tableWidgetOrders.setItem(i, 3, QTableWidgetItem(str(row['quantity'])))
            self.tableWidgetOrders.setItem(i, 4, QTableWidgetItem(row['delivery_type']))
            self.tableWidgetOrders.setItem(i, 5, QTableWidgetItem(row['delivery_place']))
            self.tableWidgetOrders.setItem(i, 6, QTableWidgetItem(f"{float(row['total_amount']):.2f}"))
            self.tableWidgetOrders.setItem(i, 7, QTableWidgetItem(row['status']))

    def back_to_login(self):
        from auth.auth import login_window
        self.win = login_window()
        self.win.show()
        self.close()
