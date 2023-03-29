from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from datetime import datetime, time, timedelta

import matplotlib.dates as mdates
import matplotlib.pyplot as plt



class GraphWidget(QWidget):
    # Constants
    UserIdIndex = 0
    TimestampIndex = 1
    Meal_nameIndex = 2
    CaloriesIndex = 3
    FatIndex = 4
    SaturatedFatIndex = 5
    CarbohydratesIndex = 6
    SugarIndex = 7
    ProteinIndex = 8
    SaltIndex = 9

    def __init__(self, *args, **kwargs):
        """ Class for displaying a matplotlib graph. """
        super().__init__(*args, **kwargs)

        self.plot_figure = plt.figure(facecolor="#e5e5e5")
        self.plot_canvas = FigureCanvas(self.plot_figure)

        self.legend_figure = plt.figure(facecolor="#e5e5e5")
        self.legend_canvas = FigureCanvas(self.legend_figure)

        self.legends_tuple = ("Calories",
                              "Fat",
                              "'- of which saturated",
                              "Carbohydrates",
                              "'- of which sugar",
                              "Protein",
                              "Salt")

        # Plot settings 
        plt.rc('font', size=8)
        plt.rc('xtick', labelsize=8)
        plt.rc('ytick', labelsize=8)
        plt.rc('legend', fontsize=8)

        # Build
        self.general_layout = QVBoxLayout()
        self.general_layout.setContentsMargins(0,0,0,0)
        self.general_layout.setSpacing(2)
        self.general_layout.addWidget(self.plot_canvas)
        self.setLayout(self.general_layout)


    def draw_graph(self, meals_list: list, days_back: int):
        """ Draws a graph of the last [days_back] days. """
        meals_list.sort(key = lambda meal: meal[self.TimestampIndex])

        earliest_day = datetime.combine(datetime.today(), time.min) - timedelta(days=days_back)
        earliest_timestamp = datetime.timestamp(earliest_day)

        days = {}
        for meal in meals_list:
            if meal[self.TimestampIndex] >= earliest_timestamp:
                date = datetime.fromtimestamp(meal[self.TimestampIndex]).date()

                if date not in days:
                    days[date] = {
                        "calories": 0,
                        "fat": 0,
                        "saturated_fat": 0,
                        "carbohydrates": 0,
                        "sugar": 0,
                        "protein": 0,
                        "salt": 0
                    }
                
                days[date]["calories"] += meal[self.CaloriesIndex] if meal[self.CaloriesIndex] else 0
                days[date]["fat"] += meal[self.FatIndex] if meal[self.FatIndex] else 0
                days[date]["saturated_fat"] += meal[self.SaturatedFatIndex] if meal[self.SaturatedFatIndex] else 0
                days[date]["carbohydrates"] += meal[self.CarbohydratesIndex] if meal[self.CarbohydratesIndex] else 0
                days[date]["sugar"] += meal[self.SugarIndex] if meal[self.SugarIndex] else 0
                days[date]["protein"] += meal[self.ProteinIndex] if meal[self.ProteinIndex] else 0
                days[date]["salt"] += meal[self.SaltIndex] if meal[self.SaltIndex] else 0

        dates = []
        calories = []
        fat = []
        saturated_fat = []
        carbohydrates = []
        sugar = []
        protein = []
        salt = []

        for day, info in days.items():
            dates.append(day)
            calories.append(info["calories"])
            fat.append(info["fat"])
            saturated_fat.append(info["saturated_fat"])
            carbohydrates.append(info["carbohydrates"])
            sugar.append(info["sugar"])
            protein.append(info["protein"])
            salt.append(info["salt"])


        ##### Draw plot #################################################

        # Clear figure
        self.plot_figure.clear()

        # Calories
        ax = self.plot_figure.add_subplot(211)
        ax.set_xticks([])
        lines = ax.plot(dates, calories, color="#0c1f49")

        # Other nutrients
        ax = self.plot_figure.add_subplot(212)
        lines += ax.plot(dates, fat)
        lines += ax.plot(dates, saturated_fat)
        lines += ax.plot(dates, carbohydrates)
        lines += ax.plot(dates, sugar)
        lines += ax.plot(dates, protein)
        lines += ax.plot(dates, salt)

        # Legend
        ax.legend(lines, self.legends_tuple, 
                  loc='upper center', 
                  bbox_to_anchor=(0.1, -0.35))

        # Format figure
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
        ax.xaxis.set_major_locator(mdates.DayLocator())
        self.plot_figure.autofmt_xdate()
        self.plot_figure.tight_layout(pad = 0, h_pad=0.5)

        # Draw figure
        self.plot_canvas.draw()
