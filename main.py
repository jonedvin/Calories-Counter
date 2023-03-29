from PyQt6.QtWidgets import QApplication
from gui.main_gui import MainWindow
import sys

if __name__ == "__main__":
    app = QApplication([])

    data_folder_path = None
    if len(sys.argv) > 1:
        data_folder_path = sys.argv[1]

    window = MainWindow(app, data_folder_path)
    window.show()
    sys.exit(app.exec())
