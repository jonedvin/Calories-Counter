from modules.databaser import Databaser


class User():
    def __init__(self, databaser: Databaser, id: int, name: str, target_calorie_count: int):
        """ Class for representing a user of this program. """
        self.databaser = databaser

        self.id = id
        self.name = name
        self.target_calorie_count = target_calorie_count

        self.eaten_meals = None

    @classmethod
    def fromDatabase(cls, databaser: Databaser, users_tuple: tuple):
        """ Inits User from user_tuple from database. """
        id = users_tuple[0]
        name = users_tuple[1]
        target_calorie_count = users_tuple[2]

        self = cls(databaser, id, name, target_calorie_count)
        return self
    
    def eat_meal(self, timestamp: int, 
                       meal_name: str, 
                       calories: float,
                       fat: float = None,
                       saturated_fat: float = None,
                       carbohydrates: float = None,
                       sugar: float = None,
                       protein: float = None,
                       salt: float = None):
        """ Registeres that the given meal was eaten at given time. """
        self.databaser.user_ate_meal(self.id, 
                                     timestamp, 
                                     meal_name, 
                                     calories,
                                     fat,
                                     saturated_fat,
                                     carbohydrates,
                                     sugar,
                                     protein,
                                     salt)
        
    def get_eaten_meals(self) -> list:
        """ Returns a list of eaten meals. """
        if not self.eaten_meals:
            self.eaten_meals = self.databaser.get_eaten_meals_by_user(self.id)
        return self.eaten_meals
