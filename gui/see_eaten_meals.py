from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout, QLabel, QTabWidget, QComboBox, QTreeWidget, QTreeWidgetItem
from pyqt_modules.graph_widget import GraphWidget
from modules.databaser import Databaser
from modules.txter import Txter
from modules.user import User


class SeeEatenMealsWidget(QWidget):
    def __init__(self, databaser: Databaser, txter: Txter, *args, **kwargs):
        """ Widget with components for viewing, throwing away and eating made meals. """
        super().__init__(*args, **kwargs)

        self.databaser = databaser
        self.txter = txter

        # User
        self.user_label = QLabel("User:")
        self.user_label.setFixedWidth(35)
        self.user = QComboBox()
        self.time_label = QLabel("Time span:")
        self.time_label.setFixedWidth(65)
        self.time_span = QComboBox()
        self.user_time_section = QHBoxLayout()
        self.user_time_section.addWidget(self.user_label)
        self.user_time_section.addWidget(self.user)
        self.user_time_section.addWidget(self.time_label)
        self.user_time_section.addWidget(self.time_span)
        self.user_time_section.addStretch()
        self.load_time_spans()
        self.load_users()

        # Graph
        self.nutrients_graph = GraphWidget()

        # Build widget
        self.general_layout = QVBoxLayout()
        self.general_layout.addLayout(self.user_time_section)
        self.general_layout.addWidget(self.nutrients_graph)
        self.setLayout(self.general_layout)

        # Signals
        self.user.currentIndexChanged.connect(self.draw_graph)
        self.time_span.currentIndexChanged.connect(self.draw_graph)


    def load_users(self):
        """ Loads registered users and add them to the users QComboBox. """
        users_list = self.databaser.get_users()
        self.user.addItem("", None)
        for user in users_list:
            self.user.addItem(f"{user[0]} {user[1]}", User.fromDatabase(self.databaser, user))


    def load_time_spans(self):
        """ Loads time spans into self.time_span. """
        self.time_span.addItem("Last week", 7-1)
        self.time_span.addItem("Last month", 30-1)
        self.time_span.addItem("Last 2 months", 60-1)
        self.time_span.addItem("Last 3 months", 90-1)
        self.time_span.addItem("Last 6 months", 180-1)
        self.time_span.addItem("Last year", 365-1)


    def draw_graph(self):
        """ Loads the eaten meals for currently selected user. """
        eaten_meals = self.user.currentData().get_eaten_meals()
        self.nutrients_graph.draw_graph(eaten_meals, self.time_span.currentData())

    