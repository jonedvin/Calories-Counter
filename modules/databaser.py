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
           
        self.conn.commit()

    def close(self):
        """ Closes the database. """
        self.conn.close()

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

    def print_users(self):
        users = self.cursor.execute(""" SELECT * FROM User """)
        for user in users:
            for col in range(len(user)):
                print(user[col],end=" ")
            print()

    def get_ingredient_names(self) -> list:
        """ Returns a list of all ingredient names. """
        query = self.cursor.execute(""" SELECT Name FROM Ingredient """)
        ingredients = []
        for ingredient in query:
            ingredients.append(ingredient[0])

        return ingredients

    def get_ingredients(self) -> list:
        """ Returns a list of all ingrediens. """
        query = self.cursor.execute(""" SELECT * FROM Ingredient """)
        ingredients = []
        for ingredient in query:
            ingredients.append(ingredient)

        return ingredients

    def get_ingredient(self, name: str) -> tuple:
        """ Returns a list of all ingrediens. """
        query = self.cursor.execute(f""" SELECT * FROM Ingredient WHERE Name = '{name}'""")
        for ingredient in query:
            return ingredient
    

    def add_ingredient(self,
                       name: str,
                       to_grams: float,
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
        VALUES ('{name}', {to_grams}, {calories}, {fat}, {saturated_fat}, {carbohydrates}, {sugar}, {protein}, {salt})
        """
        self.cursor.execute(insert_string)
        self.conn.commit()
        print("Added ingredient")
    

    def edit_ingredient(self,
                       name: str,
                       to_grams: float,
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
