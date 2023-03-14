from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel
from gui.make_meal_gui import MakeMealWidget

class MainWindow(QMainWindow):
    WindowWidth = 500
    WindowHeight = 600

    def __init__(self):
        super().__init__()
        
        self.resize(self.WindowWidth, self.WindowHeight)

        self.add_meal_widget = MakeMealWidget()
        
        self.general_layout = QVBoxLayout()
        self.general_layout.addWidget(self.add_meal_widget)
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.general_layout)
        self.setCentralWidget(self.central_widget)
