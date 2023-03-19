from PyQt6.QtWidgets import QPushButton, QApplication, QWidget, QHBoxLayout, QLineEdit, QLabel
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

        # Lists to hold dividers and part sizes
        self.dividers = []
        self.part_sizes = []

        # Add one part size
        self.addPartSize()

        # Build
        self.general_layout = QHBoxLayout()
        self.general_layout.setContentsMargins(0,10,0,50)
        self.general_layout.addWidget(self.background)
        self.setLayout(self.general_layout)


    def addDivider(self):
        """ Adds a divider. """
        new_divider = Divider(self)
        new_divider.move(self.mapToGlobal(self.pos()))
        self.dividers.append(new_divider)
        self.addPartSize()


    def addPartSize(self):
        """ Adds a part_size. """
        self.part_sizes.append(QLabel(parent=self))
        self.part_sizes[-1].setFixedWidth(40)
        self.updatePartSizes()


    def updatePartSizes(self):
        """ Updates the part sizes so that everything matches. """
        y = self.pos().y() + self.background.height()
        start_x = self.pos().x()
        end_x = self.pos().x() + self.background.width()
        length = end_x - start_x

        left_x = start_x
        for i, divider in enumerate(self.dividers):
            # Get x's
            part_x = divider.pos().x()
            middle_x = left_x + (part_x-left_x)/2

            # Update part_size
            part_size = self.part_sizes[i]
            new_pos = QPoint(int(middle_x-part_size.width()/2), int(y))
            part_size.move(new_pos)
            part_size.setText(str(round((part_x - left_x) / length, 2)))
            
            left_x = part_x

        # Last one
        middle_x = left_x + (end_x-left_x)/2
        part_size = self.part_sizes[-1]
        new_pos = QPoint(int(middle_x), int(y))
        part_size.move(new_pos)
        part_size.setText(str(round((end_x - left_x) / length, 2)))


    def getParts(self) -> list:
        """ Returns a list of parts, adding up to 1, """
        self.dividers.sort(key = lambda divider: divider.pos().x())
        parts = []

        # Get bar parameters
        start_x = self.mapToGlobal(self.pos()).x()
        end_x = self.mapToGlobal(self.pos()).x() + self.background.width()
        length = end_x - start_x

        # Add parts
        left_x = start_x
        for divider in self.dividers:
            part_x = self.mapToGlobal(divider.pos()).x()
            parts.append((part_x - left_x) / length)
            left_x = part_x
        parts.append(round((end_x - left_x) / length, 2))

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

            # Update part_sizes
            self.parent().updatePartSizes()

        super().mouseMoveEvent(event)

    
class PartSize(QLineEdit):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setFixedWidth(40)


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
