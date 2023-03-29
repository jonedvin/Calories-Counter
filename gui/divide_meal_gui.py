from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem
from widgets.base_widget import BaseWidget
from modules.txter import Txter


class DivideMealWidget(BaseWidget):
    WindowWidth = 500
    WindowHeight = 600

    def __init__(self, mainWindow, parent_, meal_string, txter: Txter, *args, **kwargs):
        """ Widget with components for viewing and throwing away made meals. """
        super().__init__(mainWindow, *args, **kwargs)

        self.setFixedSize(self.WindowWidth, self.WindowHeight)
        self.parent_ = parent_
        self.txter = txter

        # Meals tree
        self.ingredients_tree = QTreeWidget()
        self.ingredients_tree.setColumnCount(3)
        self.ingredients_tree.setHeaderLabels(["Ingredient", "Amount", "Division"])
        self.populate_ingredients_tree(meal_string)
        for item in (self.ingredients_tree.topLevelItem(i) for i in range(self.ingredients_tree.topLevelItemCount())):
            pass

        # Button strip
        self.cancel_button = QPushButton("Cancel")
        self.divide_meal_button = QPushButton("Divide meal")
        self.button_section = QHBoxLayout()
        self.button_section.addStretch()
        self.button_section.addWidget(self.cancel_button)
        self.button_section.addWidget(self.divide_meal_button)

        # Build widget
        self.general_layout = QVBoxLayout()
        self.general_layout.addWidget(self.ingredients_tree)
        self.general_layout.addLayout(self.button_section)
        self.setLayout(self.general_layout)

        # Signals
        self.cancel_button.clicked.connect(self.close)
        self.divide_meal_button.clicked.connect(self.divide_meal)

    
    def populate_ingredients_tree(self, meal_string: str):
        """ Populates the ingredients tree. """
        meal_name = meal_string.split("-")[0]
        self.setWindowTitle(f"Divide {meal_name}")


    def divide_meal(self):
        """ Removed the selected meal from made meals. """
        pass
        self.close()
        
    
    def closeEvent(self, event):
        """ Overridden to re-enable the main GUI when closed. """
        self.parent_.setAllEnabled(True)
        return super().closeEvent(event)
        
        