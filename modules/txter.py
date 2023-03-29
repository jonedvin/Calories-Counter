from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem
from modules.food import Dish, IngredientInDish
import os


class Txter():
    def __init__(self, made_meals_filename: str, dishes_filename: str):
        """ Class for dealing with text files for long term data storage. """
        self.made_meals_filename = made_meals_filename
        self.dishes_filename = dishes_filename

    ###################################################################################################
    ##### General functions ###########################################################################
    ###################################################################################################

    def get_file_lines(self, filename: str) -> list:
        """ Returns a list of all the lines in the give file. """
        if not os.path.exists(filename):
            print(f"File not recognised: {filename}")
            return []
        
        with open(filename) as file:
            return file.readlines()
        

    def write_lines_to_file(self, filename: str, lines: list):
        """ Writes the lines in the given list to the given file, overwriting previous content. """
        if not os.path.exists(filename):
            print(f"File not recognised: {filename}")
            return 
        
        with open(filename, "w") as file:
            for line in lines:
                file.write(line)

    ###################################################################################################
    ##### Meal functions ##############################################################################
    ###################################################################################################

    def get_meals(self, ingredients_dict: dict) -> list:
        """ Returns a list of Dish objects. """
        if not os.path.exists(self.made_meals_filename):
            print(f"File not recognised: {self.made_meals_filename}")
            return 
        
        # Get all meals
        meal_list = []
        lines = self.get_file_lines(self.made_meals_filename)
        for line in lines:
            if not line.strip():
                continue

            name = line.split("-")[0]
            ingredients = line.split("-")[1]

            meal = Dish(name)

            # Add all ingredients
            for ingredient in ingredients.split(","):
                ingredient_name = ingredient.split(":")[0]
                ingredient_in_dish = IngredientInDish(ingredient_name, ingredients_dict[ingredient_name], 0)
                ingredient_in_dish.amount = float(ingredient.split(":")[1].split(" ")[0])
                meal.ingredients_in_dish[ingredient_name] = ingredient_in_dish
            
            meal_list.append(meal)
        
        return meal_list


    def add_meal(self, meal_string: str):
        """ Adds given meal to the made_meals text file. """
        print(f"add_meal run with: {meal_string}")
        if not os.path.exists(self.made_meals_filename):
            print(f"File not recognised: {self.made_meals_filename}")
            return 
    
        with open(self.made_meals_filename, "a") as file:
            file.write("\n"+meal_string)


    def remove_meal(self, meal_string: str):
        """ Removes the given meal from the made_meals text file. """
        if not os.path.exists(self.made_meals_filename):
            print(f"File not recognised: {self.made_meals_filename}")
            return 
        
        lines = self.get_file_lines(self.made_meals_filename)
        for line in lines:
            if line.strip() == meal_string.strip():
                lines.remove(line)
                break
        
        self.write_lines_to_file(self.made_meals_filename, lines)

    
    def populate_meals_tree(self, meals_tree: QTreeWidget, ingredients: dict):
        """ Clears the meal tree, and re-populates it. """
        # Clear tree
        while meals_tree.topLevelItemCount() > 0:
            meals_tree.takeTopLevelItem(0)

        # Get made meals
        made_meals = self.get_meals(ingredients)
        for meal in made_meals:
            meal.setup_tree_widget_item()
            meals_tree.addTopLevelItem(meal)


    ###################################################################################################
    ##### Dish functions ##############################################################################
    ###################################################################################################
    
    def get_dish_names(self) -> list:
        """ Returns a list of all the registered dish names. """
        lines = self.get_file_lines(self.dishes_filename)
        dish_names = []
        for line in lines:
            dish_names.append(line.split("-")[0])
        return sorted(dish_names)
    

    def get_dishes(self) -> dict:
        """ Returns a dict on the form {dish_name: [ {ingredient_name: data} ] } of all dishes. """
        if not os.path.exists(self.dishes_filename):
            print(f"File not recognised: {self.dishes_filename}")
            return 
        
        dishes_dict = {}
        lines = self.get_file_lines(self.dishes_filename)
        for line in lines:
            name = line.split("-")[0]
            data = line.split("-")[1]

            dishes_dict[name] = []
            for ingredient in data.split(","):
                ingredient_dict = {
                    "name": ingredient.split(":")[0],
                    "amount": float(ingredient.split(":")[1].split(" ")[0]) if ingredient.split(":")[1].split(" ")[0] else None,
                    "unit": ingredient.split(":")[1].split(" ")[1]
                }
                dishes_dict[name].append(ingredient_dict)
        
        return dishes_dict

    

    def get_dish_ingedients(self, dish_name: str) -> list:
        """ Returns a list of all the ingredients in the given dish, on the form '[ingredient_name]:[amount][unit]'. """
        if not os.path.exists(self.dishes_filename):
            print(f"File not recognised: {self.dishes_filename}")
            return 
        
        lines = self.get_file_lines(self.dishes_filename)
        dish_ingredients = []

        # Get dish
        dish_line = None
        for line in lines:
            if line.split("-")[0] == dish_name:
                dish_line = line
                break

        # Get ingredients
        for ingredient in dish_line.split("-")[1].split(","):
            dish_ingredients.append(ingredient)
                
        return dish_ingredients


    def add_dish(self, dish_string: str):
        """ Adds given dish to the dishes text file. """
        if not os.path.exists(self.dishes_filename):
            print(f"File not recognised: {self.dishes_filename}")
            return 
    
        with open(self.dishes_filename, "a") as file:
            file.write("\n"+dish_string)


    def edit_dish(self, dish_string: str):
        """ Edits given dish in the dishes text file. """
        if not os.path.exists(self.dishes_filename):
            print(f"File not recognised: {self.dishes_filename}")
            return 
        
        dish_name = dish_string.split("-")[0]
        lines = self.get_file_lines(self.dishes_filename)
        for line in lines:
            if line.split("-")[0] == dish_name:
                lines.remove(line)
        lines.append(dish_string)
        lines.sort()

        self.write_lines_to_file(self.dishes_filename, lines)


    def remove_dish(self, dish_name: str):
        """ Removes the given meal from the made_meals text file. """
        if not os.path.exists(self.dishes_filename):
            print(f"File not recognised: {self.dishes_filename}")
            return 
        
        lines = self.get_file_lines(self.dishes_filename)
        for line in lines:
            if line.split("-")[0].strip() == dish_name:
                lines.remove(line)
                break
        
        self.write_lines_to_file(self.dishes_filename, lines)
