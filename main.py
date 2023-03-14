from PyQt6.QtWidgets import QApplication
from gui.main_gui import MainWindow
import sys

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
