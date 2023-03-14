from collections import namedtuple

Ingredient = namedtuple("Ingredient", ["unit", "standard_amount"])

# All values given per 100g of ingredient
ingredients = {
    "Chicken": {
        "to_grams": 1,
        "Calories": 147,
        "Fat": 8.3,
        "'- of which saturated": 2.5,
        "Carbohydrates": 0,
        "'- of which sugar": 0,
        "Protein": 18,
        "Salt": 0.2
    },
    "Dijon mustard": {
        "to_grams": 15,
        "Calories": 151,
        "Fat": 11,
        "'- of which saturated": 0.6,
        "Carbohydrates": 3.5,
        "'- of which sugar": 1.9,
        "Protein": 7,
        "Salt": 4.9
    },
    "Soy sauce": {
        "to_grams": 5,
        "Calories": 72,
        "Fat": 0,
        "'- of which saturated": 0,
        "Carbohydrates": 7.8,
        "'- of which sugar": 1.6,
        "Protein": 7.1,
        "Salt": 16.2
    },
    "Rice": {
        "to_grams": 80,
        "Calories": 343,
        "Fat": 0.8,
        "'- of which saturated": 0.3,
        "Carbohydrates": 75,
        "'- of which sugar": 0.7,
        "Protein": 7.49,
        "Salt": 0.01
    },
    "Redcurrant jam": {
        "to_grams": 15,
        "Calories": 210,
        "Fat": 0.5,
        "'- of which saturated": 0,
        "Carbohydrates": 52.5,
        "'- of which sugar": 52.5,
        "Protein": 0.3,
        "Salt": 0
    },
    "Cream (fløte)": {
        "to_grams": 50,
        "Calories": 353,
        "Fat": 37,
        "'- of which saturated": 24,
        "Carbohydrates": 2.9,
        "'- of which sugar": 2.9,
        "Protein": 2.1,
        "Salt": 0.1
    },
    "Broccoli": {
        "to_grams": 1,
        "Calories": 28,
        "Fat": 0.3,
        "'- of which saturated": 0.1,
        "Carbohydrates": 1.9,
        "'- of which sugar": 1.9,
        "Protein": 3.2,
        "Salt": 0
    },
    "Chicken stock": {
        "to_grams": 10,
        "Calories": 271,
        "Fat": 9.6,
        "'- of which saturated": 5.1,
        "Carbohydrates": 40.3,
        "'- of which sugar": 25.1,
        "Protein": 5.7,
        "Salt": 33
    },
}

template = {
    "template": {
        "to_100g": 1,
        "Calories": 100,
        "Fat": 100,
        "'- of which saturated": 100,
        "Carbohydrates": 100,
        "'- of which sugar": 100,
        "Protein": 100,
        "Salt": 100
    },
}
