from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QMessageBox, QDialog

from database.db import all_categories, add_item, edit_item, save_discount
from ui.product_dialog import Ui_ProductDialog


class product_dialog(QDialog, Ui_ProductDialog):
    def __init__(self, item=None):
        super().__init__()
        self.setupUi(self)
        self.item = item
        self.dateEditDiscount.setDate(QDate.currentDate().addDays(14))

        for row in all_categories():
            self.comboBoxCategory.addItem(row['category_name'])

        if item:
            self.lineEditName.setText(item['item_name'])
            self.plainTextEditDescription.setPlainText(item.get('description') or '')
            self.doubleSpinBoxPrice.setValue(float(item['price']))
            self.lineEditImage.setText(item.get('image') or '')
            self.comboBoxCategory.setCurrentText(item.get('category') or '')
            self.spinBoxDiscount.setValue(int(item.get('discount_percent') or 0))
            date_end = item.get('date_end')
            if date_end:
                date = QDate.fromString(str(date_end), 'yyyy-MM-dd')
                if date.isValid():
                    self.dateEditDiscount.setDate(date)

        self.buttonBox.accepted.connect(self.save_item)
        self.buttonBox.rejected.connect(self.reject)

    def save_item(self):
        name = self.lineEditName.text().strip()
        category = self.comboBoxCategory.currentText().strip()
        price = self.doubleSpinBoxPrice.value()
        image = self.lineEditImage.text().strip()
        discount = self.spinBoxDiscount.value()
        date_end = self.dateEditDiscount.date().toString('yyyy-MM-dd')

        if not name or not category or price <= 0:
            QMessageBox.warning(self, 'Ошибка', 'Введите название, категорию и цену')
            return

        if image == '':
            image = None

        if self.item:
            ok = edit_item(
                self.item['item_id'],
                name,
                self.plainTextEditDescription.toPlainText(),
                price,
                category,
                image
            )
            if ok:
                save_discount(self.item['item_id'], discount, date_end)
        else:
            item_id = add_item(
                name,
                self.plainTextEditDescription.toPlainText(),
                price,
                category,
                image
            )
            ok = item_id is not None
            if ok:
                save_discount(item_id, discount, date_end)

        if ok:
            self.accept()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Товар не сохранен')
