from information.ingredients import Ingredient
from modules.helper import unit

dishes = {
    "Chicken in the good sauce": {
        "Chicken": Ingredient(unit.g, None),
        "Broccoli": Ingredient(unit.g, 100),
        "Rice": Ingredient(unit.dl, None),
        "Cream (fløte)": Ingredient(unit.dl, 3),
        "Redcurrant jam": Ingredient(unit.tbsp, 2),
        "Dijon mustard": Ingredient(unit.tbsp, 2),
        "Soy sauce": Ingredient(unit.tsp, 2),
        "Chicken stock": Ingredient(unit.unit, 2)
    }
}
