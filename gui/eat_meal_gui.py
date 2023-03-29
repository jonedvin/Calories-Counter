from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout, QLabel, QTabWidget, QComboBox, QTreeWidget, QTreeWidgetItem
from widgets.datetime_widget import DateTimeWidget
from widgets.base_widget import BaseWidget
from modules.databaser import Databaser
from modules.txter import Txter
from modules.user import User


class EatMealWidget(BaseWidget):
    def __init__(self, mainWindow, databaser: Databaser, txter: Txter, *args, **kwargs):
        """ Widget with components for viewing, throwing away and eating made meals. """
        super().__init__(mainWindow, *args, **kwargs)

        self.databaser = databaser
        self.txter = txter
        self.qlabel_width_short = 130
        self.qlabel_width_long = 150

        # Consumer
        self.user_label = QLabel("Consumer:")
        self.user_label.setFixedWidth(self.qlabel_width_long)
        self.user = QComboBox()
        self.user_section = QHBoxLayout()
        self.user_section.addWidget(self.user_label)
        self.user_section.addWidget(self.user)
        self.user_section.addStretch()
        self.load_users()

        # Consumtion time
        self.eat_time_label = QLabel("Consumption time:")
        self.eat_time_label.setFixedWidth(self.qlabel_width_long)
        self.eat_time = DateTimeWidget()
        self.eat_time_section = QHBoxLayout()
        self.eat_time_section.addWidget(self.eat_time_label)
        self.eat_time_section.addWidget(self.eat_time)
        self.eat_time_section.addStretch()

        # Unregistered meal 
        self.meal_name_label = QLabel("Meal name: ")
        self.meal_name_label.setFixedWidth(self.qlabel_width_short)
        self.meal_name = QLineEdit()
        self.meal_name_section = QHBoxLayout()
        self.meal_name_section.addWidget(self.meal_name_label)
        self.meal_name_section.addWidget(self.meal_name)

        self.meal_calories_label = QLabel("Calories:")
        self.meal_calories_label.setFixedWidth(self.qlabel_width_short)
        self.meal_calories = QLineEdit()
        self.meal_calories_section = QHBoxLayout()
        self.meal_calories_section.addWidget(self.meal_calories_label)
        self.meal_calories_section.addWidget(self.meal_calories)

        # Other nutrients
        self.other_nutrients = ["Fat:", "'- of which saturated:", "Carbohydrates:", "'- of which sugar:", "Protein:", "Salt:"]
        self.other_nutriens_section = QVBoxLayout()
        for nutrient in self.other_nutrients:
            label = QLabel(nutrient)
            label.setFixedWidth(self.qlabel_width_short)
            lineedit = QLineEdit()
            box = QHBoxLayout()
            box.addWidget(label)
            box.addWidget(lineedit)
            self.other_nutriens_section.addLayout(box)

        self.eat_unregistered_section = QVBoxLayout()
        self.eat_unregistered_section.addLayout(self.meal_name_section)
        self.eat_unregistered_section.addLayout(self.meal_calories_section)
        self.eat_unregistered_section.addLayout(self.other_nutriens_section)
        self.eat_unregistered_section.addStretch()
        self.eat_unregistered_widget = QWidget()
        self.eat_unregistered_widget.setLayout(self.eat_unregistered_section)

        # Meals tree
        self.meals_tree = QTreeWidget()
        self.meals_tree.setColumnWidth(0, 200)
        self.meals_tree.setHeaderLabels(["Meals"])
        self.meals_tree.setIndentation(0)
        self.reload()

        # Registered/unregistered meal tab
        self.tabs_widget = QTabWidget()
        self.tabs_widget.addTab(self.meals_tree, "Registered meal")
        self.tabs_widget.addTab(self.eat_unregistered_widget, "Unregistered meal")

        # Bottom section
        self.eat_button = QPushButton("Eat meal")
        self.button_section = QHBoxLayout()
        self.button_section.addStretch()
        self.button_section.addWidget(self.eat_button)

        # Build widget
        self.general_layout = QVBoxLayout()
        self.general_layout.addLayout(self.user_section)
        self.general_layout.addLayout(self.eat_time_section)
        self.general_layout.addWidget(self.tabs_widget)
        self.general_layout.addLayout(self.button_section)
        self.setLayout(self.general_layout)

        # Signals
        self.eat_button.clicked.connect(self.eat_meal)

    
    def reload(self):
        self.txter.populate_meals_tree(self.meals_tree, self.mainWindow.ingredients)

    
    def load_users(self):
        """ Loads registered users and add them to the users QComboBox. """
        users_list = self.databaser.get_users()
        self.user.addItem("", None)
        for user in users_list:
            self.user.addItem(f"{user[0]} {user[1]}", User.fromDatabase(self.databaser, user))


    def delete_meal(self):
        """ Removed the selected meal from made meals. """
        self.txter.remove_meal(self.meals_tree.currentItem().to_string())
        self.meals_tree.invisibleRootItem().removeChild(self.meals_tree.currentItem())

    
    def eat_meal(self):
        """ Eat meal. """
        # Get meal info
        if self.tabs_widget.currentIndex() == 0: # registered
            if not self.meals_tree.currentItem():
                print("Please select meal")
                return

            # Get info
            meal_name = self.meals_tree.currentItem().name
            calories = self.meals_tree.currentItem().calories
            fat = self.meals_tree.currentItem().fat
            saturated_fat = self.meals_tree.currentItem().saturated_fat
            carbohydrates = self.meals_tree.currentItem().carbohydrates
            sugar = self.meals_tree.currentItem().sugar
            protein = self.meals_tree.currentItem().protein
            salt = self.meals_tree.currentItem().salt

        elif self.tabs_widget.currentIndex() == 1: # unregistered
            meal_name = self.meal_name.text()
            calories = self.meal_calories.text()

            # Make sure there's a name
            if not meal_name:
                print("Must enter meal name")
                return

            # Make sure calories is a number
            try:
                calories = float(calories)
            except ValueError:
                print("Calories must be a number")
                return
            
            # Initial values
            fat = None
            saturated_fat = None
            carbohydrates = None
            sugar = None
            protein = None
            salt = None
            
            # Get other nutrients
            for i in range(self.other_nutriens_section.count()):
                layout = self.other_nutriens_section.itemAt(i)
                for widget in (layout.itemAt(j).widget() for j in range(layout.count())):
                    if type(widget) == QLineEdit:
                        try:
                            value = float(widget.text())
                        except ValueError:
                            value = None

                        fat = value if i == 0 else fat
                        saturated_fat = value if i == 1 else saturated_fat
                        carbohydrates = value if i == 2 else carbohydrates
                        sugar = value if i == 3 else sugar
                        protein = value if i == 4 else protein
                        salt = value if i == 5 else salt
    
        else: # tab not implemented
            print(f"Error: self.tabs_widget.currentIndex() == {self.tabs_widget.currentIndex()}")
            return
        
        # Get user
        user = self.user.currentData()
        if not user:
            print("Please select user")
            return
        
        # Get time
        timestamp = self.eat_time.get_timestamp()

        # Eat meal
        user.eat_meal(timestamp, 
                      meal_name, 
                      calories,
                      fat,
                      saturated_fat,
                      carbohydrates,
                      sugar,
                      protein,
                      salt)

        # Delete meal if eaten
        if self.tabs_widget.currentIndex() == 0: # registered 
            self.delete_meal()
            
        elif self.tabs_widget.currentIndex() == 1: # unregistered
            self.meal_name.setText("")
            self.meal_calories.setText("")
            for i in range(self.other_nutriens_section.count()):
                layout = self.other_nutriens_section.itemAt(i)
                for j in range(layout.count()):
                    widget = layout.itemAt(j).widget()
                    if type(widget) == QLineEdit:
                        widget.setText("")
