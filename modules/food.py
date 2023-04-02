from PyQt6.QtWidgets import QTreeWidgetItem
import enum


class unit(enum.Enum):
    g = "g"    # Grams
    dl = "dl"   # desi Litres
    tbsp = "tbsp" # Table spoons
    tsp = "tsp"  # Tea spoons

registered_units = ["g", "dl", "tbst", "tsp"]


class Food():
    def __init__(self, name: str,
                       calories: float,
                       fat: float,
                       saturated_fat: float,
                       carbohydrates: float,
                       sugar: float,
                       protein: float,
                       salt: float):
        """ Abstract class for representing food. """
        self.name = name
        self.calories = calories
        self.fat = fat
        self.saturated_fat = saturated_fat
        self.carbohydrates = carbohydrates
        self.sugar = sugar
        self.protein = protein
        self.salt = salt


class Ingredient(Food):
    def __init__(self, name: str,
                       to_grams: float,
                       unit: str,
                       calories: float,
                       fat: float,
                       saturated_fat: float,
                       carbohydrates: float,
                       sugar: float,
                       protein: float,
                       salt: float ):
        """ Class for representing an ingredient. """
        super().__init__(name,
                         calories,
                         fat,
                         saturated_fat,
                         carbohydrates,
                         sugar,
                         protein,
                         salt)
        
        self.to_grams = to_grams
        self.unit = unit

    def __repr__(self):
        string = f"{self.name}:"
        string += f"\nTo grams: {self.to_grams}"
        string += f"\nCalories: {self.calories}"
        string += f"\nFat: {self.fat}"
        string += f"\nSaturated fat: {self.saturated_fat}"
        string += f"\nCarbohydrates: {self.carbohydrates}"
        string += f"\nSugar: {self.sugar}"
        string += f"\nProtein: {self.protein}"
        string += f"\nSalt: {self.salt}"
        return string


class Dish(Food, QTreeWidgetItem):
    def __init__(self, name: str, *args, **kwargs):
        """ Class for representing a dish. """
        Food.__init__(self, name, 0, 0, 0, 0, 0, 0, 0)
        QTreeWidgetItem.__init__(self, *args, **kwargs)

        self.name = name
        self.ingredients_in_dish = {}

    
    def setup_tree_widget_item(self) -> None:
        """ Setup object as QTreeWidgetItem. """
        self.calculate()
        self.setText(0, f"{self.name}: {round(self.calories)} kcal")


    def to_string(self) -> str:
        """ Returns a string containing information to reconstruct the dish object. """
        string = f"{self.name}-"

        for name, ingredient_in_dish in self.ingredients_in_dish.items():
            string += f"{name}:{self.ingredients_in_dish[name].amount} {ingredient_in_dish.ingredient.unit},"

        return string[:-1]
    

    def to_made_meal_string(self) -> str:
        """ Returns a string containing the meal name, and its nutrients. """
        string = f"{self.name}-"
        string += f"calories:{self.calories},"
        string += f"fat:{self.fat},"
        string += f"saturated_fat:{self.saturated_fat},"
        string += f"carbohydrates:{self.carbohydrates},"
        string += f"sugar:{self.sugar},"
        string += f"protein:{self.protein},"
        string += f"salt:{self.salt}"
        string += "-"
        for ingredient, in_dish in self.ingredients_in_dish.items():
            string += f"{ingredient}:{in_dish.amount},"
        return string[:-1]


    def reset_nutrients_values(self):
        """ Sets the value of all the dishes nutrients to 0. """
        self.calories = 0
        self.fat = 0
        self.saturated_fat = 0
        self.carbohydrates = 0
        self.sugar = 0
        self.protein = 0
        self.salt = 0


    def calculate(self, nutrients_table = None, fill_to_target: bool = False):
        """
        Calculates and updates gui with nutrient values for the selected meal.\n
        If nutrients_table: saves the results to given NutrientsTable.\n
        If fill_to_target: returns the total calories and the empty ingredient's name.
        """
        # Reset values
        self.reset_nutrients_values()

        # Calculate totals
        empty_ingredient = None
        for _, ingredient_in_dish in self.ingredients_in_dish.items():
            amount = ingredient_in_dish.amount

            if amount == 0:

                # Ignore a single empty ingredient if filling
                if fill_to_target:
                    if empty_ingredient:
                        print("Fill in the amount for all but 1 (one) ingredient.")
                        self.reset_nutrients_values()
                        return (None, None)
                    empty_ingredient = ingredient_in_dish.name
                    continue

                # Panic
                else:
                    print(f"{ingredient_in_dish.name} does not have a value.")
                    self.reset_nutrients_values()
                    return (None, None)
            
            # Add to totals
            amount_in_grams = amount*ingredient_in_dish.ingredient.to_grams
            self.calories += ingredient_in_dish.ingredient.calories*amount_in_grams/100
            self.fat += ingredient_in_dish.ingredient.fat*amount_in_grams/100
            self.saturated_fat += ingredient_in_dish.ingredient.saturated_fat*amount_in_grams/100
            self.carbohydrates += ingredient_in_dish.ingredient.carbohydrates*amount_in_grams/100
            self.sugar += ingredient_in_dish.ingredient.sugar*amount_in_grams/100
            self.protein += ingredient_in_dish.ingredient.protein*amount_in_grams/100
            self.salt += ingredient_in_dish.ingredient.salt*amount_in_grams/100

            # Save amount
            self.ingredients_in_dish[ingredient_in_dish.name].amount = amount

        # Return result
        if fill_to_target:
            return self.calories, empty_ingredient
        elif nutrients_table:
            nutrients_table.setValues(self)

    
    def fill_to_target(self, target: float, amounts: list):
        """
        Returns the name of the empty ingredient, and the amount needed to reach target. 
        """
        # Get calories and ingredient
        calories, empty_ingredient_name = self.calculate(amounts, fill_to_target=True)
        calories_to_go = target-calories

        if not empty_ingredient_name:
            print("Please remove amount for 1 (one) ingredient.")
            return None, None

        # Make sure we're not in negatives
        if calories_to_go < 0:
            print(f"The selected amount is already higher than target: {calories}")
            return None, None
        
        # Calculate amount
        amount_in_grams = calories_to_go*100 / self.ingredients_in_dish[empty_ingredient_name].ingredient.calories
        amount_in_unit = amount_in_grams / self.ingredients_in_dish[empty_ingredient_name].ingredient.to_grams

        # Set amount and display results
        return empty_ingredient_name, amount_in_unit



class IngredientInDish(QTreeWidgetItem):
    def __init__(self, name: str, ingredient: Ingredient, standard_amount: float, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.ingredient = ingredient
        self.standard_amount = standard_amount

        self.amount = standard_amount

        self.setText(0, self.name)
        self.setText(1, str(self.amount))
