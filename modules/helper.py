from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem, QTableWidget, QTableWidgetItem, QLineEdit
import enum


class unit(enum.Enum):
    g = "g"    # Grams
    dl = "dl"   # desi Litres
    tbsp = "tbsp" # Table spoons
    tsp = "tsp"  # Tea spoons
    unit = "unit" # Standard unit



class IngredientItem(QTreeWidgetItem):
    def __init__(self, name: str, unit: unit, amount_column: int, *args, tree: QTreeWidget = None, **kwargs):
        """ Class for displaying an ingredient in its tree. """
        super().__init__(*args, **kwargs)
        
        self.name = name
        self.unit = unit
        self.amount_column = amount_column

        self.tree = tree
        if self.tree:
            self.tree.addTopLevelItem(self)

        self.setText(0, name)
        self.setText(2, unit.value)

    @property
    def amount(self):
        """ Returns the amount specified. """
        return self.text(3)
    
    def addQLineWidget(self, column: int, standard_amount: float):
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

    def setValues(self, calories: float,
                        fat: float,
                        saturated_fat: float,
                        carbohydrates: float,
                        sugar: float,
                        protein: float,
                        salt: float):
        """ Sets the given values to their respective rows in the table. """
        self.setItem(0, 1, QTableWidgetItem(str(round(calories, 2))))
        self.setItem(1, 1, QTableWidgetItem(str(round(fat, 2))))
        self.setItem(2, 1, QTableWidgetItem(str(round(saturated_fat, 2))))
        self.setItem(3, 1, QTableWidgetItem(str(round(carbohydrates, 2))))
        self.setItem(4, 1, QTableWidgetItem(str(round(sugar, 2))))
        self.setItem(5, 1, QTableWidgetItem(str(round(protein, 2))))
        self.setItem(6, 1, QTableWidgetItem(str(round(salt, 2))))
