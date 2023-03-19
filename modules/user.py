from modules.databaser import Databaser


class User():
    def __init__(self, databaser: Databaser, id: int, name: str, target_calorie_count: int):
        """ Class for representing a user of this program. """
        self.databaser = databaser

        self.id = id
        self.name = name
        self.target_calorie_count = target_calorie_count

    @classmethod
    def fromDatabase(cls, databaser: Databaser, users_tuple: tuple):
        """ Inits User from user_tuple from database. """
        id = users_tuple[0]
        name = users_tuple[1]
        target_calorie_count = users_tuple[2]

        self = cls(databaser, id, name, target_calorie_count)
        return self
    
    def eat_meal(self, timestamp: int, meal_name: str, calories: float):
        """ Registeres that the given meal was eaten at given time. """
        self.databaser.user_ate_meal(self.id, timestamp, meal_name, calories)