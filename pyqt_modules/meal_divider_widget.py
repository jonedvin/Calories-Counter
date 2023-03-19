from PyQt6.QtWidgets import QPushButton, QApplication, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QMouseEvent


class MealDividerWidget(QWidget):
    def __init__(self, *args, **kwargs):
        """
        Widget for showing a meal divider bar.\n
        Example figure of bar, with dividers at 1/2 and 3/4:\n
        ====|==|=="""
        super().__init__(*args, **kwargs)

        # Bar to represent whole
        self.background = QPushButton()
        self.background.setFixedHeight(30)
        self.background.setEnabled(False)

        self.dividers = []

        # Build
        self.general_layout = QHBoxLayout()
        self.general_layout.setContentsMargins(0,10,0,10)
        self.general_layout.addWidget(self.background)
        self.setLayout(self.general_layout)

    def addDivider(self):
        """ Adds a divider. """
        new_divider = Divider(self)
        new_divider.move(self.mapToGlobal(self.pos()))
        self.dividers.append(new_divider)

    def getParts(self) -> list:
        """ Returns a list of parts, adding up to 1, """
        self.dividers.sort(key = lambda divider: divider.pos().x())
        parts = []

        # Get bar parameters
        start_x = self.mapToGlobal(self.pos()).x()
        end_x = self.mapToGlobal(self.pos()).x() + self.width()
        length = end_x - start_x

        # Add parts
        left_x = start_x
        for divider in self.dividers:
            part_x = self.mapToGlobal(divider.pos()).x()
            parts.append((part_x - left_x) / length)
            left_x = part_x
        parts.append((end_x - left_x) / length)

        for part in parts:
            print(part)

        return parts


class Divider(QPushButton):
    def __init__(self, parent: MealDividerWidget):
        """ Widget for showing a divider. Must be added to a MealDividerWidget. """
        super().__init__(parent=parent)

        self.setFixedWidth(10)
        self.setFixedHeight(40)

        self.__mouseMovePos = None

    def mousePressEvent(self, event: QMouseEvent):
        """ Overridden to save press location. """
        if event.button() == Qt.MouseButton.LeftButton:
            self.__mouseMovePos = event.globalPosition()

        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        """ Overriden to move widget with mouse if left mouse button is held down. """
        if event.buttons() == Qt.MouseButton.LeftButton:
            # Calculate new position of widget
            widgetPos = self.mapToGlobal(self.pos())
            mousePos = event.globalPosition()
            mousePosDiff = mousePos - self.__mouseMovePos
            newPos = self.mapFromGlobal(widgetPos + QPoint(int(mousePosDiff.x()), 0))

            # Move widget and save position
            self.move(newPos)
            self.__mouseMovePos = mousePos

        super().mouseMoveEvent(event)


if __name__ == "__main__":
    app = QApplication([])
    w = QWidget()
    w.resize(800,600)

    meal_divider = MealDividerWidget(w)
    meal_divider.setFixedWidth(800)
    meal_divider.addDivider()
    meal_divider.addDivider()

    button = QPushButton("Get parts", w)
    button.move(0, 200)
    button.clicked.connect(meal_divider.getParts)

    w.show()
    app.exec()
