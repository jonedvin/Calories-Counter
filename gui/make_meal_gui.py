from PyQt6.QtWidgets import QWidget, QComboBox, QTreeWidget, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout
from modules.helper import IngredientItem, NutrientsTable
from information.ingredients import ingredients
from information.dishes import dishes


class MakeMealWidget(QWidget):
    AmountColumn = 1

    def __init__(self, *args, **kwargs):
        """ Widget with components for calculating the nutrients of a meal. """
        super().__init__(*args, **kwargs)

        # Compnonents
        self.meal = QComboBox()
        self.meal.addItem("")
        for dish in dishes:
            self.meal.addItem(dish)

        self.ingredients_tree = QTreeWidget()
        self.ingredients_tree.setColumnCount(3)
        self.ingredients_tree.setHeaderLabels(["Ingredients", "", ""])
        self.ingredients_tree.setColumnWidth(0, 200)
        self.ingredients_tree.setColumnWidth(1, 40)
        self.ingredients_tree.setColumnWidth(2, 50)
        self.ingredients_tree.setIndentation(5)

        self.calculate_button = QPushButton("Calculate")
        self.fill_to_target_button = QPushButton("Fill to target")
        self.target = QLineEdit()
        self.calculate_layout = QHBoxLayout()
        self.calculate_layout.addStretch()
        self.calculate_layout.addWidget(self.calculate_button)
        self.calculate_layout.addStretch()
        self.calculate_layout.addWidget(self.fill_to_target_button)
        self.calculate_layout.addWidget(self.target)
        self.calculate_layout.addStretch()

        self.nutrients_table = NutrientsTable()

        self.make_meal_button = QPushButton("Make meal")
        self.make_meal_button_layout = QHBoxLayout()
        self.make_meal_button_layout.addStretch()
        self.make_meal_button_layout.addWidget(self.make_meal_button)

        # Build widget
        self.general_layout = QVBoxLayout()
        self.general_layout.addWidget(self.meal)
        self.general_layout.addWidget(self.ingredients_tree)
        self.general_layout.addLayout(self.calculate_layout)
        self.general_layout.addWidget(self.nutrients_table)
        self.general_layout.addLayout(self.make_meal_button_layout)
        self.setLayout(self.general_layout)

        # Signals
        self.meal.currentTextChanged.connect(self.update_ingredients)
        self.calculate_button.clicked.connect(self.calculate)
        self.fill_to_target_button.clicked.connect(self.fill_to_target)
        self.target.editingFinished.connect(self.fill_to_target)
        # self.make_meal_button.clicked.connnect(pass)


    def update_ingredients(self):
        """ Updates the ingredients list according to dish selected. """
        # Remove ingredients if nothing is selected
        if not self.meal.currentText():
            while self.ingredients_tree.topLevelItemCount() > 0:
                self.ingredients_tree.takeTopLevelItem(0)
            self.calculate_button.setEnabled(False)
            return

        # Update ingredients
        self.calculate_button.setEnabled(True)
        for ingredient, info in dishes[self.meal.currentText()].items():
            standard_amount = str(info.standard_amount) if info.standard_amount else ""
            ingredient_item = IngredientItem(ingredient, info.unit, self.AmountColumn, tree=self.ingredients_tree)
            ingredient_item.addQLineWidget(self.AmountColumn, standard_amount)


    def calculate(self, fill_to_target: bool = False):
        """
        Calculates and updates gui with nutrient values for the selected meal.\n
        If fill_to_target: returns the total calories and the empty ingredient.
        """
        # Initial values
        calories = 0
        fat = 0
        saturated_fat = 0
        carbohydrates = 0
        sugar = 0
        protein = 0
        salt = 0

        # Calculate totals
        empty_ingredient = None
        for i in range(self.ingredients_tree.topLevelItemCount()):
            ingredient = self.ingredients_tree.topLevelItem(i)

            amount = ingredient.getAmount()
            if amount == 0:

                # Ignore a single empty ingredient if filling
                if fill_to_target:
                    if empty_ingredient:
                        print("Fill in the amount for all but 1 (one) ingredient.")
                        return
                    empty_ingredient = ingredient
                    continue

                # Panic
                else:
                    print(f"{ingredient.name} does not have a value.")
                    return
            
            # Add to totals
            amount_in_grams = amount*ingredients[ingredient.name]["to_grams"]
            calories += ingredients[ingredient.name]["Calories"]*amount_in_grams/100
            fat += ingredients[ingredient.name]["Fat"]*amount_in_grams/100
            saturated_fat += ingredients[ingredient.name]["'- of which saturated"]*amount_in_grams/100
            carbohydrates += ingredients[ingredient.name]["Carbohydrates"]*amount_in_grams/100
            sugar += ingredients[ingredient.name]["'- of which sugar"]*amount_in_grams/100
            protein += ingredients[ingredient.name]["Protein"]*amount_in_grams/100
            salt += ingredients[ingredient.name]["Salt"]*amount_in_grams/100

        # Return result
        if fill_to_target:
            return calories, empty_ingredient
        else:
            self.nutrients_table.setValues(calories, fat, saturated_fat, carbohydrates, sugar, protein, salt)

    
    def fill_to_target(self):
        """
        Sets the amount of one empty ingredient to match target calories.
        """
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

        # Get calories and ingredient
        calories, empty_ingredient = self.calculate(fill_to_target=True)
        calories_to_go = target-calories

        if not empty_ingredient:
            print("Please remove amount for 1 (one) ingredient.")
            return

        # Make sure we're not in negatives
        if calories_to_go < 0:
            print(f"The selected amount is already higher than target: {calories}")
            return
        
        # Calculate amount
        amount_in_grams = calories_to_go*100 / ingredients[empty_ingredient.name]["Calories"]
        amount_in_unit = amount_in_grams / ingredients[empty_ingredient.name]["to_grams"]

        # Set amount and display results
        empty_ingredient.setAmount(round(amount_in_unit, 1))
        self.calculate()
