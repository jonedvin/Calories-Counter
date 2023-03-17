from modules.databaser import Databaser

if __name__ == "__main__":
    databaser = Databaser("database.db")
    databaser.addUser("Ovar", 3500)

    databaser.printUsers()

