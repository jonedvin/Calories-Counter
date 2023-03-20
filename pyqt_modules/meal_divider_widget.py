from PyQt6.QtWidgets import QPushButton, QApplication, QWidget, QHBoxLayout, QLineEdit, QLabel, QMenu
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QMouseEvent, QResizeEvent, QMoveEvent


class MealDividerWidget(QWidget):
    def __init__(self, *args, height: int = 30, **kwargs):
        """
        Widget for showing a meal divider bar.\n
        Example figure of bar, with dividers at 1/2 and 3/4:\n
        ====|==|=="""
        super().__init__(*args, **kwargs)
        
        self.height_ = height

        # Bar to represent whole
        self.background = QPushButton()
        self.background.setFixedHeight(height)
        self.background.setEnabled(False)

        # Lists to hold dividers and part sizes
        self.dividers = []
        self.part_sizes = []

        # Add one part size
        self.addPartSize()

        # Build
        self.general_layout = QHBoxLayout()
        self.general_layout.setSpacing(5)
        self.general_layout.setContentsMargins(0,0,0,20)
        self.general_layout.addWidget(self.background)
        self.setLayout(self.general_layout)

        # Signals
        # self.add_divider_button.clicked.connect(self.addDivider)

    
    def resizeEvent(self, event: QResizeEvent):
        """ Overridden to update Divider limits. """
        min_max_x = (self.pos().x(), self.pos().x()+event.size().width())
        for divider in self.dividers:
            divider.update_min_max_x(min_max_x)
        return super().resizeEvent(event)
    

    def moveEvent(self, event: QMoveEvent):
        """ Overridden to update Divider limits. """
        min_max_x = (event.pos().x(), event.pos().x()+self.width())
        for divider in self.dividers:
            divider.update_min_max_x(min_max_x)
        return super().moveEvent(event)


    def addDivider(self):
        """ Adds a divider. """
        # Get spawn point
        y = self.pos().y()
        start_x = self.pos().x()
        end_x = self.pos().x() + self.background.width()
        spawn_point = QPoint(int((end_x-start_x)/2), int(y))

        # Spawn divider and part_size
        new_divider = Divider(self)
        new_divider.move(spawn_point)
        new_divider.setVisible(True)
        self.dividers.append(new_divider)
        self.addPartSize()


    def addPartSize(self):
        """ Adds a part_size. """
        self.part_sizes.append(QLabel(parent=self))
        self.part_sizes[-1].setFixedWidth(40)
        self.part_sizes[-1].setVisible(True)
        self.updatePartSizes()

    
    def deleteDivider(self, divider):
        """ Deletes the given divider. """
        self.dividers.remove(divider)
        divider.close()
        part_size = self.part_sizes.pop(0)
        part_size.close()
        self.updatePartSizes()


    def updatePartSizes(self):
        """ Updates the part sizes so that everything matches. """
        self.dividers.sort(key = lambda divider: divider.pos().x())

        y = self.pos().y() + self.background.height()*4/5
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
        self.updatePartSizes()

        parts = []
        for part_size in self.part_sizes:
            parts.append(float(part_size.text()))

        return parts


class Divider(QPushButton):
    def __init__(self, parent: MealDividerWidget):
        """ Widget for showing a divider. Must be added to a MealDividerWidget. """
        super().__init__(parent=parent)

        self.setFixedWidth(10)
        self.setFixedHeight(int(parent.height_*4/3))

        self.min_man_x = (parent.pos().x(), parent.pos().x()+parent.width())
        self.__mouseMovePos = None

    
    def update_min_max_x(self, min_max_x: tuple):
        """ Updates the min and max x-values allowed. """
        # Scale !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.min_man_x = min_max_x


    def contextMenuEvent(self, event):
        """ Overridden function. Adds option to delete divider. """
        contextMenu = QMenu(self)
        deleteDivider = contextMenu.addAction("Delete")
        action = contextMenu.exec(self.mapToGlobal(event.pos()))
        if action == deleteDivider:
            self.parent().deleteDivider(self)


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
            if self.min_man_x[0] <= newPos.x() <= self.min_man_x[1]:
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

    meal_divider = MealDividerWidget(w, height=30)
    meal_divider.setFixedWidth(800)
    meal_divider.addDivider()
    meal_divider.addDivider()

    button = QPushButton("Get parts", w)
    button.move(0, 200)
    button.clicked.connect(meal_divider.getParts)

    w.show()
    app.exec()
