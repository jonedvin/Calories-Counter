from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem, QLineEdit
from modules.food import IngredientInDish
from pyqt_modules.meal_divider_widget import MealDividerWidget


class IngredientItem(QTreeWidgetItem):
    def __init__(self, ingredient_in_dish: IngredientInDish, amount_column: int, *args, tree: QTreeWidget = None, **kwargs):
        """ Class for displaying an ingredient in its tree. """
        super().__init__(*args, **kwargs)
        
        self.ingredient = ingredient_in_dish.ingredient
        self.amount_column = amount_column

        self.tree = tree
        if self.tree:
            self.tree.addTopLevelItem(self)

        self.setText(0, self.ingredient.name)
        self.setText(2, self.ingredient.unit)

    @property
    def amount(self):
        """ Returns the amount specified. """
        return self.text(3)
    
    def addQLineEdit(self, column: int, standard_amount: float):
        """ Adds a QLineEdit widget in the specified column. """
        self.tree.setItemWidget(self, column, QLineEdit(standard_amount))
    
    def addMealDivider(self, column: int):
        """ Adds a QLineEdit widget in the specified column. """
        self.tree.setItemWidget(self, column, MealDividerWidget())
    
    def getAmount(self):
        """
        Returns the amount written for the item. \n
        Returns 0 if empty or value is not a number.
        """
        amount = self.treeWidget().itemWidget(self, self.amount_column).text()
        if not amount:
            return 0
        try:
            return float(amount)
        except ValueError:
            return 0
        
    def setAmount(self, amount: float):
        """ Sets the amount to amount."""
        self.treeWidget().itemWidget(self, self.amount_column).setText(str(amount))
