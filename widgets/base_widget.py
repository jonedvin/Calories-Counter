from PyQt6.QtWidgets import QWidget, QMainWindow



class BaseMainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setAllEnabled(self, enable: bool):
        """ Sets all widgets to enable. """
        layout = self.centralWidget().layout()
        for widget in (layout.itemAt(i).widget() for i in range(layout.count())):
            widget.setEnabled(enable)
            



class BaseWidget(QWidget):
    def __init__(self, mainWindow, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mainWindow = mainWindow

    def setAllEnabled(self, enable: bool):
        """ Calls self.mainWindow.setAllEnabled(enable). """
        self.mainWindow.setAllEnabled(enable)
    
    def setEnabled(self, enable: bool) -> None:
        """ Sets itself and all child widgets to enable. """
        for widget in (self.layout().itemAt(i).widget() for i in range(self.layout().count())):
            widget.setEnabled(enable)
            
        return super().setEnabled(enable)