from PyQt6.QtWidgets import QPushButton, QApplication, QWidget
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QMouseEvent


class DragButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__mousePressPos = None
        self.__mouseMovePos = None

    def mousePressEvent(self, event: QMouseEvent):
        """ Overridden to save press location. """
        if event.button() == Qt.MouseButton.LeftButton:
            self.__mousePressPos = event.globalPosition()
            self.__mouseMovePos = event.globalPosition()

        return super(DragButton, self).mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        """ Overriden to move widget with mouse if left mouse button is held down. """
        if event.buttons() == Qt.MouseButton.LeftButton:
            # Calculate new position of widget
            widgetPos = self.mapToGlobal(self.pos())
            mousePos = event.globalPosition()
            mousePosDiff = mousePos - self.__mouseMovePos
            newPos = self.mapFromGlobal(widgetPos + QPoint(int(mousePosDiff.x()), int(mousePosDiff.y())))
            self.move(newPos)

            self.__mouseMovePos = mousePos

        super(DragButton, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        """ Overridden to not click when moved"""
        if self.__mousePressPos is not None:
            moved = event.globalPosition() - self.__mousePressPos 
            if moved.manhattanLength() > 3:
                event.ignore()
                return

        super(DragButton, self).mouseReleaseEvent(event)

def clicked():
    print("click as normal!")

if __name__ == "__main__":
    app = QApplication([])
    w = QWidget()
    w.resize(800,600)

    button = DragButton("Drag", w)
    button.clicked.connect(clicked)
    button.setEnabled(False)

    w.show()
    app.exec()
