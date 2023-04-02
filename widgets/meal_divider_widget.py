from PyQt6.QtWidgets import QPushButton, QApplication, QWidget, QHBoxLayout, QLineEdit, QLabel, QMenu
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QMouseEvent, QResizeEvent, QMoveEvent


class DividerWidget(QWidget):
    def __init__(self, *args, width: int = 500, height: int = 30, number_of_dividers: int = 0, **kwargs):
        """
        Widget for showing a meal divider bar.\n
        Example figure of bar, with dividers at 1/2 and 3/4:\n
        ====|==|=="""
        super().__init__(*args, **kwargs)
        
        # Constants
        self.height_ = height
        self.width_ = width
        self.min_max_x = (0, self.width_)
        self.divider_width = 10

        # Adjust y-coordinate of labels if height is too low to fit them inside
        if self.height_ < 25:
            self.bottom_margin = 20
            self.part_size_y_adjustment = self.height_ - 13
        else:
            self.bottom_margin = 0
            self.part_size_y_adjustment = (self.height_ - 30)/2

        # Bar to represent whole
        self.background = QPushButton()
        self.background.setFixedHeight(self.height_)
        self.background.setEnabled(False)

        # Lists to hold dividers and part sizes
        self.dividers = []
        self.part_sizes = []

        # Build
        self.general_layout = QHBoxLayout()
        self.general_layout.setSpacing(0)
        self.general_layout.setContentsMargins(0,0,0,self.bottom_margin)
        self.general_layout.addWidget(self.background)
        self.setLayout(self.general_layout)

        self.setFixedWidth(self.width_)

        # Add one part size
        self.addPartSize()

        # Add dividers
        for _ in range(number_of_dividers):
            self.addDivider()

        self.moveEvent(QMoveEvent(self.pos(), self.pos()))

        # Signals
        # self.add_divider_button.clicked.connect(self.addDivider)


    def addDivider(self):
        """ Adds a divider. """
        new_divider = Divider(self, self.min_max_x)
        new_divider.move(QPoint(int(self.width_/2-self.divider_width/2), int(self.pos().y())))
        self.dividers.append(new_divider)
        self.addPartSize()


    def addPartSize(self):
        """ Adds a part_size. """
        self.part_sizes.append(QLabel(parent=self))
        self.part_sizes[-1].setFixedWidth(27)
        self.updatePartSizes()

        # Draw dividers on top of part labels
        if len(self.dividers) > 0:
            self.dividers[-1].raise_()

    
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

        # Get constants
        y = self.background.pos().y() + self.part_size_y_adjustment
        start_x = self.min_max_x[0]
        end_x = self.min_max_x[1] - self.divider_width
        length = end_x - start_x

        # Update part sizes
        left_x = start_x
        for i, divider in enumerate(self.dividers):
            divider_x = divider.pos().x()
            self.updateSinglePartSize(i, left_x, divider_x, y, length)
            left_x = divider_x
        self.updateSinglePartSize(-1, left_x, end_x, y, length)

    
    def updateSinglePartSize(self, index: int, left_x, right_x, y, length):
        """ Updates the part size at given index. """
        part_size = self.part_sizes[index]

        # Find new position
        left_x_plus_divider_width = left_x + self.divider_width if index != 0 else left_x
        middle_of_area_i_x = left_x_plus_divider_width + (right_x-left_x_plus_divider_width)/2
        new_pos = QPoint(int(middle_of_area_i_x-part_size.width()/2), int(y))

        # Move and update value
        part_size.move(new_pos)
        part_size.setText(str(round((right_x - left_x) / length, 2)))


    def getParts(self) -> list:
        """ Returns a list of parts, adding up to 1, """
        self.updatePartSizes()

        parts = []
        for part_size in self.part_sizes:
            parts.append(float(part_size.text()))

        return parts


class Divider(QPushButton):
    def __init__(self, parent: DividerWidget, min_max_x: tuple = None):
        """ Widget for showing a divider. Must be added to a DividerWidget. """
        super().__init__(parent=parent)

        self.setFixedWidth(parent.divider_width)
        self.setFixedHeight(int(parent.height_))

        self.__mouseMovePos = None

    
    @property
    def halfWidth(self):
        return self.width()/2


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
            if self.parent().min_max_x[0] <= newPos.x() <= self.parent().min_max_x[1] - self.parent().divider_width:
                self.move(newPos)
                self.__mouseMovePos = mousePos

                # Update part_sizes
                self.parent().updatePartSizes()

        super().mouseMoveEvent(event)


if __name__ == "__main__":
    app = QApplication([])
    w = QWidget()
    w.resize(800,600)

    meal_divider = DividerWidget(w, height=25, number_of_dividers=2)
    meal_divider.move(100, 0)

    button = QPushButton("Get parts", w)
    button.move(0, 200)
    button.clicked.connect(meal_divider.getParts)

    w.show()
    app.exec()
