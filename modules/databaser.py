import sqlite3


class Databaser():
    def __init__(self, database_file):

        self.conn = sqlite3.connect(database_file)
        self.cursor = self.conn.cursor()
        
        # Creating table
        user_table = """
        CREATE TABLE IF NOT EXISTS User(
            ID INTEGER NOT NULL,
            Name VARCHAR(255), 
            TargetCalorieCount INTEGER,
            CONSTRAINT user_pk PRIMARY KEY (ID)
        );"""
        self.cursor.execute(user_table)
           
        self.conn.commit()

    def addUser(self, name: str, target_calorie_count: int):
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

    def close(self):
        """ Closes the database. """
        self.conn.close()

    def printUsers(self):
        users = self.cursor.execute(""" SELECT * FROM User """)
        for user in users:
            for col in range(len(user)):
                print(user[col],end=" ")
            print()