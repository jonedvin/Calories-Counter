from PyQt6.QtWidgets import QVBoxLayout, QWidget, QTabWidget
from gui.see_eaten_meals import SeeEatenMealsWidget
from gui.ingredient_gui import IngredientWidget
from gui.made_meals_gui import MadeMealsWidget
from gui.make_meal_gui import MakeMealWidget
from gui.eat_meal_gui import EatMealWidget
from gui.dish_gui import DishWidget
from widgets.base_widget import BaseMainWindow
from modules.databaser import Databaser
from modules.txter import Txter


class MainWindow(BaseMainWindow):
    WindowWidth = 500
    WindowHeight = 600

    def __init__(self, app, data_folder_path):
        super().__init__()

        self.app = app

        if not data_folder_path:
            data_folder_path = "data"
        
        self.setFixedSize(self.WindowWidth, self.WindowHeight)

        self.database_filename = f"{data_folder_path}/database.db"
        self.made_meals_filename = f"{data_folder_path}/made_meals.txt"
        self.dishes_filename = f"{data_folder_path}/dishes.txt"
        self.databaser = Databaser(self.database_filename)
        self.txter = Txter(self.made_meals_filename, self.dishes_filename)

        # Tabs
        self.add_meal_widget = MakeMealWidget(self, self.databaser, self.txter)
        self.made_meals_widget = MadeMealsWidget(self, self.databaser, self.txter)
        self.eat_meal_widget = EatMealWidget(self, self.databaser, self.txter)
        self.see_eaten_meals_widget = SeeEatenMealsWidget(self, self.databaser, self.txter)
        self.ingredient_widget = IngredientWidget(self, self.databaser)
        self.dish_widget = DishWidget(self, self.databaser, self.txter)

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
