from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class Widget(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def mousePressEvent(self, event: QMouseEvent):
        """ Overridden to save press location. """
        print(event.pos())


if __name__ == "__main__":
    app = QApplication([])
    w = QWidget()
    w.resize(800,600)

    widget = Widget(w)
    canvas = QPixmap(400, 300)
    canvas.fill(QColor("#ffffff"))
    widget.setPixmap(canvas)
    widget.move(100, 100)

    label = QLabel("0.00", w)
    label.setFixedWidth(27)
    label.move(100, 100)
    print(label.pos().x()+label.width()/2)

    w.show()
    app.exec()
