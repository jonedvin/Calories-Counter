import sqlite3


class Databaser():
    def __init__(self):

        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()
        
        # Creating table
        table = """CREATE TABLE STUDENT(NAME VARCHAR(255), CLASS VARCHAR(255),
        SECTION VARCHAR(255));"""
        self.cursor.execute(table)
        
        # Queries to INSERT records.
        self.cursor.execute('''INSERT INTO STUDENT VALUES ('Raju', '7th', 'A')''')
        self.cursor.execute('''INSERT INTO STUDENT VALUES ('Shyam', '8th', 'B')''')
        self.cursor.execute('''INSERT INTO STUDENT VALUES ('Baburao', '9th', 'C')''')
        
        # Display data inserted
        print("Data Inserted in the table: ")
        data=self.cursor.execute('''SELECT * FROM STUDENT''')
        for row in data:
            print(row)
        
        # Commit your changes in the database    
        self.conn.commit()
        
        self.conn.close()