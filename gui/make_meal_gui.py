from PyQt6.QtWidgets import QWidget, QComboBox, QTreeWidget, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout
from pyqt_modules.meal_divider_widget import MealDividerWidget
from pyqt_modules.ingredient_item import IngredientItem
from pyqt_modules.nutrients_table import NutrientsTable
from modules.databaser import Databaser
from modules.txter import Txter
from modules.load_data import get_ingredients, get_dishes


class MakeMealWidget(QWidget):
    AmountColumn = 1
    MealDividerColumn = 3

    def __init__(self, databaser: Databaser, txter: Txter, *args, **kwargs):
        """ Widget with components for calculating the nutrients of a meal. """
        super().__init__(*args, **kwargs)

        self.databaser = databaser
        self.txter = txter
        self.made_meals_filename = "data/made_meals.txt"

        # Current dish
        self.current_dish = None

        # Meal section
        self.meal = QComboBox()
        self.reload_meals()
        self.reload_meals_button = QPushButton("Reload")
        self.reload_meals_button.setFixedWidth(100)
        self.select_meal_section = QHBoxLayout()
        self.select_meal_section.addWidget(self.meal)
        self.select_meal_section.addWidget(self.reload_meals_button)
        self.select_meal_section.addStretch()

        # Ingredients tree
        self.ingredients_tree = QTreeWidget()
        self.ingredients_tree.setColumnCount(4)
        self.ingredients_tree.setHeaderLabels(["Ingredients", "", "", ""])
        self.ingredients_tree.setColumnWidth(0, 200)
        self.ingredients_tree.setColumnWidth(1, 40)
        self.ingredients_tree.setColumnWidth(2, 50)
        self.ingredients_tree.setIndentation(5)
        self.ingredients_tree.setFixedHeight(300)

        # Nutrients table section
        self.calculate_button = QPushButton("Calculate")
        self.calculate_layout = QHBoxLayout()
        self.calculate_layout.addWidget(self.calculate_button)
        self.calculate_layout.addStretch()
        self.nutrients_table = NutrientsTable()
        self.nutrients_section = QVBoxLayout()
        self.nutrients_section.addLayout(self.calculate_layout)
        self.nutrients_section.addWidget(self.nutrients_table)
        self.nutrients_section_widget = QWidget()
        self.nutrients_section_widget.setLayout(self.nutrients_section)
        width = 0
        for column in range(3):
            width += self.ingredients_tree.columnWidth(column)
        self.nutrients_section_widget.setFixedWidth(width)

        # Make meal section
        self.overall_meal_divider = MealDividerWidget()

        self.add_divider_button = QPushButton("Add divider")
        self.remove_divider_button = QPushButton("Delete divider")
        self.divider_section = QHBoxLayout()
        self.divider_section.addWidget(self.add_divider_button)
        self.divider_section.addWidget(self.remove_divider_button)
        self.divider_section.addStretch()

        self.fill_to_target_button = QPushButton("Fill to target")
        self.target = QLineEdit()
        self.target_layout = QHBoxLayout()
        self.target_layout.addWidget(self.fill_to_target_button)
        self.target_layout.addWidget(self.target)

        self.make_meal_button = QPushButton("Make meal")

        self.make_meal_meal_section = QVBoxLayout()
        self.make_meal_meal_section.addWidget(self.overall_meal_divider)
        self.make_meal_meal_section.addLayout(self.divider_section)
        self.make_meal_meal_section.addStretch()
        self.make_meal_meal_section.addLayout(self.target_layout)
        self.make_meal_meal_section.addWidget(self.make_meal_button)

        # Bottom layout
        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.setContentsMargins(0,60,0,0)
        self.bottom_layout.setSpacing(0)
        self.bottom_layout.addWidget(self.nutrients_section_widget)
        self.bottom_layout.addLayout(self.make_meal_meal_section)

        # Build widget
        self.general_layout = QVBoxLayout()
        self.general_layout.addLayout(self.select_meal_section)
        self.general_layout.addWidget(self.ingredients_tree)
        self.general_layout.addLayout(self.bottom_layout)
        self.setLayout(self.general_layout)

        self.buttons_setEnabled(False)

        # Signals
        self.meal.currentTextChanged.connect(self.update_ingredients)
        self.meal.currentTextChanged.connect(self.nutrients_table.clear_nutrients)
        self.reload_meals_button.clicked.connect(self.reload_meals)
        self.calculate_button.clicked.connect(self.calculate)
        self.fill_to_target_button.clicked.connect(self.fill_to_target)
        self.target.editingFinished.connect(self.fill_to_target)
        self.make_meal_button.clicked.connect(self.make_meal)
        self.add_divider_button.clicked.connect(lambda: self.overall_meal_divider.addDivider())


    def reload_meals(self):
        """ Clears the meals, and loads them in again, thus refereshing the list. """
        self.meal.clear()

        self.ingredients = get_ingredients(self.databaser)
        self.dishes = get_dishes(self.txter, self.ingredients)

        self.meal.addItem("")
        for dish in self.dishes:
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

        self.txter.add_meal(self.current_dish.to_made_meal_string())

    
    def buttons_setEnabled(self, set_enabled: bool):
        """ Sets all buttons to set_enabled. """
        self.calculate_button.setEnabled(set_enabled)
        self.fill_to_target_button.setEnabled(set_enabled)
        self.add_divider_button.setEnabled(set_enabled)
        self.remove_divider_button.setEnabled(set_enabled)


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
        self.current_dish = self.dishes[self.meal.currentText()]

        # Update ingredients
        self.buttons_setEnabled(True)
        for _, ingredient_in_dish in self.current_dish.ingredients_in_dish.items():
            standard_amount = str(ingredient_in_dish.standard_amount) if ingredient_in_dish.standard_amount else ""
            ingredient_item = IngredientItem(ingredient_in_dish, self.AmountColumn, tree=self.ingredients_tree)
            ingredient_item.addQLineEdit(self.AmountColumn, standard_amount)
            ingredient_item.addMealDivider(self.MealDividerColumn)

    
    def getAmounts(self):
        amounts = {}
        for i in range(self.ingredients_tree.topLevelItemCount()):
            ingredient_item = self.ingredients_tree.topLevelItem(i)
            amounts[ingredient_item.ingredient.name] = ingredient_item.getAmount()
        return amounts

    
    def calculate(self):
        self.current_dish.calculate(self.getAmounts(), self.nutrients_table)


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
