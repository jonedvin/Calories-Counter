from modules.food import Ingredient, Dish, IngredientInDish
from modules.databaser import Databaser
from modules.txter import Txter


def get_ingredients(databaser: Databaser) -> dict:
    """ Returns a dictionary on the form {ingredient_name: Ingredient} containing all registered ingredients. """
    ingredients = {}
    ingredients_dict = databaser.get_ingredients()
    for _, ingredient in ingredients_dict.items():
        ingredients[ingredient["name"]] = Ingredient(ingredient["name"],
                                                ingredient["to_grams"],
                                                ingredient["unit"],
                                                ingredient["calories"],
                                                ingredient["fat"],
                                                ingredient["saturated_fat"],
                                                ingredient["carbohydrates"],
                                                ingredient["sugar"],
                                                ingredient["protein"],
                                                ingredient["salt"])
    return ingredients
    

def get_dishes(txter: Txter, ingredients_dict: dict) -> dict:
    """ Returns a dictionary on the form {dish_name: Dish} containing all registered dishes. """
    dishes = {}
    dishes_dict = txter.get_dishes()

    for dish_name, ingredients_list in dishes_dict.items():
        dish = Dish(dish_name)

        for ingredient in ingredients_list:
            name = ingredient["name"]
            dish.ingredients_in_dish[name] = IngredientInDish(name, ingredients_dict[name], ingredient["amount"])

        dishes[dish_name] = dish

    return dishes
