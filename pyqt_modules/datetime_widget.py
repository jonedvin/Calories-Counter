from PyQt6.QtWidgets import QDateEdit, QPushButton, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QComboBox
from PyQt6.QtCore import QDate, pyqtSlot
from datetime import datetime


class DateTimeWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Date
        self.date_edit = QDateEdit(QDate.currentDate(), calendarPopup=True)
        self.date_edit_today_button = QPushButton("Today")
        self.date_section = QHBoxLayout()
        self.date_section.addWidget(self.date_edit)
        self.date_section.addWidget(self.date_edit_today_button)

        # # Time
        self.time = TimeWidget()
        self.time.layout().setContentsMargins(0,0,0,0)
        self.time_section = QHBoxLayout()
        self.time_section.addWidget(self.time)

        # # Build widget
        self.general_layout = QVBoxLayout()
        self.general_layout.setSpacing(0)
        self.general_layout.setContentsMargins(0,0,0,0)
        self.general_layout.addLayout(self.date_section)
        self.general_layout.addLayout(self.time_section)
        self.setLayout(self.general_layout)

        # # Signals
        self.date_edit_today_button.clicked.connect(self.set_date_to_today)

    @pyqtSlot()
    def set_date_to_today(self):
        """ Sets the date of self.date_edit to today"""
        self.date_edit_today_button.clearFocus()
        self.date_edit.calendarWidget().setSelectedDate(QDate.currentDate())

    def get_timestamp(self) -> int:
        """ Returns the timestamp of selected date and time as and int. """
        year = int(self.date_edit.text().split("/")[2])
        month = int(self.date_edit.text().split("/")[1])
        day = int(self.date_edit.text().split("/")[0])
        hour = self.time.hour
        minute = self.time.minute

        return int(datetime.timestamp(datetime(year, month, day, hour, minute)))


class TimeWidget(QWidget):
    def __init__(self, *args, add_now_button: bool = True, init_to_now: bool = True, **kwargs):
        super().__init__(*args, **kwargs)

        self.hour_combobox = LimitedNumberComboBox(0, 23)
        self.separator = QLabel(":")
        self.minute_combobox = LimitedNumberComboBox(0, 59)

        self.time_section = QHBoxLayout()
        self.time_section.setContentsMargins(0,0,0,0)
        self.time_section.setSpacing(2)
        self.time_section.addWidget(self.hour_combobox)
        self.time_section.addWidget(self.separator)
        self.time_section.addWidget(self.minute_combobox)
        self.time_widget = QWidget()
        self.time_widget.setLayout(self.time_section)
        self.time_widget.setFixedWidth(125)

        self.now_button = QPushButton("Now")

        # Build widget
        self.general_layout = QHBoxLayout()
        self.general_layout.setContentsMargins(0,0,0,0)
        self.general_layout.addWidget(self.time_widget)
        if add_now_button:
            self.general_layout.addWidget(self.now_button)
        self.general_layout.addStretch()
        self.setLayout(self.general_layout)

        # Init
        if init_to_now:
            self.set_time_to_now()

        # Signal    
        self.now_button.clicked.connect(self.set_time_to_now)

    def set_time_to_now(self):
        """ Sets the time of the widget to now. """
        self.hour_combobox.setCurrentNumber(datetime.now().hour)
        self.minute_combobox.setCurrentNumber(datetime.now().minute)

    @property
    def hour(self) -> int:
        """ Returns the hour set. Returns 0 if blank. """
        return self.hour_combobox.getCurrentNumber()

    @property
    def minute(self) -> int:
        """ Returns the hour set. Returns 0 if blank. """
        return self.minute_combobox.getCurrentNumber()



class LimitedNumberComboBox(QComboBox):
    def __init__(self, bottom_limit: int, top_limit: int, set_editable: bool = True, *args, **kwargs):
        """ QComboBox that only allows integers in given range. """
        super().__init__(*args, **kwargs)

        self.bottom_limit = bottom_limit
        self.top_limit = top_limit
        self.lastText = ""

        self.addItem("")
        for i in range(bottom_limit, top_limit+1):
            self.addItem(str(i))

        self.setEditable(set_editable)
        self.editTextChanged.connect(self.checkText)


    def checkText(self):
        """ Check whether the inputted text satisfy the range constraints. """
        # Allow to remove text
        if len(self.currentText()) == 0:
            self.lastText = self.currentText()
            return

        # Check that it's a number
        try:
            new_number = int(self.currentText())
        except ValueError:
            self.setCurrentText(self.lastText)
            return
        
        # Check range
        if new_number < self.bottom_limit \
        or new_number > self.top_limit:
            self.setCurrentText(self.lastText)
            return

        # Allow new number
        self.lastText = self.currentText()

    def setCurrentNumber(self, number: int):
        """ Sets the current number to given number if it satisfies contraints. """
        self.setCurrentText(str(number))

    @pyqtSlot()
    def getCurrentNumber(self) -> int:
        """ Returns the current number. Returns 0 if blank. """
        if len(self.currentText()) == 0:
            return 0
        return int(self.currentText())
