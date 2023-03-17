from PyQt6.QtWidgets import QWidget, QComboBox, QTreeWidget, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout
from modules.helper import IngredientItem, NutrientsTable
from modules.load_ingredients import get_ingredients, get_dishes


class MakeMealWidget(QWidget):
    AmountColumn = 1

    def __init__(self, *args, **kwargs):
        """ Widget with components for calculating the nutrients of a meal. """
        super().__init__(*args, **kwargs)

        # Get dishes and ingredients
        self.ingredients = get_ingredients()
        self.dishes = get_dishes(self.ingredients)

        # Current dish
        self.current_dish = None

        # Compnonents
        self.meal = QComboBox()
        self.meal.addItem("")
        for dish in self.dishes:
            self.meal.addItem(dish)

        self.ingredients_tree = QTreeWidget()
        self.ingredients_tree.setColumnCount(3)
        self.ingredients_tree.setHeaderLabels(["Ingredients", "", ""])
        self.ingredients_tree.setColumnWidth(0, 200)
        self.ingredients_tree.setColumnWidth(1, 40)
        self.ingredients_tree.setColumnWidth(2, 50)
        self.ingredients_tree.setIndentation(5)

        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.setEnabled(False)
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

        # Clear ingredients
        while self.ingredients_tree.topLevelItemCount() > 0:
            self.ingredients_tree.takeTopLevelItem(0)

        # Remove ingredients if nothing is selected
        if not self.meal.currentText():
            self.calculate_button.setEnabled(False)
            self.current_dish = None
            return
        
        # Update self.current_dish
        self.current_dish = self.dishes[self.meal.currentText()]

        # Update ingredients
        self.calculate_button.setEnabled(True)
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
    