from PyQt6.QtWidgets import QPushButton, QApplication, QWidget, QHBoxLayout, QLabel, QMenu
from PyQt6.QtCore import Qt, QPoint, pyqtSignal
from PyQt6.QtGui import QMouseEvent, QMoveEvent


class DividerWidget(QWidget):
    # Custom signals
    divisionChanged = pyqtSignal(tuple)

    def __init__(self, *args,
                       width: int = 500,
                       height: int = 30,
                       number_of_dividers: int = 0,
                       min_dividers: int = 0,
                       show_buttons: bool = False,
                       **kwargs):
        """
        Widget for showing a meal divider bar.\n
        Example figure of bar, with dividers at 1/2 and 3/4:\n
        ====|==|=="""
        super().__init__(*args, **kwargs)
        
        # Constants
        self.height_ = height
        self.width_ = width
        self.show_buttons = show_buttons
        self.min_dividers = min_dividers
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
        self.background.setFixedWidth(self.width_)

        # Buttons for removing and adding dividers
        self.remove_divider_button = QPushButton("-")
        self.remove_divider_button.setFixedHeight(self.height_)
        self.remove_divider_button.setFixedWidth(self.height_)
        self.add_divider_button = QPushButton("+")
        self.add_divider_button.setFixedHeight(self.height_)
        self.add_divider_button.setFixedWidth(self.height_)

        # Lists to hold dividers and part sizes
        self.dividers = []
        self.part_sizes = []

        # Build
        self.general_layout = QHBoxLayout()
        self.general_layout.setSpacing(0)
        self.general_layout.setContentsMargins(0,0,0,self.bottom_margin)
        if show_buttons:
            self.general_layout.addWidget(self.remove_divider_button)
            self.general_layout.addWidget(self.add_divider_button)
        self.general_layout.addWidget(self.background)
        self.setLayout(self.general_layout)

        if show_buttons:
            self.setFixedWidth(2*self.height_+self.width_)
        else:
            self.setFixedWidth(self.width_)

        # Add one part size
        self.addPartSize()

        # Add dividers
        for _ in range(number_of_dividers):
            self.addDivider()

        self.moveEvent(QMoveEvent(self.pos(), self.pos()))

        # Signals
        self.add_divider_button.clicked.connect(self.addDivider)
        self.remove_divider_button.clicked.connect(self.deleteDivider)


    def getMinMaxX(self):
        """ Returns a tuple with the minimum and maximum allowed x values for the dividers. """
        min = 0
        max = self.width_

        if self.show_buttons:
            min += 2*self.height_
            max += 2*self.height_

        return (min, max)


    def addDivider(self):
        """ Adds a divider. """
        x = self.getMinMaxX()[0] + (self.getMinMaxX()[1] - self.getMinMaxX()[0])/2 - self.divider_width/2
        y = self.background.pos().y()

        new_divider = Divider(self)
        new_divider.move(QPoint(int(x), int(y)))
        new_divider.setVisible(True)

        self.dividers.append(new_divider)
        self.addPartSize()

    
    def deleteDivider(self):
        """ Deletes the given divider. """
        if len(self.dividers) <= self.min_dividers:
            return
        
        divider = self.dividers.pop(-1)
        divider.close()
        part_size = self.part_sizes.pop(-1)
        part_size.close()
        self.updatePartSizes()


    def addPartSize(self):
        """ Adds a part_size. """
        self.part_sizes.append(QLabel(parent=self))
        self.part_sizes[-1].setFixedWidth(27)
        self.part_sizes[-1].setVisible(True)
        self.updatePartSizes()

        # Draw dividers on top of part labels
        if len(self.dividers) > 0:
            self.dividers[-1].raise_()


    def updatePartSizes(self):
        """ Updates the part sizes so that everything matches. """
        self.dividers.sort(key = lambda divider: divider.pos().x())

        # Get constants
        y = self.background.pos().y() + self.part_size_y_adjustment
        start_x = self.getMinMaxX()[0]
        end_x = self.getMinMaxX()[1] - self.divider_width
        length = end_x - start_x

        # Update part sizes
        left_x = start_x
        for i, divider in enumerate(self.dividers):
            divider_x = divider.pos().x()
            self.updateSinglePartSize(i, left_x, divider_x, y, length)
            left_x = divider_x
        self.updateSinglePartSize(-1, left_x, end_x, y, length)

        # Emit signal that part sizes changed
        self.divisionChanged.emit(self.getAllDividerXs())

    
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

    
    def getAllDividerXs(self) -> tuple:
        """ Returns a tuple of all divider x-positions. """
        list = []
        x_adjustment = 0 if not self.show_buttons else 2*self.height_
        for divider in self.dividers:
            list.append(divider.pos().x()-x_adjustment)
        return tuple(list)

    
    def setAllDividerXs(self, x_positions: tuple):
        """ Sets all dividers to given x-positions and updates part sizes. """
        if len(x_positions) != len(self.dividers):
            return

        x_adjustment = 0 if not self.show_buttons else 2*self.height_
        for i in range(len(x_positions)):
            self.dividers[i].move(QPoint(x_positions[i]+x_adjustment, self.dividers[i].pos().y()))

        self.updatePartSizes()


    def getParts(self) -> list:
        """ Returns a list of parts, adding up to 1, """
        self.updatePartSizes()

        parts = []
        for part_size in self.part_sizes:
            parts.append(float(part_size.text()))

        return parts


class Divider(QPushButton):
    def __init__(self, parent: DividerWidget):
        """ Widget for showing a divider. Must be added to a DividerWidget. """
        super().__init__(parent=parent)

        self.setFixedWidth(parent.divider_width)
        self.setFixedHeight(int(parent.height_))

        self.__mouseMovePos = None


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
            if self.parent().getMinMaxX()[0] <= newPos.x() <= self.parent().getMinMaxX()[1] - self.parent().divider_width:
                self.move(newPos)
                self.__mouseMovePos = mousePos

                # Update part_sizes
                self.parent().updatePartSizes()

        super().mouseMoveEvent(event)


if __name__ == "__main__":
    app = QApplication([])
    w = QWidget()
    w.resize(800,600)

    meal_divider = DividerWidget(w, height=25, number_of_dividers=0, show_buttons=True)
    meal_divider.move(100, 0)

    button = QPushButton("Get parts", w)
    button.move(0, 200)
    button.clicked.connect(meal_divider.getParts)

    w.show()
    app.exec()
