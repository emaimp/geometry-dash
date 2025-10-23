from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter
from PySide6.QtCharts import QChart, QChartView, QPieSeries, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis, QLineSeries

class AccuracyChart(QChartView):
    # Gráfico de torta para precisión de detección (gestos vs clicks)
    def __init__(self):
        super().__init__()
        # Antialiasing para suavizar los bordes del gráfico
        self.setRenderHint(QPainter.Antialiasing)
        # Crear una nueva serie de tipo torta para representar los datos
        self.series = QPieSeries()

        chart = QChart() # Crear un objeto QChart para contener la serie y configuraciones
        chart.addSeries(self.series) # Agregar la serie de torta al gráfico
        chart.setTitle("Precisión de Detección")
        chart.setTheme(QChart.ChartThemeBlueCerulean)
        chart.setAnimationOptions(QChart.NoAnimation) # Deshabilitar animaciones para un rendimiento más rápido
        chart.legend().setVisible(True) # Hacer visible la leyenda del gráfico
        chart.legend().setAlignment(Qt.AlignBottom) # Alinear la leyenda en la parte inferior del gráfico

        self.setChart(chart) # Asignar el gráfico configurado a la vista

    def update_data(self, gestures_detected, clicks_performed):
        # Método para actualizar los datos del gráfico de torta
        self.series.clear()  # Limpiar la serie actual antes de agregar nuevos datos
        total = gestures_detected + clicks_performed # Calcular el total de gestos y clicks para determinar porcentajes
        if total > 0:
            # Agregar segmento para gestos detectados
            slice_gestures = self.series.append("Gestos Detectados", gestures_detected)
            slice_gestures.setLabelVisible(False) # Ocultar la etiqueta del segmento para simplicidad
            slice_gestures.setColor(QColor("#007cff"))
            # Agregar segmento para clicks realizados
            slice_clicks = self.series.append("Clicks Realizados", clicks_performed)
            slice_clicks.setLabelVisible(False) # Ocultar la etiqueta del segmento
            slice_clicks.setColor(QColor("#ff0000"))
        else:
            # Si no hay datos, mostrar un segmento de "Sin Datos"
            slice_no_data = self.series.append("Sin Datos", 1)
            slice_no_data.setLabelVisible(False) # Ocultar la etiqueta
            slice_no_data.setColor(QColor("#ffd700"))
class ActivityTimeChart(QChartView):
    # Gráfico de torta para tiempo de sesión con/sin gestos
    def __init__(self):
        super().__init__()
        self.setRenderHint(QPainter.Antialiasing) # Habilitar antialiasing para bordes suaves
        self.series = QPieSeries() # Crear serie de torta para los datos de tiempo

        chart = QChart() # Crear el gráfico
        chart.addSeries(self.series) # Agregar la serie al gráfico
        chart.setTitle("Tiempo de Sesión por Actividad")
        chart.setTheme(QChart.ChartThemeBlueCerulean)
        chart.setAnimationOptions(QChart.NoAnimation) # Deshabilitar animaciones
        chart.legend().setVisible(True) # Hacer visible la leyenda
        chart.legend().setAlignment(Qt.AlignBottom) # Alinear la leyenda en la parte inferior

        self.setChart(chart) # Asignar el gráfico a la vista

    def update_data(self, time_with_gestures, time_without_gestures):
        # Método para actualizar los datos del gráfico de tiempo de sesión
        self.series.clear() # Limpiar la serie
        total = time_with_gestures + time_without_gestures # Calcular total de tiempo
        if total > 0:
            # Agregar segmento para tiempo con gestos
            slice_with = self.series.append("Tiempo con Gestos", time_with_gestures)
            slice_with.setLabelVisible(False) # Ocultar etiqueta
            slice_with.setColor(QColor("#007cff"))
            # Agregar segmento para tiempo sin gestos
            slice_without = self.series.append("Tiempo sin Gestos", time_without_gestures)
            slice_without.setLabelVisible(False) # Ocultar etiqueta
            slice_without.setColor(QColor("#ff0000"))
        else:
            slice_no_data = self.series.append("Sin Datos", 1)
            slice_no_data.setLabelVisible(False) # Ocultar etiqueta
            slice_no_data.setColor(QColor("#ffd700"))

