from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTabWidget
from gui.see_eaten_meals import SeeEatenMealsWidget
from gui.ingredient_gui import IngredientWidget
from gui.made_meals_gui import MadeMealsWidget
from gui.make_meal_gui import MakeMealWidget
from gui.eat_meal_gui import EatMealWidget
from gui.dish_gui import DishWidget
from modules.databaser import Databaser
from modules.txter import Txter


class MainWindow(QMainWindow):
    WindowWidth = 1000
    WindowHeight = 600

    def __init__(self, app):
        super().__init__()

        self.app = app
        
        self.setFixedSize(self.WindowWidth, self.WindowHeight)

        self.database_filename = "data/database.db"
        self.made_meals_filename = "data/made_meals.txt"
        self.dishes_filename = "data/dishes.txt"
        self.databaser = Databaser(self.database_filename)
        self.txter = Txter(self.made_meals_filename, self.dishes_filename)

        # Tabs
        self.add_meal_widget = MakeMealWidget(self.databaser, self.txter)
        self.made_meals_widget = MadeMealsWidget(self.databaser, self.txter)
        self.eat_meal_widget = EatMealWidget(self.databaser, self.txter)
        self.see_eaten_meals_widget = SeeEatenMealsWidget(self.databaser, self.txter)
        self.ingredient_widget = IngredientWidget(self.databaser)
        self.dish_widget = DishWidget(self.databaser, self.txter)

        # Add tabs to tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.add_meal_widget, "Make meal")
        self.tab_widget.addTab(self.made_meals_widget, "Made meals")
        self.tab_widget.addTab(self.eat_meal_widget, "Eat meal")
        self.tab_widget.addTab(self.see_eaten_meals_widget, "See history")
        self.tab_widget.addTab(self.ingredient_widget, "Ingredients")
        self.tab_widget.addTab(self.dish_widget, "Dishes")

        # Build window
        self.general_layout = QVBoxLayout()
        self.general_layout.addWidget(self.tab_widget)
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.general_layout)
        self.setCentralWidget(self.central_widget)
