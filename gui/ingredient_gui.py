from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout, QLabel, QTabWidget, QComboBox
from widgets.base_widget import BaseWidget
from modules.databaser import Databaser
from modules.food import registered_units



class IngredientWidget(BaseWidget):
    def __init__(self, mainWindow, databaser: Databaser, *args, **kwargs):
        """ Widget with components for registering new ingredients to the database. """
        super().__init__(mainWindow, *args, **kwargs)

        self.databaser = databaser
        self.qlabel_width = 130

        self.ingredient_names = databaser.get_ingredient_names()

        # Components
        self.add_name = QHBoxLayout()
        self.add_name.addWidget(QLabel("Ingredient name:"))
        self.add_name.addWidget(QLineEdit())
        self.add_name.itemAt(0).widget().setFixedWidth(self.qlabel_width)
        self.add_name_widget = QWidget()
        self.add_name_widget.setLayout(self.add_name)

        self.edit_name = QHBoxLayout()
        self.edit_name.addWidget(QLabel("Ingredient name:"))
        self.edit_name.addWidget(QComboBox())
        self.edit_name.itemAt(0).widget().setFixedWidth(self.qlabel_width)
        self.edit_name_widget = QWidget()
        self.edit_name_widget.setLayout(self.edit_name)

        self.remove_name = QHBoxLayout()
        self.remove_name.addWidget(QLabel("Ingredient name:"))
        self.remove_name.addWidget(QComboBox())
        self.remove_name.itemAt(0).widget().setFixedWidth(self.qlabel_width)
        self.remove_name_widget = QWidget()
        self.remove_name_widget.setLayout(self.remove_name)

        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.add_name_widget, "Add ingredient")
        self.tab_widget.addTab(self.edit_name_widget, "Edit ingredient")
        self.tab_widget.addTab(self.remove_name_widget, "Remove ingredient")
        self.tab_widget.setFixedHeight(100)

        self.to_grams = QHBoxLayout()
        self.to_grams.addWidget(QLabel("To grams:"))
        self.to_grams.addWidget(QLineEdit())
        self.to_grams.itemAt(0).widget().setFixedWidth(self.qlabel_width)

        self.unit = QHBoxLayout()
        self.unit.addWidget(QLabel("Unit:"))
        self.unit.addWidget(QLineEdit())
        self.unit.itemAt(0).widget().setFixedWidth(self.qlabel_width)

        self.calories = QHBoxLayout()
        self.calories.addWidget(QLabel("Calories:"))
        self.calories.addWidget(QLineEdit())
        self.calories.itemAt(0).widget().setFixedWidth(self.qlabel_width)

        self.fat = QHBoxLayout()
        self.fat.addWidget(QLabel("Fat:"))
        self.fat.addWidget(QLineEdit())
        self.fat.itemAt(0).widget().setFixedWidth(self.qlabel_width)

        self.saturated_fat = QHBoxLayout()
        self.saturated_fat.addWidget(QLabel("'- of which saturated:"))
        self.saturated_fat.addWidget(QLineEdit())
        self.saturated_fat.itemAt(0).widget().setFixedWidth(self.qlabel_width)

        self.carbohydrates = QHBoxLayout()
        self.carbohydrates.addWidget(QLabel("Carbohydrates:"))
        self.carbohydrates.addWidget(QLineEdit())
        self.carbohydrates.itemAt(0).widget().setFixedWidth(self.qlabel_width)

        self.sugar = QHBoxLayout()
        self.sugar.addWidget(QLabel("'- of which sugar:"))
        self.sugar.addWidget(QLineEdit())
        self.sugar.itemAt(0).widget().setFixedWidth(self.qlabel_width)

        self.protein = QHBoxLayout()
        self.protein.addWidget(QLabel("Protein:"))
        self.protein.addWidget(QLineEdit())
        self.protein.itemAt(0).widget().setFixedWidth(self.qlabel_width)

        self.salt = QHBoxLayout()
        self.salt.addWidget(QLabel("Salt:"))
        self.salt.addWidget(QLineEdit())
        self.salt.itemAt(0).widget().setFixedWidth(self.qlabel_width)

        self.add_edit_remove_ingredient_button = QPushButton("Add ingredient")
        self.button_section = QHBoxLayout()
        self.button_section.addStretch()
        self.button_section.addWidget(self.add_edit_remove_ingredient_button)

        # Build widget
        self.general_layout = QVBoxLayout()
        self.general_layout.addWidget(self.tab_widget)
        self.general_layout.addLayout(self.to_grams)
        self.general_layout.addLayout(self.unit)
        self.general_layout.addLayout(self.calories)
        self.general_layout.addLayout(self.fat)
        self.general_layout.addLayout(self.saturated_fat)
        self.general_layout.addLayout(self.carbohydrates)
        self.general_layout.addLayout(self.sugar)
        self.general_layout.addLayout(self.protein)
        self.general_layout.addLayout(self.salt)
        self.general_layout.addLayout(self.button_section)
        self.setLayout(self.general_layout)

        # Signals
        self.tab_widget.currentChanged.connect(self.update_view)
        self.add_edit_remove_ingredient_button.clicked.connect(self.add_edit_remove_ingredient)
        self.add_name.itemAt(1).widget().returnPressed.connect(self.add_edit_remove_ingredient)
        self.edit_name.itemAt(1).widget().currentTextChanged.connect(self.update_values)
        self.to_grams.itemAt(1).widget().returnPressed.connect(self.add_edit_remove_ingredient)
        self.calories.itemAt(1).widget().returnPressed.connect(self.add_edit_remove_ingredient)
        self.fat.itemAt(1).widget().returnPressed.connect(self.add_edit_remove_ingredient)
        self.saturated_fat.itemAt(1).widget().returnPressed.connect(self.add_edit_remove_ingredient)
        self.carbohydrates.itemAt(1).widget().returnPressed.connect(self.add_edit_remove_ingredient)
        self.sugar.itemAt(1).widget().returnPressed.connect(self.add_edit_remove_ingredient)
        self.protein.itemAt(1).widget().returnPressed.connect(self.add_edit_remove_ingredient)
        self.salt.itemAt(1).widget().returnPressed.connect(self.add_edit_remove_ingredient)

    
    def update_view(self):
        """ Updates the widget to match the tab selected. """
        self.clear_values()

        if self.tab_widget.currentIndex() == 0: # add
            self.add_name.itemAt(1).widget().setFocus()
            self.add_edit_remove_ingredient_button.setText("Add ingredient")

        elif self.tab_widget.currentIndex() == 1: # edit
            self.edit_name.itemAt(1).widget().clear()
            self.edit_name.itemAt(1).widget().addItem("")
            self.edit_name.itemAt(1).widget().addItems(self.databaser.get_ingredient_names())
            self.edit_name.itemAt(1).widget().setFocus()
            self.add_edit_remove_ingredient_button.setText("Update ingredient")

        elif self.tab_widget.currentIndex() == 2: # remove
            self.remove_name.itemAt(1).widget().clear()
            self.remove_name.itemAt(1).widget().addItem("")
            self.remove_name.itemAt(1).widget().addItems(self.databaser.get_ingredient_names())
            self.remove_name.itemAt(1).widget().setFocus()
            self.add_edit_remove_ingredient_button.setText("Remove ingredient")

        # Enable/disable nutrients
        enabled = False if self.tab_widget.currentIndex() == 2 else True
        self.to_grams.itemAt(0).widget().setEnabled(enabled)
        self.to_grams.itemAt(1).widget().setEnabled(enabled)
        self.unit.itemAt(0).widget().setEnabled(enabled)
        self.unit.itemAt(1).widget().setEnabled(enabled)
        self.calories.itemAt(0).widget().setEnabled(enabled)
        self.calories.itemAt(1).widget().setEnabled(enabled)
        self.fat.itemAt(0).widget().setEnabled(enabled)
        self.fat.itemAt(1).widget().setEnabled(enabled)
        self.saturated_fat.itemAt(0).widget().setEnabled(enabled)
        self.saturated_fat.itemAt(1).widget().setEnabled(enabled)
        self.carbohydrates.itemAt(0).widget().setEnabled(enabled)
        self.carbohydrates.itemAt(1).widget().setEnabled(enabled)
        self.sugar.itemAt(0).widget().setEnabled(enabled)
        self.sugar.itemAt(1).widget().setEnabled(enabled)
        self.protein.itemAt(0).widget().setEnabled(enabled)
        self.protein.itemAt(1).widget().setEnabled(enabled)
        self.salt.itemAt(0).widget().setEnabled(enabled)
        self.salt.itemAt(1).widget().setEnabled(enabled)


    def update_values(self):
        """ Updates the values to match those in the database. """
        name = self.get_name()
        if not name:
            self.clear_values()
            return
        
        ingredient = self.databaser.get_ingredient(name)

        self.to_grams.itemAt(1).widget().setText(str(ingredient["to_grams"]))
        self.unit.itemAt(1).widget().setText(str(ingredient["unit"]))
        self.calories.itemAt(1).widget().setText(str(ingredient["calories"]))
        self.fat.itemAt(1).widget().setText(str(ingredient["fat"]))
        self.saturated_fat.itemAt(1).widget().setText(str(ingredient["saturated_fat"]))
        self.carbohydrates.itemAt(1).widget().setText(str(ingredient["carbohydrates"]))
        self.sugar.itemAt(1).widget().setText(str(ingredient["sugar"]))
        self.protein.itemAt(1).widget().setText(str(ingredient["protein"]))
        self.salt.itemAt(1).widget().setText(str(ingredient["salt"]))

    
    def get_value(self, layout: QHBoxLayout) -> float:
        """ Returns value if valid value, None if not. """
        value = layout.itemAt(1).widget().text()
        
        # Make sure there's data
        if not value:
            print(f"Add {layout.itemAt(0).widget().text()[:-1]}")
            return None
        
        # Convert to float
        try:
            value = float(value.strip())
        except ValueError:
            print(f"{layout.itemAt(0).widget().text()} must be a number")
            return None
        
        return value
    
    def get_name(self) -> str:
        """ Returns the ingredient name. """
        if self.tab_widget.currentIndex() == 0: # add_name
            return self.add_name.itemAt(1).widget().text().strip()
        
        elif self.tab_widget.currentIndex() == 1: # edit_name
            return self.edit_name.itemAt(1).widget().currentText().strip()
        
        elif self.tab_widget.currentIndex() == 2: # remove_name
            return self.remove_name.itemAt(1).widget().currentText().strip()
    
        return ""
    
    def get_unit(self) -> str:
        """ Returns the unit. """
        unit = self.unit.itemAt(1).widget().text().strip()
        if unit:
            if unit not in registered_units:
                print("Unit not regonised. Make sure to use one of the following:")
                for unit in registered_units:
                    print(f"- {unit}")
                return None
        return unit


    def clear_values(self):
        """ Clears the values of the QLineEdits. """
        self.add_name.itemAt(1).widget().setText("")
        self.to_grams.itemAt(1).widget().setText("")
        self.unit.itemAt(1).widget().setText("")
        self.calories.itemAt(1).widget().setText("")
        self.fat.itemAt(1).widget().setText("")
        self.saturated_fat.itemAt(1).widget().setText("")
        self.carbohydrates.itemAt(1).widget().setText("")
        self.sugar.itemAt(1).widget().setText("")
        self.protein.itemAt(1).widget().setText("")
        self.salt.itemAt(1).widget().setText("")


    def add_edit_remove_ingredient(self):
        """ Adds ingredient whose info is inserted into the database. """
        # Get all ingredient names and make sure it's not registered already
        name = self.get_name()

        if self.tab_widget.currentIndex() == 0: # add
            already_registered_ingredients = self.databaser.get_ingredient_names()
            for ingredient in already_registered_ingredients:
                if name.lower() == ingredient.lower():
                    print("Ingredient already added. ")
                    self.clear_values()
                    return
                
        elif self.tab_widget.currentIndex() == 2: # remove
            self.databaser.remove_ingredient(name)
            self.update_view() # To clear away the removed ingredient
            return

        # Get all values
        to_grams = self.get_value(self.to_grams)
        unit = self.get_unit()
        calories = self.get_value(self.calories)
        fat = self.get_value(self.fat)
        saturated_fat = self.get_value(self.saturated_fat)
        carbohydrates = self.get_value(self.carbohydrates)
        sugar = self.get_value(self.sugar)
        protein = self.get_value(self.protein)
        salt = self.get_value(self.salt)
        
        # Check that all values are inserted and okay
        if name is None \
        or to_grams is None  \
        or unit is None  \
        or calories is None  \
        or fat is None  \
        or saturated_fat is None  \
        or carbohydrates is None  \
        or sugar is None  \
        or protein is None  \
        or salt is None:
            print("Missing values.")
            return

        # Add ingredient
        if self.tab_widget.currentIndex() == 0: # add
            self.databaser.add_ingredient(name, to_grams, unit, calories, fat, saturated_fat, carbohydrates, sugar, protein, salt)
            self.clear_values()
        elif self.tab_widget.currentIndex() == 1: # edit
            self.databaser.edit_ingredient(name, to_grams, unit, calories, fat, saturated_fat, carbohydrates, sugar, protein, salt)
        else:
            print("Error: Tab not recognised!")
            return