class ClicksPerMinuteChart(QChartView):
    # Gráfico de barras para clicks por minuto (últimos 10 min)
    def __init__(self):
        super().__init__()
        self.bar_set = QBarSet("Clicks") # Crear conjunto de barras con nombre "Clicks"
        self.bar_set.setColor(QColor("#007cff"))
        self.series = QBarSeries() # Crear serie de barras y agregar el conjunto
        self.series.append(self.bar_set)

        # Inicializar categorías para los últimos 10 minutos (0-1, 1-2, ..., 9-10)
        self.categories = [f"{i}-{i+1}" for i in range(10)]
        self.bar_set.append([0] * 10) # Inicializar valores en cero para cada minuto

        chart = QChart() # Crear el gráfico
        chart.addSeries(self.series) # Agregar la serie de barras al gráfico
        chart.setTitle("Clicks por Minuto (Últimos 10 min)")
        chart.setTheme(QChart.ChartThemeBlueCerulean)
        chart.setAnimationOptions(QChart.AllAnimations) # Habilitar todas las animaciones para transiciones suaves

        axis_x = QBarCategoryAxis() # Crear eje X categórico para las barras
        axis_x.append(self.categories) # Agregar las categorías de minutos
        chart.addAxis(axis_x, Qt.AlignBottom) # Adjuntar eje X al gráfico y a la serie
        self.series.attachAxis(axis_x)

        self.axis_y = QValueAxis() # Crear eje Y de valores con rango inicial 0-1000
        self.axis_y.setRange(0, 1000)
        chart.addAxis(self.axis_y, Qt.AlignLeft) # Adjuntar eje Y al gráfico y a la serie
        self.series.attachAxis(self.axis_y)

        self.setChart(chart) # Asignar el gráfico a la vista

    def update_data(self, clicks_per_minute_list):
        # Método para actualizar los datos del gráfico de barras
        self.bar_set.remove(0, self.bar_set.count()) # Remover todos los valores actuales
        for val in clicks_per_minute_list: # Agregar los nuevos valores de la lista
            self.bar_set.append(val)
        if clicks_per_minute_list: # Ajustar el rango del eje Y dinámicamente basado en los valores máximos
            max_val = max(clicks_per_minute_list)
            self.axis_y.setRange(0, max_val * 1.1 if max_val > 0 else 10) # Establecer rango con un margen del 10% sobre el máximo

class ClicksLineChart(QChartView):
    # Gráfico de líneas para clicks por hora (próximas 5 horas)
    def __init__(self):
        super().__init__()
        self.series = QLineSeries() # Crear serie de líneas con nombre
        self.series.setName("Clicks por Hora")
        self.series.setColor(QColor("#007cff"))
        self.series.setPointsVisible(True) # Hacer visibles los puntos en la línea

        for i in range(5): # Inicializar con 5 puntos en cero (para las próximas 5 horas)
            self.series.append(i, 0)

        chart = QChart() # Crear el gráfico
        chart.addSeries(self.series) # Agregar la serie de líneas
        chart.setTitle("Clicks por Hora (Próximas 5 horas)")
        chart.setTheme(QChart.ChartThemeBlueCerulean)
        chart.setAnimationOptions(QChart.AllAnimations) # Habilitar animaciones

        axis_x = QValueAxis() # Crear eje X de valores con rango 0-4 (para horas 0 a 4)
        axis_x.setRange(0, 4)
        axis_x.setLabelFormat("%d") # Formato de etiqueta como entero
        chart.addAxis(axis_x, Qt.AlignBottom) # Adjuntar eje X
        self.series.attachAxis(axis_x)

        self.axis_y = QValueAxis() # Crear eje Y con rango inicial 0-10000 (más alto para horas)
        self.axis_y.setRange(0, 10000)
        chart.addAxis(self.axis_y, Qt.AlignLeft) # Adjuntar eje Y
        self.series.attachAxis(self.axis_y)

        self.setChart(chart) # Asignar gráfico a la vista

    def update_data(self, clicks_per_hour_list):
        # Método para actualizar los datos del gráfico de líneas
        self.series.clear() # Limpiar la serie
        for i, val in enumerate(clicks_per_hour_list): # Agregar nuevos puntos de la lista
            self.series.append(i, val)
        if clicks_per_hour_list: # Ajustar rango del eje Y dinámicamente
            max_val = max(clicks_per_hour_list)
            self.axis_y.setRange(0, max_val * 1.1 if max_val > 0 else 100) # Rango con margen del 10% sobre el máximo
