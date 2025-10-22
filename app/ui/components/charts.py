from PySide6.QtCore import Qt
from PySide6.QtCharts import QChart, QChartView, QPieSeries, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis, QLineSeries

class AccuracyChart(QChartView):
    # Gráfico de torta para precisión de detección (gestos vs clicks)
    def __init__(self):
        super().__init__()
        self.series = QPieSeries()
        self.series.append("Gestos Detectados", 0)
        self.series.append("Clicks Realizados", 0)

        chart = QChart()
        chart.addSeries(self.series)
        chart.setTitle("Precisión de Detección")
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        self.setChart(chart)
        self.setFixedSize(400, 300)  # Tamaño fijo del gráfico

    def update_data(self, gestures_detected, clicks_performed):
        # Actualizar datos del gráfico de torta
        self.series.clear()
        self.series.append("Gestos Detectados", gestures_detected)
        self.series.append("Clicks Realizados", clicks_performed)

class ActivityTimeChart(QChartView):
    # Gráfico de torta para tiempo de sesión con/sin gestos
    def __init__(self):
        super().__init__()
        self.series = QPieSeries()
        self.series.append("Tiempo con Gestos", 0)
        self.series.append("Tiempo sin Gestos", 0)

        chart = QChart()
        chart.addSeries(self.series)
        chart.setTitle("Tiempo de Sesión por Actividad")
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        self.setChart(chart)
        self.setFixedSize(400, 300)

    def update_data(self, time_with_gestures, time_without_gestures):
        # Actualizar datos del gráfico de torta
        self.series.clear()
        self.series.append("Tiempo con Gestos", time_with_gestures)
        self.series.append("Tiempo sin Gestos", time_without_gestures)

class ClicksPerMinuteChart(QChartView):
    # Gráfico de barras para clicks por minuto (últimos 10 min)
    def __init__(self):
        super().__init__()
        self.bar_set = QBarSet("Clicks")
        self.series = QBarSeries()
        self.series.append(self.bar_set)

        # Inicializar con 10 minutos
        self.categories = [f"{i}-{i+1}" for i in range(10)]
        self.bar_set.append([0] * 10)

        chart = QChart()
        chart.addSeries(self.series)
        chart.setTitle("Clicks por Minuto (Últimos 10 min)")

        axis_x = QBarCategoryAxis()
        axis_x.append(self.categories)
        chart.addAxis(axis_x, Qt.AlignBottom)
        self.series.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setRange(0, 1000)
        chart.addAxis(axis_y, Qt.AlignLeft)
        self.series.attachAxis(axis_y)

        self.setChart(chart)
        self.setFixedSize(400, 300)

    def update_data(self, clicks_per_minute_list):
        # Actualizar datos del gráfico de barras
        self.bar_set.remove(0, self.bar_set.count())
        for val in clicks_per_minute_list:
            self.bar_set.append(val)

class ClicksLineChart(QChartView):
    # Gráfico de líneas para clicks por hora (próximas 5 horas)
    def __init__(self):
        super().__init__()
        self.series = QLineSeries()
        self.series.setName("Clicks por Hora")

        # Inicializar con 5 puntos
        for i in range(5):
            self.series.append(i, 0)

        chart = QChart()
        chart.addSeries(self.series)
        chart.setTitle("Clicks por Hora (Próximas 5 horas)")

        axis_x = QValueAxis()
        axis_x.setRange(0, 4)
        axis_x.setLabelFormat("%d")
        chart.addAxis(axis_x, Qt.AlignBottom)
        self.series.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setRange(0, 10000)  # Más alto para horas
        chart.addAxis(axis_y, Qt.AlignLeft)
        self.series.attachAxis(axis_y)

        self.setChart(chart)
        self.setFixedSize(400, 300)

    def update_data(self, clicks_per_hour_list):
        # Actualizar datos del gráfico de líneas
        self.series.clear()
        for i, val in enumerate(clicks_per_hour_list):
            self.series.append(i, val)
