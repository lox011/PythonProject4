from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTableWidgetItem, QMessageBox
from database.db import (
    all_items, items_by_category, search_items, items_sorted,
    all_categories, all_orders, update_order_status
)
from ui.manager_window import Ui_ManagerWindow
from users.product_card import product_card


class manager_window(QMainWindow, Ui_ManagerWindow):
    def __init__(self, full_name):
        super().__init__()
        self.setupUi(self)
        self.images_dir = 'resources/images'
        self.selected_order_id = None

        self.labelCurrentUser.setText(f'Менеджер: {full_name}')

        self.cards_widget = QWidget()
        self.cards_layout = QVBoxLayout(self.cards_widget)
        self.scrollAreaProducts.setWidget(self.cards_widget)

        self.comboBoxCategory.addItem('Все категории', None)
        for row in all_categories():
            self.comboBoxCategory.addItem(row['category_name'], row['category_name'])

        self.comboBoxSort.addItems(['Цена', 'Название'])

        self.comboBoxStatus.addItem('Новый', 'Новый')
        self.comboBoxStatus.addItem('В работе', 'В работе')
        self.comboBoxStatus.addItem('Готов', 'Готов')
        self.comboBoxStatus.addItem('Выдан', 'Выдан')
        self.comboBoxStatus.addItem('Отменен', 'Отменен')

        self.tableWidgetOrders.setColumnCount(9)
        self.tableWidgetOrders.setHorizontalHeaderLabels([
            'ID', 'Дата', 'Клиент', 'Товар', 'Кол-во', 'Куда', 'Адрес/место', 'Сумма', 'Статус'
        ])
        self.tableWidgetOrders.cellClicked.connect(self.select_order)

        self.pushButtonRefreshProducts.clicked.connect(self.load_items)
        self.pushButtonSearch.clicked.connect(self.search_items)
        self.pushButtonFilter.clicked.connect(self.filter_items)
        self.pushButtonSortUp.clicked.connect(self.sort_up)
        self.pushButtonSortDown.clicked.connect(self.sort_down)
        self.pushButtonRefreshOrders.clicked.connect(self.load_orders)
        self.pushButtonChangeStatus.clicked.connect(self.change_status)
        self.pushButtonLogout.clicked.connect(self.back_to_login)

        self.load_items()
        self.load_orders()

    def clear_cards(self):
        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def show_items(self, rows):
        self.clear_cards()
        for row in rows:
            card = product_card(row, self.images_dir)
            self.cards_layout.addWidget(card)
        self.statusbar.showMessage(f'Товаров: {len(rows)}')

    def load_items(self):
        self.show_items(all_items())

    def search_items(self):
        self.show_items(search_items(self.lineEditSearch.text()))

    def filter_items(self):
        category = self.comboBoxCategory.currentData()
        if category:
            rows = items_by_category(category)
        else:
            rows = all_items()
        self.show_items(rows)

    def sort_up(self):
        self.show_items(items_sorted(self.comboBoxSort.currentText(), 'ASC'))

    def sort_down(self):
        self.show_items(items_sorted(self.comboBoxSort.currentText(), 'DESC'))

    def load_orders(self):
        rows = all_orders()
        self.tableWidgetOrders.setRowCount(len(rows))
        for i, row in enumerate(rows):
            self.tableWidgetOrders.setItem(i, 0, QTableWidgetItem(str(row['order_id'])))
            self.tableWidgetOrders.setItem(i, 1, QTableWidgetItem(str(row['order_date'])))
            self.tableWidgetOrders.setItem(i, 2, QTableWidgetItem(row['client_name']))
            self.tableWidgetOrders.setItem(i, 3, QTableWidgetItem(row['item_name']))
            self.tableWidgetOrders.setItem(i, 4, QTableWidgetItem(str(row['quantity'])))
            self.tableWidgetOrders.setItem(i, 5, QTableWidgetItem(row['delivery_type']))
            self.tableWidgetOrders.setItem(i, 6, QTableWidgetItem(row['delivery_place']))
            self.tableWidgetOrders.setItem(i, 7, QTableWidgetItem(f"{float(row['total_amount']):.2f}"))
            self.tableWidgetOrders.setItem(i, 8, QTableWidgetItem(row['status']))

    def select_order(self, row):
        self.selected_order_id = int(self.tableWidgetOrders.item(row, 0).text())

    def change_status(self):
        if not self.selected_order_id:
            QMessageBox.warning(self, 'Ошибка', 'Выберите заказ в таблице')
            return

        ok = update_order_status(self.selected_order_id, self.comboBoxStatus.currentData())
        if ok:
            self.load_orders()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Статус не изменен')

    def back_to_login(self):
        from auth.auth import login_window
        self.win = login_window()
        self.win.show()
        self.close()