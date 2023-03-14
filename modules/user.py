


class User():
    def __init__(self, id: int, name: str, targetCalorieCount: int):
        """ Class for representing a user of this program. """
        self.id = id
        self.name = name
        self.targetCalorieCount = targetCalorieCount

    @classmethod
    def fromDatabase(cls):
        pass