from PyQt6.QtWidgets import QComboBox, QTreeWidget, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout
from widgets.ingredient_item import IngredientItem
from widgets.nutrients_table import NutrientsTable
from widgets.base_widget import BaseWidget
from modules.databaser import Databaser
from modules.txter import Txter
from modules.load_data import get_ingredients, get_dishes


class MakeMealWidget(BaseWidget):
    AmountColumn = 1
    MealDividerColumn = 3

    def __init__(self, mainWindow, databaser: Databaser, txter: Txter, *args, **kwargs):
        """ Widget with components for calculating the nutrients of a meal. """
        super().__init__(mainWindow, *args, **kwargs)

        self.databaser = databaser
        self.txter = txter
        self.made_meals_filename = "data/made_meals.txt"

        # Current dish
        self.current_dish = None

        # Meal section
        self.meal = QComboBox()
        self.reload()
        self.reload_meals_button = QPushButton("Reload")
        self.reload_meals_button.setFixedWidth(100)
        self.select_meal_section = QHBoxLayout()
        self.select_meal_section.addWidget(self.meal)
        self.select_meal_section.addWidget(self.reload_meals_button)
        self.select_meal_section.addStretch()

        # Ingredients tree
        self.ingredients_tree = QTreeWidget()
        self.ingredients_tree.setColumnCount(3)
        self.ingredients_tree.setHeaderLabels(["Ingredients", "", ""])
        self.ingredients_tree.setColumnWidth(0, 200)
        self.ingredients_tree.setColumnWidth(1, 40)
        self.ingredients_tree.setColumnWidth(2, 50)
        self.ingredients_tree.setIndentation(5)

        # Nutrients table section
        self.nutrients_table = NutrientsTable()
        width = 0
        for column in range(3):
            column_width = self.ingredients_tree.columnWidth(column)
            self.nutrients_table.setColumnWidth(column, column_width)
            width += column_width
        self.nutrients_table.setFixedWidth(width+2)

        # Calculate strip
        self.calculate_button = QPushButton("Calculate")
        self.fill_to_target_button = QPushButton("Fill to target")
        self.target = QLineEdit()
        self.calculate_strip = QHBoxLayout()
        self.calculate_strip.addWidget(self.calculate_button)
        self.calculate_strip.addWidget(self.fill_to_target_button)
        self.calculate_strip.addWidget(self.target)
        self.calculate_strip.addStretch()

        self.make_meal_button = QPushButton("Make meal")

        self.make_meal_meal_section = QVBoxLayout()
        self.make_meal_meal_section.addStretch()
        self.make_meal_meal_section.addWidget(self.make_meal_button)

        # Bottom layout
        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.setContentsMargins(0,0,0,0)
        self.bottom_layout.setSpacing(0)
        self.bottom_layout.addWidget(self.nutrients_table)
        self.bottom_layout.addWidget(self.make_meal_button)

        # Build widget
        self.general_layout = QVBoxLayout()
        self.general_layout.addLayout(self.select_meal_section)
        self.general_layout.addWidget(self.ingredients_tree)
        self.general_layout.addLayout(self.calculate_strip)
        self.general_layout.addLayout(self.bottom_layout)
        self.setLayout(self.general_layout)

        self.buttons_setEnabled(False)

        # Signals
        self.meal.currentTextChanged.connect(self.update_ingredients)
        self.meal.currentTextChanged.connect(self.nutrients_table.clear_nutrients)
        self.reload_meals_button.clicked.connect(self.reload)
        self.calculate_button.clicked.connect(self.calculate)
        self.fill_to_target_button.clicked.connect(self.fill_to_target)
        self.target.editingFinished.connect(self.fill_to_target)
        self.make_meal_button.clicked.connect(self.make_meal)


    def reload(self):
        """ Clears the meals, and loads them in again, thus refereshing the list. """
        self.meal.clear()

        self.mainWindow.ingredients = get_ingredients(self.databaser)
        self.mainWindow.dishes = get_dishes(self.txter, self.mainWindow.ingredients)

        self.meal.addItem("")
        for dish in self.mainWindow.dishes:
            self.meal.addItem(dish)

    
    def make_meal(self):
        """ Makes a meal and saves it. """
        self.calculate()

        # Make sure all values are okay
        amounts = self.getAmounts()
        for amount in amounts:
            if not amount:
                print("Cannot make, missing amount")
                return

        self.txter.add_meal(self.current_dish.to_string())

    
    def buttons_setEnabled(self, set_enabled: bool):
        """ Sets all buttons to set_enabled. """
        self.calculate_button.setEnabled(set_enabled)
        self.fill_to_target_button.setEnabled(set_enabled)


    def update_ingredients(self):
        """ Updates the ingredients list according to dish selected. """

        # Clear ingredients
        while self.ingredients_tree.topLevelItemCount() > 0:
            self.ingredients_tree.takeTopLevelItem(0)

        # Remove ingredients if nothing is selected
        if not self.meal.currentText():
            self.buttons_setEnabled(False)
            self.current_dish = None
            return
        
        # Update self.current_dish
        self.current_dish = self.mainWindow.dishes[self.meal.currentText()]

        # Update ingredients
        self.buttons_setEnabled(True)
        for _, ingredient_in_dish in self.current_dish.ingredients_in_dish.items():
            standard_amount = str(ingredient_in_dish.standard_amount) if ingredient_in_dish.standard_amount else ""
            ingredient_item = IngredientItem(ingredient_in_dish, self.AmountColumn, tree=self.ingredients_tree)
            ingredient_item.addQLineEdit(self.AmountColumn, standard_amount)

    
    def getAmounts(self):
        amounts = {}
        for i in range(self.ingredients_tree.topLevelItemCount()):
            ingredient_item = self.ingredients_tree.topLevelItem(i)
            amounts[ingredient_item.ingredient.name] = ingredient_item.getAmount()
        return amounts
    

    def updateAmounts(self):
        for i in range(self.ingredients_tree.topLevelItemCount()):
            ingredient_item = self.ingredients_tree.topLevelItem(i)
            self.current_dish.ingredients_in_dish[ingredient_item.ingredient.name].amount = ingredient_item.getAmount()

    
    def calculate(self):
        self.updateAmounts()
        self.current_dish.calculate(nutrients_table=self.nutrients_table)


    def fill_to_target(self):
        """
        Sets the amount of one empty ingredient to match target calories.
        """
        if not self.current_dish:
            print("Please select a dish first. ")
            return
        
        # Make sure the target value is a valid number
        target = self.target.text()
        if not target:
            print("Enter a target calorie count for the meal.")
            return
        try:
            target = float(target)
        except ValueError:
            print("Target calorie count must be a number.")
            return
        
        # Calculate amount of remaining ingredient
        empty_ingredient_name, amount = self.current_dish.fill_to_target(target, self.getAmounts())
        if not empty_ingredient_name:
            return

        # Find empty ingredient
        for i in range(self.ingredients_tree.topLevelItemCount()):
            ingredient_item = self.ingredients_tree.topLevelItem(i)
            if ingredient_item.ingredient.name == empty_ingredient_name:
                empty_ingredient = ingredient_item
                break

        # Set amount and calculate
        empty_ingredient.setAmount(round(amount, 1))
        self.calculate()
