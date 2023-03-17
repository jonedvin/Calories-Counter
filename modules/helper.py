from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem, QTableWidget, QTableWidgetItem, QLineEdit
from modules.food import Food, IngredientInDish, unit



class IngredientItem(QTreeWidgetItem):
    def __init__(self, ingredient_in_dish: IngredientInDish, amount_column: int, *args, tree: QTreeWidget = None, **kwargs):
        """ Class for displaying an ingredient in its tree. """
        super().__init__(*args, **kwargs)
        
        self.ingredient = ingredient_in_dish.ingredient
        self.unit = ingredient_in_dish.unit
        self.amount_column = amount_column

        self.tree = tree
        if self.tree:
            self.tree.addTopLevelItem(self)

        self.setText(0, self.ingredient.name)
        self.setText(2, self.unit.value)

    @property
    def amount(self):
        """ Returns the amount specified. """
        return self.text(3)
    
    def addQLineEdit(self, column: int, standard_amount: float):
        """ Adds a QLineEdit widget in the specified column. """
        self.tree.setItemWidget(self, column, QLineEdit(standard_amount))
    
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
        


class NutrientsTable(QTableWidget):
    RowHeight = 15

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)
        self.setFixedHeight(7*self.RowHeight+2)
        self.setFixedWidth(200+70+50+2)

        self.setRowCount(7)
        self.verticalHeader().setMinimumSectionSize(self.RowHeight)
        self.verticalHeader().setDefaultSectionSize(self.RowHeight)

        self.setColumnCount(3)
        self.setColumnWidth(0, 200)
        self.setColumnWidth(1, 70)
        self.setColumnWidth(2, 50)

        self.setItem(0, 2, QTableWidgetItem("kcal"))
        for i in range(1, self.rowCount()):
            self.setItem(i, 2, QTableWidgetItem("g"))

        self.setItem(0, 0, QTableWidgetItem("Calories"))
        self.setItem(1, 0, QTableWidgetItem("Fat"))
        self.setItem(2, 0, QTableWidgetItem("'- of which saturated"))
        self.setItem(3, 0, QTableWidgetItem("Carbohydrates"))
        self.setItem(4, 0, QTableWidgetItem("'- of which sugar"))
        self.setItem(5, 0, QTableWidgetItem("Protein"))
        self.setItem(6, 0, QTableWidgetItem("Salt"))

    def setValues(self, food: Food):
        """ Sets the given values to their respective rows in the table. """
        self.setItem(0, 1, QTableWidgetItem(str(round(food.calories, 2))))
        self.setItem(1, 1, QTableWidgetItem(str(round(food.fat, 2))))
        self.setItem(2, 1, QTableWidgetItem(str(round(food.saturated_fat, 2))))
        self.setItem(3, 1, QTableWidgetItem(str(round(food.carbohydrates, 2))))
        self.setItem(4, 1, QTableWidgetItem(str(round(food.sugar, 2))))
        self.setItem(5, 1, QTableWidgetItem(str(round(food.protein, 2))))
        self.setItem(6, 1, QTableWidgetItem(str(round(food.salt, 2))))


def save_made_meal(meal_name: str, nutrients):
    pass