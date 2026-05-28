from PyQt6.QtWidgets import QDialog, QMessageBox
from database.db import add_order
from ui.order_dialog import Ui_OrderDialog


class order_dialog(QDialog, Ui_OrderDialog):
    def __init__(self, user_id, item, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.user_id = user_id
        self.item = item

        self.labelProduct.setText(item['item_name'])

        self.comboBoxDestination.addItem('Самовывоз', 'Самовывоз')
        self.comboBoxDestination.addItem('Доставка', 'Доставка')

        self.spinBoxQuantity.valueChanged.connect(self.update_total)
        self.buttonBox.accepted.connect(self.save_order)
        self.buttonBox.rejected.connect(self.reject)
        self.update_total()

    def update_total(self):
        total = float(self.item['new_price']) * self.spinBoxQuantity.value()
        self.labelTotal.setText(f'Сумма: {total:.2f} ₽')

    def save_order(self):
        place = self.lineEditPlace.text()
        if not place:
            QMessageBox.warning(self, 'Ошибка', 'Введите адрес или место получения')
            return

        ok = add_order(
            self.user_id,
            self.item['item_id'],
            self.spinBoxQuantity.value(),
            self.comboBoxDestination.currentData(),
            place
        )
        if ok:
            self.accept()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Заказ не сохранен')
