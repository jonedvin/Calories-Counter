import sqlite3


class Databaser():
    def __init__(self, database_file):
        """ Class for interacting with the database. """

        self.conn = sqlite3.connect(database_file)
        self.cursor = self.conn.cursor()
        
        # Create tables
        user_table = """
        CREATE TABLE IF NOT EXISTS User(
            ID INTEGER NOT NULL,
            Name VARCHAR(255), 
            TargetCalorieCount INTEGER,
            CONSTRAINT user_pk PRIMARY KEY (ID)
        );"""
        self.cursor.execute(user_table)

        ingredients_table = """
        CREATE TABLE IF NOT EXISTS Ingredient(
            Name VARCHAR(255) NOT NULL, 
            ToGrams REAL,
            Unit VARCHAR(255),
            Calories REAL,
            Fat REAL,
            SaturatedFat REAL,
            Carbohydrates REAL,
            Sugar REAL,
            Protein REAL,
            Salt REAL,
            CONSTRAINT ingredient_pk PRIMARY KEY (Name)
        );"""
        self.cursor.execute(ingredients_table)

        eaten_meals_table = """
        CREATE TABLE IF NOT EXISTS EatenMeals(
            UserId INTEGER NOT NULL,
            Timestamp INTEGER NOT NULL,
            MealName VARCHAR(255),
            Calories REAL NOT NULL,
            Fat REAL,
            SaturatedFat REAL,
            Carbohydrates REAL,
            Sugar REAL,
            Protein REAL,
            Salt REAL
        );"""
        self.cursor.execute(eaten_meals_table)
           
        self.conn.commit()

    def close(self):
        """ Closes the database. """
        self.conn.close()

    ###################################################################################################
    ##### User functions ##############################################################################
    ###################################################################################################

    def add_user(self, name: str, target_calorie_count: int):
        """ Adds a new user to the User table in the database. """
        # Get count(id) and ids used
        new_id = self.cursor.execute("""SELECT COUNT(ID) FROM User""").fetchone()[0] + 1
        ids = self.cursor.execute("""SELECT ID FROM User""")

        # Get unique id
        while True:
            found_identical = False
            for id in ids:
                if new_id == id:
                    found_identical = True
            
            if not found_identical:
                break

            new_id += 1

        # Add new user
        insert_string = f""" INSERT INTO User VALUES ({new_id}, '{name}', {target_calorie_count}) """
        self.cursor.execute(insert_string)
        self.conn.commit()

    
    def get_users(self) -> list:
        """ Returns a list of user tuples, that can be fed directly into the User class. """
        query = self.cursor.execute(""" SELECT * FROM User """)
        users = []
        for user in query:
            users.append(user)
        return users


    def print_users(self):
        users = self.cursor.execute(""" SELECT * FROM User """)
        for user in users:
            for col in range(len(user)):
                print(user[col],end=" ")
            print()


    def user_ate_meal(self, userId: int, 
                            timestamp: int, 
                            meal_name: str,
                            calories: float,
                            fat: float = None,
                            saturated_fat: float = None,
                            carbohydrates: float = None,
                            sugar: float = None,
                            protein: float = None,
                            salt: float = None):
        """ Saves the meal to the user's eaten meals database. """
        if not fat:
            fat = "NULL"
        if not saturated_fat:
            saturated_fat = "NULL"
        if not carbohydrates:
            carbohydrates = "NULL"
        if not sugar:
            sugar = "NULL"
        if not protein:
            protein = "NULL"
        if not salt:
            salt = "NULL"

        insert_string = f""" INSERT INTO EatenMeals VALUES ({userId}, 
                                                            {timestamp}, 
                                                            '{meal_name}', 
                                                            {calories}, 
                                                            {fat}, 
                                                            {saturated_fat}, 
                                                            {carbohydrates}, 
                                                            {sugar}, 
                                                            {protein}, 
                                                            {salt}); """
        self.cursor.execute(insert_string)
        self.conn.commit()


    ###################################################################################################
    ##### Ingredient functions ########################################################################
    ###################################################################################################

    def get_ingredient_names(self) -> list:
        """ Returns a list of all ingredient names. """
        query = self.cursor.execute(""" SELECT Name FROM Ingredient """)
        ingredients = []
        for ingredient in query:
            ingredients.append(ingredient[0])

        return sorted(ingredients)

    def get_ingredients(self) -> dict:
        """ Returns a dict on the form {name: data} of all ingredients. """
        query = self.cursor.execute(""" SELECT * FROM Ingredient """)
        ingredients = {}
        for ingredient in query:
            ingredients[ingredient[0]] = {
                "name": ingredient[0],
                "to_grams": ingredient[1],
                "unit": ingredient[2],
                "calories": ingredient[3],
                "fat": ingredient[4],
                "saturated_fat": ingredient[5],
                "carbohydrates": ingredient[6],
                "sugar": ingredient[7],
                "protein": ingredient[8],
                "salt": ingredient[9],
            }

        return ingredients

    def get_ingredient(self, name: str) -> dict:
        """ Returns a dict with the given ingredient's info. """
        query = self.cursor.execute(f""" SELECT * FROM Ingredient WHERE Name = '{name}'""")
        for ingredient in query:
            return {
                "name": ingredient[0],
                "to_grams": ingredient[1],
                "unit": ingredient[2],
                "calories": ingredient[3],
                "fat": ingredient[4],
                "saturated_fat": ingredient[5],
                "carbohydrates": ingredient[6],
                "sugar": ingredient[7],
                "protein": ingredient[8],
                "salt": ingredient[9],
            }
    

    def add_ingredient(self,
                       name: str,
                       to_grams: float,
                       unit: str,
                       calories: float,
                       fat: float,
                       saturated_fat: float,
                       carbohydrates: float,
                       sugar: float,
                       protein: float,
                       salt: float):
        """ Adds the given ingredient to the ingredient table in the database. """
        insert_string = f""" 
        INSERT INTO Ingredient 
        VALUES ('{name}', {to_grams}, '{unit}', {calories}, {fat}, {saturated_fat}, {carbohydrates}, {sugar}, {protein}, {salt})
        """
        self.cursor.execute(insert_string)
        self.conn.commit()
        print("Added ingredient")
    

    def edit_ingredient(self,
                       name: str,
                       to_grams: float,
                       unit: str,
                       calories: float,
                       fat: float,
                       saturated_fat: float,
                       carbohydrates: float,
                       sugar: float,
                       protein: float,
                       salt: float):
        """ Adds the given ingredient to the ingredient table in the database. """
        insert_string = f"""
        UPDATE Ingredient
        SET ToGrams = {to_grams},
            Unit = '{unit}',
            Calories = {calories},
            Fat = {fat},
            SaturatedFat = {saturated_fat},
            Carbohydrates = {carbohydrates},
            Sugar = {sugar},
            Protein = {protein},
            Salt = {salt}
        WHERE Name = '{name}';
        """
        self.cursor.execute(insert_string)
        self.conn.commit()
        print("Updated ingredient")


    def remove_ingredient(self, name: str):
        """ Removed the given ingredient from the database. """
        remove_string = f""" DELETE FROM Ingredient WHERE Name = '{name}'; """
        self.cursor.execute(remove_string)
        self.conn.commit()
        print(f"Removed ingredient: {name}")
