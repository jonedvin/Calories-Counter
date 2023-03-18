from data.ingredients import ingredients_database
from data.dishes import dishes_database
from modules.food import Ingredient, Dish, IngredientInDish
from modules.databaser import Databaser
        

def get_ingredients(databaser: Databaser) -> dict:
    """ Returns a dictionary on the form {ingredient_name: Ingredient} containing all registered ingredients. """
    ingredients = {}
    ingredients_list = databaser.get_ingredients()
    for ingredient in ingredients_list:
        ingredients[ingredient[0]] = Ingredient(ingredient[0], # name
                                                ingredient[2], # calories
                                                ingredient[3], # fat
                                                ingredient[4], # saturated fat
                                                ingredient[5], # carbohydrates
                                                ingredient[6], # sugar
                                                ingredient[7], # protein
                                                ingredient[8], # salt
                                                ingredient[1]) # to grams
    return ingredients
    

def get_dishes(ingredients_dict: dict) -> dict:
    """ Returns a dictionary on the form {dish_name: Dish} containing all registered dishes. """
    dishes = {}
    for dish_name, ingredients_list in dishes_database.items():
        dish = Dish(dish_name)

        for ingredient in ingredients_list:
            name = ingredient[0]
            unit = ingredient[1]
            standard_amount = ingredient[2]

            dish.ingredients_in_dish[name] = IngredientInDish(name, ingredients_dict[name], unit, standard_amount)

        dishes[dish_name] = dish

    return dishes
