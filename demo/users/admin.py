from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from database.db import (
    all_items, items_by_category, search_items, items_sorted,
    all_categories, all_orders, one_item, one_order,
    delete_item, delete_order
)
from dialogs.product_dialog import product_dialog
from dialogs.admin_order_dialog import admin_order_dialog
from ui.admin_window import Ui_AdminWindow


class admin_window(QMainWindow, Ui_AdminWindow):
    def __init__(self, full_name):
        super().__init__()
        self.setupUi(self)
        self.selected_item_id = None
        self.selected_order_id = None

        self.labelCurrentUser.setText(f'Администратор: {full_name}')

        self.comboBoxCategory.addItem('Все категории', None)
        for row in all_categories():
            self.comboBoxCategory.addItem(row['category_name'], row['category_name'])

        self.comboBoxSort.addItems(['Цена', 'Название'])

        self.tableWidgetProducts.setColumnCount(8)
        self.tableWidgetProducts.setHorizontalHeaderLabels([
            'ID', 'Название', 'Описание', 'Цена', 'Новая цена', 'Категория', 'Картинка', 'Скидка'
        ])
        self.tableWidgetProducts.cellClicked.connect(self.select_item)

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
        self.pushButtonAddProduct.clicked.connect(self.add_item)
        self.pushButtonEditProduct.clicked.connect(self.edit_item)
        self.pushButtonDeleteProduct.clicked.connect(self.delete_item)

        self.pushButtonRefreshOrders.clicked.connect(self.load_orders)
        self.pushButtonAddOrder.clicked.connect(self.add_order)
        self.pushButtonEditOrder.clicked.connect(self.edit_order)
        self.pushButtonDeleteOrder.clicked.connect(self.delete_order)
        self.pushButtonLogout.clicked.connect(self.back_to_login)

        self.load_items()
        self.load_orders()

    def show_items(self, rows):
        self.tableWidgetProducts.setRowCount(len(rows))
        for i, row in enumerate(rows):
            discount = row.get('discount_percent')
            if discount:
                discount_text = f"{discount}% до {row['date_end']}"
            else:
                discount_text = ''
            self.tableWidgetProducts.setItem(i, 0, QTableWidgetItem(str(row['item_id'])))
            self.tableWidgetProducts.setItem(i, 1, QTableWidgetItem(row['item_name']))
            self.tableWidgetProducts.setItem(i, 2, QTableWidgetItem(row.get('description') or ''))
            self.tableWidgetProducts.setItem(i, 3, QTableWidgetItem(f"{float(row['price']):.2f}"))
            self.tableWidgetProducts.setItem(i, 4, QTableWidgetItem(f"{float(row['new_price']):.2f}"))
            self.tableWidgetProducts.setItem(i, 5, QTableWidgetItem(row.get('category') or ''))
            self.tableWidgetProducts.setItem(i, 6, QTableWidgetItem(row.get('image') or ''))
            self.tableWidgetProducts.setItem(i, 7, QTableWidgetItem(discount_text))
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

    def select_item(self, row):
        self.selected_item_id = int(self.tableWidgetProducts.item(row, 0).text())

    def add_item(self):
        dialog = product_dialog()
        if dialog.exec():
            self.reload_categories()
            self.load_items()

    def edit_item(self):
        if not self.selected_item_id:
            QMessageBox.warning(self, 'Ошибка', 'Выберите товар в таблице')
            return

        item = one_item(self.selected_item_id)
        dialog = product_dialog(item)
        if dialog.exec():
            self.reload_categories()
            self.load_items()

    def delete_item(self):
        if not self.selected_item_id:
            QMessageBox.warning(self, 'Ошибка', 'Выберите товар в таблице')
            return

        ok = delete_item(self.selected_item_id)
        if ok:
            self.selected_item_id = None
            self.reload_categories()
            self.load_items()
            self.load_orders()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Товар не удален')

    def reload_categories(self):
        self.comboBoxCategory.clear()
        self.comboBoxCategory.addItem('Все категории', None)
        for row in all_categories():
            self.comboBoxCategory.addItem(row['category_name'], row['category_name'])

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

    def add_order(self):
        dialog = admin_order_dialog()
        if dialog.exec():
            self.load_orders()

    def edit_order(self):
        if not self.selected_order_id:
            QMessageBox.warning(self, 'Ошибка', 'Выберите заказ в таблице')
            return

        order = one_order(self.selected_order_id)
        dialog = admin_order_dialog(order)
        if dialog.exec():
            self.load_orders()

    def delete_order(self):
        if not self.selected_order_id:
            QMessageBox.warning(self, 'Ошибка', 'Выберите заказ в таблице')
            return

        ok = delete_order(self.selected_order_id)
        if ok:
            self.selected_order_id = None
            self.load_orders()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Заказ не удален')

    def back_to_login(self):
        from auth.auth import login_window
        self.win = login_window()
        self.win.show()
        self.close()
