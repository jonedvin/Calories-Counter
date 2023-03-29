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
        self.populate_meals_tree()
        # NOTE: The meal_string for each meal is held in QTreeWidgetItem.text(1)

        # Bottom section
        self.reload_button = QPushButton("Reload")
        self.throw_away_button = QPushButton("Throw away meal")
        self.divide_meal_button = QPushButton("Divide meal")
        self.button_section = QHBoxLayout()
        self.button_section.addWidget(self.reload_button)
        self.button_section.addWidget(self.throw_away_button)
        self.button_section.addStretch()
        self.button_section.addWidget(self.divide_meal_button)

        # Build widget
        self.general_layout = QVBoxLayout()
        self.general_layout.addWidget(self.meals_tree)
        self.general_layout.addLayout(self.button_section)
        self.setLayout(self.general_layout)

        # Signals
        self.reload_button.clicked.connect(self.populate_meals_tree)
        self.throw_away_button.clicked.connect(self.delete_meal)
        self.divide_meal_button.clicked.connect(self.open_divide_meal_window)

    
    def populate_meals_tree(self):
        """ Clears the meal tree, and re-populates it. """
        # Clear tree
        while self.meals_tree.topLevelItemCount() > 0:
            self.meals_tree.takeTopLevelItem(0)

        # Get made meals
        made_meals = self.txter.get_meals()
        for meal, meal_string, nutrients in made_meals:
            desc = f"{meal}:"
            desc += f"\n - Calories: {round(nutrients['calories'], 2)}"
            desc += f"\n - Fat: {round(nutrients['fat'], 2)}"
            desc += f"\n - '- of which saturated: {round(nutrients['saturated_fat'], 2)}"
            desc += f"\n - Carbohydrates: {round(nutrients['carbohydrates'], 2)}"
            desc += f"\n - '- of which sugar: {round(nutrients['sugar'], 2)}"
            desc += f"\n - Protein: {round(nutrients['protein'], 2)}"
            desc += f"\n - Salt: {round(nutrients['salt'], 2)}"
            desc += "\n"

            item = QTreeWidgetItem()
            item.setText(0, desc)
            item.setText(1, meal_string)
            self.meals_tree.addTopLevelItem(item)


    def delete_meal(self):
        """ Removed the selected meal from made meals. """
        self.txter.remove_meal(self.meals_tree.currentItem().text(1))
        self.meals_tree.invisibleRootItem().removeChild(self.meals_tree.currentItem())

    def open_divide_meal_window(self):
        """ Opens a window to divide the selected meal. """
        if not self.meals_tree.currentItem():
            print("Please select an item first.")
            return
        
        self.setAllEnabled(False)
        self.meal_divider_popup = DivideMealWidget(self.mainWindow, self, self.txter)
        self.meal_divider_popup.show()
