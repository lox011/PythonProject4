import os
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFrame, QLabel, QHBoxLayout


class product_card(QFrame):
    clicked = pyqtSignal(int)

    def __init__(self, item, images_dir):
        super().__init__()
        self.item_id = item['item_id']
        self.setMinimumHeight(130)

        layout = QHBoxLayout(self)

        self.label_photo = QLabel()
        self.label_photo.setFixedSize(140, 110)
        self.label_photo.setScaledContents(True)
        self.label_photo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        image_name = item.get('image')
        image_path = f'{images_dir}/{image_name}'
        if image_name and os.path.exists(image_path):
            self.label_photo.setPixmap(QPixmap(image_path))
        else:
            self.label_photo.setText('Нет фото')

        price = float(item['price'])
        new_price = float(item.get('new_price') or item['price'])
        discount = item.get('discount_percent')

        if discount:
            price_text = f"<s>{price:.2f} ₽</s> {new_price:.2f} ₽"
            discount_text = f"{discount}%<br>до {item['date_end']}"
        else:
            price_text = f"{price:.2f} ₽"
            discount_text = 'Без скидки'

        self.label_info = QLabel()
        self.label_info.setText(
            f"<b>{item['item_name']}</b><br>"
            f"{item.get('category') or ''}<br>"
            f"{item.get('description') or ''}<br><br>"
            f"{price_text}"
        )
        self.label_info.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self.label_discount = QLabel()
        self.label_discount.setText(discount_text)
        self.label_discount.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_discount.setFixedWidth(120)

        layout.addWidget(self.label_photo)
        layout.addWidget(self.label_info)
        layout.addWidget(self.label_discount)

    def mousePressEvent(self, event):
        self.clicked.emit(self.item_id)
        super().mousePressEvent(event)
