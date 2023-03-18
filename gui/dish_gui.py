from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout, QLabel, QTabWidget, QComboBox, QTreeWidget, QTreeWidgetItem
from modules.databaser import Databaser
from modules.txter import Txter


class DishWidget(QWidget):
    def __init__(self, databaser: Databaser, txter: Txter, *args, **kwargs):
        """ Widget with components for registering new ingredients to the database. """
        super().__init__(*args, **kwargs)

        self.databaser = databaser
        self.txter = txter
        self.qlabel_width = 130

        # Components
        self.add_name = QHBoxLayout()
        self.add_name.addWidget(QLabel("Dish name:"))
        self.add_name.addWidget(QLineEdit())
        self.add_name.itemAt(0).widget().setFixedWidth(self.qlabel_width)
        self.add_name_widget = QWidget()
        self.add_name_widget.setLayout(self.add_name)

        self.edit_name = QHBoxLayout()
        self.edit_name.addWidget(QLabel("Dish name:"))
        self.edit_name.addWidget(QComboBox())
        self.edit_name.itemAt(0).widget().setFixedWidth(self.qlabel_width)
        self.edit_name_widget = QWidget()
        self.edit_name_widget.setLayout(self.edit_name)

        self.remove_name = QHBoxLayout()
        self.remove_name.addWidget(QLabel("Dish name:"))
        self.remove_name.addWidget(QComboBox())
        self.remove_name.itemAt(0).widget().setFixedWidth(self.qlabel_width)
        self.remove_name_widget = QWidget()
        self.remove_name_widget.setLayout(self.remove_name)

        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.add_name_widget, "Add dish")
        self.tab_widget.addTab(self.edit_name_widget, "Edit dish")
        self.tab_widget.addTab(self.remove_name_widget, "Remove dish")
        self.tab_widget.setFixedHeight(100)

        self.ingredients_tree = QTreeWidget()
        self.ingredients_tree.setColumnCount(3)
        self.ingredients_tree.setColumnWidth(0, 200)
        self.ingredients_tree.setHeaderLabels(["Ingredients", "", ""])
        self.ingredients_tree.setColumnWidth(0, 200)
        self.ingredients_tree.setColumnWidth(1, 40)
        self.ingredients_tree.setColumnWidth(2, 50)
        self.ingredients_tree.setIndentation(5)

        self.add_ingredient_button = QPushButton("Add ingredient")
        self.add_edit_remove_dish_button = QPushButton("Add dish")
        self.button_section = QHBoxLayout()
        self.button_section.addWidget(self.add_ingredient_button)
        self.button_section.addStretch()
        self.button_section.addWidget(self.add_edit_remove_dish_button)

        # Build widget
        self.general_layout = QVBoxLayout()
        self.general_layout.addWidget(self.tab_widget)
        self.general_layout.addWidget(self.ingredients_tree)
        self.general_layout.addLayout(self.button_section)
        self.setLayout(self.general_layout)

        # Signals
        self.tab_widget.currentChanged.connect(self.update_view)
        self.add_ingredient_button.clicked.connect(self.add_ingredient)
        self.add_edit_remove_dish_button.clicked.connect(self.add_edit_remove_dish)
        self.add_name.itemAt(1).widget().returnPressed.connect(self.add_edit_remove_dish)
        self.edit_name.itemAt(1).widget().currentTextChanged.connect(self.update_values)

    
    def update_view(self):
        """ Updates the widget to match the tab selected. """
        self.clear_values()

        if self.tab_widget.currentIndex() == 0: # add
            self.add_name.itemAt(1).widget().setFocus()
            self.add_edit_remove_dish_button.setText("Add dish")

        elif self.tab_widget.currentIndex() == 1: # edit
            self.dish_names = self.txter.get_dish_names()
            self.edit_name.itemAt(1).widget().clear()
            self.edit_name.itemAt(1).widget().addItem("")
            self.edit_name.itemAt(1).widget().addItems(self.dish_names)
            self.edit_name.itemAt(1).widget().setFocus()
            self.add_edit_remove_dish_button.setText("Update dish")

        elif self.tab_widget.currentIndex() == 2: # remove
            self.dish_names = self.txter.get_dish_names()
            self.remove_name.itemAt(1).widget().clear()
            self.remove_name.itemAt(1).widget().addItem("")
            self.remove_name.itemAt(1).widget().addItems(self.dish_names)
            self.remove_name.itemAt(1).widget().setFocus()
            self.add_edit_remove_dish_button.setText("Remove dish")

        # Enable/disable nutrients
        enabled = False if self.tab_widget.currentIndex() == 2 else True
        self.ingredients_tree.setEnabled(enabled)

    
    def add_ingredients_to_combobox(self, combobox: QComboBox):
        """ Adds an empty item, and all ingredients to given QComboBox. """
        combobox.addItem("")
        for _, ingredient in self.databaser.get_ingredients().items():
            combobox.addItem(ingredient["name"], ingredient["unit"])
        combobox.setFocus()

    
    def add_ingredient(self, item: QTreeWidgetItem = None):
        """ Adds an ingredient line to self.ingredients_tree. """
        # Make item
        if not item:
            item = QTreeWidgetItem()
        self.ingredients_tree.addTopLevelItem(item)

        # Make QLineEdit
        unit_lineedit = QLineEdit()

        # Make QComboBox
        ingredients_combobox = QComboBox()
        self.add_ingredients_to_combobox(ingredients_combobox)
        ingredients_combobox.currentTextChanged.connect(lambda: item.setText(2, ingredients_combobox.currentData()))

        # Insert QComboBox and QLineEdit
        self.ingredients_tree.setItemWidget(item, 0, ingredients_combobox)
        self.ingredients_tree.setItemWidget(item, 1, unit_lineedit)


    def update_values(self):
        """ Updates the values to match those in the database. """
        name = self.get_name()
        if not name:
            self.clear_values()
            return
        
        ingredients = self.txter.get_dish_ingedients(name)
        for ingredient in ingredients:
            ingredient_name = ingredient.split(":")[0]
            amount = float(ingredient.split(":")[1].split(" ")[0]) if ingredient.split(":")[1].split(" ")[0] else ""
            unit = ingredient.split(":")[1].split(" ")[1]

            item = QTreeWidgetItem()
            self.add_ingredient(item=item)
            self.ingredients_tree.itemWidget(item, 0).setCurrentText(ingredient_name)
            self.ingredients_tree.itemWidget(item, 1).setText(str(amount))
    

    def get_name(self) -> str:
        """ Returns the ingredient name. """
        if self.tab_widget.currentIndex() == 0: # add_name
            return self.add_name.itemAt(1).widget().text()
        
        elif self.tab_widget.currentIndex() == 1: # edit_name
            return self.edit_name.itemAt(1).widget().currentText()
        
        elif self.tab_widget.currentIndex() == 2: # remove_name
            return self.remove_name.itemAt(1).widget().currentText()
    
        return ""
    

    def clear_values(self):
        """ Clears the values of the QLineEdits. """
        self.add_name.itemAt(1).widget().setText("")
        while self.ingredients_tree.topLevelItemCount() > 0:
            self.ingredients_tree.takeTopLevelItem(0)


    def add_edit_remove_dish(self):
        """ Adds ingredient whose info is inserted into the database. """
        # Get all ingredient names and make sure it's not registered already
        name = self.get_name()

        if self.tab_widget.currentIndex() == 0: # add
            already_registered_dishes = self.txter.get_dish_names()
            for dish in already_registered_dishes:
                if name.lower() == dish.lower():
                    print("Dish already added. ")
                    self.clear_values()
                    return

        elif self.tab_widget.currentIndex() == 2: # remove
            self.txter.remove_dish(name)
            self.update_view() # To clear away the removed ingredient
            return

        # Get all values
        dish_string = f"{name}-"
        for i in range(self.ingredients_tree.topLevelItemCount()):
            ingredient = self.ingredients_tree.topLevelItem(i)

            ingredient_name = ingredient.treeWidget().itemWidget(ingredient, 0).currentText()
            amount = ingredient.treeWidget().itemWidget(ingredient, 1).text()
            unit = ingredient.text(2)

            if not ingredient_name:
                continue

            dish_string += f"{ingredient_name}:{amount} {unit},"

        dish_string = dish_string[:-1]

        # Add ingredient
        if self.tab_widget.currentIndex() == 0: # add
            self.txter.add_dish(dish_string)
            self.clear_values()
        elif self.tab_widget.currentIndex() == 1: # edit
            self.txter.edit_dish(dish_string)
        else:
            print("Error: Tab not recognised!")
            return
