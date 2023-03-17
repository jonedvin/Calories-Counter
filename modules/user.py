


class User():
    def __init__(self, id: int, name: str, target_calorie_count: int):
        """ Class for representing a user of this program. """
        self.id = id
        self.name = name
        self.target_calorie_count = target_calorie_count

    @classmethod
    def fromDatabase(cls):
        pass