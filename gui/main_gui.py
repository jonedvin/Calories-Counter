from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTabWidget
from gui.make_meal_gui import MakeMealWidget
from gui.add_ingredient_gui import AddIngredientWidget
from modules.databaser import Databaser

class MainWindow(QMainWindow):
    WindowWidth = 500
    WindowHeight = 600

    def __init__(self, app):
        super().__init__()

        self.app = app
        
        self.resize(self.WindowWidth, self.WindowHeight)

        self.database_filename = "data/database.db"
        self.databaser = Databaser(self.database_filename)

        # Tabs
        self.add_meal_widget = MakeMealWidget(self.databaser)
        self.add_ingredient_widget = AddIngredientWidget(self.databaser)

        # Add tabs to tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.add_meal_widget, "Make meal")
        self.tab_widget.addTab(self.add_ingredient_widget, "Register ingredients")

        # Build window
        self.general_layout = QVBoxLayout()
        self.general_layout.addWidget(self.tab_widget)
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.general_layout)
        self.setCentralWidget(self.central_widget)
