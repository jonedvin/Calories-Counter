from data.ingredients import ingredients_database
from data.dishes import dishes_database
from modules.food import Ingredient, Dish, IngredientInDish
        

def get_ingredients() -> dict:
    """ Returns a dictionary on the form {ingredient_name: Ingredient} containing all registered ingredients. """
    ingredients = {}
    for name, data in ingredients_database.items():
        ingredients[name] = Ingredient(name,
                                 data["Calories"],
                                 data["Fat"],
                                 data["'- of which saturated"],
                                 data["Carbohydrates"],
                                 data["'- of which sugar"],
                                 data["Protein"],
                                 data["Salt"],
                                 data["to_grams"])
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
