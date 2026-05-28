from PyQt6.QtWidgets import QDialog, QMessageBox
from database.db import (
    all_clients, all_items,
    add_order, edit_order
)
from ui.admin_order_dialog import Ui_AdminOrderDialog


class admin_order_dialog(QDialog, Ui_AdminOrderDialog):
    def __init__(self, order=None):
        super().__init__()
        self.setupUi(self)
        self.order = order
        self.items = all_items()

        for row in all_clients():
            self.comboBoxClient.addItem(row['full_name'], row['user_id'])
        for row in self.items:
            self.comboBoxProduct.addItem(row['item_name'], row['item_id'])
        self.comboBoxDestination.addItem('Самовывоз', 'Самовывоз')
        self.comboBoxDestination.addItem('Доставка', 'Доставка')

        self.comboBoxStatus.addItem('Новый', 'Новый')
        self.comboBoxStatus.addItem('В работе', 'В работе')
        self.comboBoxStatus.addItem('Готов', 'Готов')
        self.comboBoxStatus.addItem('Выдан', 'Выдан')
        self.comboBoxStatus.addItem('Отменен', 'Отменен')

        if order:
            self.comboBoxClient.setCurrentIndex(self.comboBoxClient.findData(order['user_id']))
            self.comboBoxProduct.setCurrentIndex(self.comboBoxProduct.findData(order['item_id']))
            self.spinBoxQuantity.setValue(order['quantity'])
            self.comboBoxDestination.setCurrentIndex(self.comboBoxDestination.findData(order['delivery_type']))
            self.lineEditPlace.setText(order['delivery_place'])
            self.comboBoxStatus.setCurrentIndex(self.comboBoxStatus.findData(order['status']))

        self.comboBoxProduct.currentIndexChanged.connect(self.update_total)
        self.spinBoxQuantity.valueChanged.connect(self.update_total)
        self.buttonBox.accepted.connect(self.save_order)
        self.buttonBox.rejected.connect(self.reject)
        self.update_total()

    def current_price(self):
        item_id = self.comboBoxProduct.currentData()
        for item in self.items:
            if item['item_id'] == item_id:
                return float(item['new_price'])
        return 0

    def update_total(self):
        total = self.current_price() * self.spinBoxQuantity.value()
        self.labelTotal.setText(f'Сумма: {total:.2f} ₽')

    def save_order(self):
        place = self.lineEditPlace.text()
        if not place:
            QMessageBox.warning(self, 'Ошибка', 'Введите адрес или место получения')
            return

        if self.order:
            ok = edit_order(
                self.order['order_id'],
                self.comboBoxClient.currentData(),
                self.comboBoxProduct.currentData(),
                self.spinBoxQuantity.value(),
                self.comboBoxDestination.currentData(),
                place,
                self.comboBoxStatus.currentData()
            )
        else:
            ok = add_order(
                self.comboBoxClient.currentData(),
                self.comboBoxProduct.currentData(),
                self.spinBoxQuantity.value(),
                self.comboBoxDestination.currentData(),
                place,
                self.comboBoxStatus.currentData()
            )

        if ok:
            self.accept()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Заказ не сохранен')
