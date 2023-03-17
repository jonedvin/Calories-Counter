from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from modules.food import Food


class NutrientsTable(QTableWidget):
    RowHeight = 15

    def __init__(self, *args, **kwargs):
        """ Class"""
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

    def clear_nutrients(self):
        for i in range(7):
            self.setItem(i, 1, QTableWidgetItem(""))
