from PyQt6.QtWidgets import QDateEdit, QPushButton
from PyQt6.QtCore import pyqtSlot, QDate



class DateTimeWidget(QDateEdit):
    def __init__(self, parent=None):
        super().__init__(parent, calendarPopup=True)
        self._today_button = QPushButton(self.tr("Today"))
        self._today_button.clicked.connect(self._update_today)
        self.calendarWidget().layout().addWidget(self._today_button)

    @pyqtSlot()
    def _update_today(self):
        self._today_button.clearFocus()
        today = QDate.currentDate()
        self.calendarWidget().setSelectedDate(today)