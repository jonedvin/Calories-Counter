from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem
from widgets.base_widget import BaseWidget
from gui.divide_meal_gui import DivideMealWidget
from modules.databaser import Databaser
from modules.txter import Txter


class MadeMealsWidget(BaseWidget):
    def __init__(self, mainWindow, databaser: Databaser, txter: Txter, *args, **kwargs):
        """ Widget with components for viewing, throwing away and eating made meals. """
        super().__init__(mainWindow, *args, **kwargs)

        self.databaser = databaser
        self.txter = txter

        # Meals tree
        self.meals_tree = QTreeWidget()
        self.meals_tree.setColumnWidth(0, 200)
        self.meals_tree.setHeaderLabels(["Meals"])
        self.meals_tree.setIndentation(0)
        self.reload()

        # Bottom section
        self.throw_away_button = QPushButton("Throw away meal")
        self.divide_meal_button = QPushButton("Divide meal")
        self.button_section = QHBoxLayout()
        self.button_section.addWidget(self.throw_away_button)
        self.button_section.addStretch()
        self.button_section.addWidget(self.divide_meal_button)

        # Build widget
        self.general_layout = QVBoxLayout()
        self.general_layout.addWidget(self.meals_tree)
        self.general_layout.addLayout(self.button_section)
        self.setLayout(self.general_layout)

        # Signals
        self.throw_away_button.clicked.connect(self.delete_meal)
        self.divide_meal_button.clicked.connect(self.open_divide_meal_window)

    
    def reload(self):
        self.txter.populate_meals_tree(self.meals_tree, self.mainWindow.ingredients)


    def delete_meal(self):
        """ Removed the selected meal from made meals. """
        self.txter.remove_meal(self.meals_tree.currentItem().to_string())
        self.meals_tree.invisibleRootItem().removeChild(self.meals_tree.currentItem())


    def open_divide_meal_window(self):
        """ Opens a window to divide the selected meal. """
        if not self.meals_tree.currentItem():
            print("Please select an item first.")
            return
        
        self.setAllEnabled(False)
        self.meal_divider_popup = DivideMealWidget(self.mainWindow, self, self.meals_tree.currentItem(), self.txter)
        self.meal_divider_popup.show()
