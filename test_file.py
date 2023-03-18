from modules.databaser import Databaser
from modules.txter import *
import sqlite3

if __name__ == "__main__":
    databaser = Databaser("data/database.db")
    # databaser.addUser("Ovar", 3500)

    # databaser.printUsers()
    # ingredients = databaser.get_ingredient_names()
    databaser.move_over_ingredients()

    # filename = "data/made_meals.txt"
    # lines = get_file_lines(filename)
    # write_lines_to_file(filename, lines)





