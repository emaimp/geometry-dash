import sys
import cv2
import time
from core import detection, recognition
from .components import charts, stats
from pynput.keyboard import Key, Controller
from PySide6.QtCore import QTimer, Qt, QSize
from PySide6.QtGui import QPixmap, QImage, QIcon, QMovie
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout

"""
Ventana principal de la aplicación
"""
class MainWindow(QWidget):
    # Método de inicialización de la ventana
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control de Gestos")
        self.setWindowIcon(QIcon("app/assets/geometry-dash-icon-150px.png"))
        self.setStyleSheet("background: #f4f4f4;");
        self.resize(1440, 900)

        # Inicializar el detector de manos utilizando el módulo detection
        self.hands = detection.init_hands()
        # Inicializar el controlador de teclado para simular pulsaciones
        self.keyboard = Controller()

        # Variables principales para estadísticas y control del programa
        self.gesture_count = 0 # Contador de gestos detectados en la sesión
        self.last_press_time = 0 # Timestamp del último clic para controlar cooldown
        self.cooldown = 0.1 # Tiempo mínimo entre clicks en segundos para evitar pulsaciones repetidas
        self.cap = None # Objeto de captura de video de OpenCV
        self.running = False # Bandera que indica si la detección está activa
        self.click_timestamps = [] # Lista de timestamps de cada clic realizado
        self.session_start = time.time() # Timestamp del inicio de la sesión actual
        self.time_with_gestures = 0 # Tiempo acumulado (en segundos) cuando hay gestos detectados
        self.time_without_gestures = 0 # Tiempo acumulado (en segundos) sin gestos detectados
        self.clicks_per_minute = [0] * 10 # Lista de clicks por cada minuto en los últimos 10 minutos
        self.clicks_per_hour = [0] * 5 # Lista de clicks por cada hora en las próximas 5 horas

        # Configuración del layout principal dividido en panel izquierdo y derecho
        layout = QHBoxLayout()

        """
        Panel izquierdo: Video y Estadísticas
        """
        left_layout = QVBoxLayout()

        self.video_label = QLabel(self) # Label para mostrar el video de la webcam
        self.video_label.setFixedSize(550, 450)
        # self.video_label.setStyleSheet("border: 2px solid #ffffff;")
        left_layout.addWidget(self.video_label) # Agregar el label de video al layout izquierdo

        # Panel de estadísticas que muestra conteo de gestos y estadísticas
        self.stats = stats.StatsPanel()
        # Agregar el panel de estadísticas al layout izquierdo
        left_layout.addWidget(self.stats)

        """
        Panel derecho: Gráficos (charts)
        """
        right_layout = QVBoxLayout()

        #--- Layout horizontal para los gráficos superiores ---#
        top_charts_layout = QHBoxLayout()
        top_charts_layout.setSpacing(10) # Espaciado entre elementos en la fila de gráficos superiores

        # Gráfico de precisión (accuracy) de gestos detectados vs. clicks
        self.accuracy_chart = charts.AccuracyChart()
        # Agregar gráfico de precisión al layout superior
        top_charts_layout.addWidget(self.accuracy_chart)

        # Gráfico de tiempo de actividad (con/sin gestos)
        self.activity_chart = charts.ActivityTimeChart()
        # Agregar gráfico de actividad al layout superior
        top_charts_layout.addWidget(self.activity_chart)

        # Agregar el layout superior de gráficos al panel derecho
        right_layout.addLayout(top_charts_layout)

        """
        Icono animado de Geometry Dash        
        """
        self.icon_label = QLabel()
        self.icon_movie = QMovie("app/assets/geometry-dash-animated.gif") # Cargar el archivo GIF
        self.icon_movie.setScaledSize(QSize(325, 163)) # Ajustar el tamaño del GIF

        # Asignar el GIF al label
        self.icon_label.setMovie(self.icon_movie)
        # Iniciar la reproducción del GIF
        self.icon_movie.start()
        # Centrar el icono en el layout
        self.icon_label.setAlignment(Qt.AlignCenter)

        # Agregar el icono animado entre los layouts superior e inferior
        right_layout.addWidget(self.icon_label)

        #--- Layout horizontal para los gráficos inferiores ---#
        bottom_charts_layout = QHBoxLayout()
        bottom_charts_layout.setSpacing(10) # Espaciado entre elementos en la fila de gráficos inferiores

        # Gráfico de barras para clicks por minuto (últimos 10 minutos)
        self.clicks_per_minute_chart = charts.ClicksPerMinuteChart()
        # Agregar gráfico de clicks por minuto al layout inferior
        bottom_charts_layout.addWidget(self.clicks_per_minute_chart)

        # Gráfico de líneas para clicks por hora (próximas 5 horas)
        self.clicks_line_chart = charts.ClicksLineChart()
        # Agregar gráfico de líneas al layout inferior
        bottom_charts_layout.addWidget(self.clicks_line_chart)

        # Agregar el layout inferior de gráficos al panel derecho
        right_layout.addLayout(bottom_charts_layout)

        # Agregar los paneles izquierdo y derecho al layout principal horizontal
        layout.addLayout(left_layout)
        layout.addLayout(right_layout)

        self.timer = QTimer() # Configurar temporizador para actualizar el video
        self.timer.timeout.connect(self.update_frame) # Conectar el timeout del temporizador al método update_frame

        self.start_detection() # Iniciar la detección de gestos y captura de video
        self.setLayout(layout) # Establecer el layout principal en la ventana

    # Método para iniciar la detección de gestos y captura de video
    def start_detection(self):
        # Verificar si ya está corriendo para evitar inicializaciones múltiples
        if not self.running:
            # Inicializar captura de video desde la cámara predeterminada (índice 0)
            self.cap = cv2.VideoCapture(0) # Cámara predeterminada
            # Verificar si la webcam se abrió correctamente
            if not self.cap.isOpened():
                # Mostrar mensaje de error en el panel de estadísticas
                self.stats.set_error_message("Error: No se pudo abrir la webcam")
                return
            # Marcar como corriendo y iniciar el temporizador
            self.running = True
            # Iniciar el temporizador con intervalo (FPS)
            self.timer.start(30) # FPS

    # Método que se ejecuta cada iteración del temporizador para procesar frames de video
    def update_frame(self):
        # Verificar que la detección esté activa y la captura funcione
        if not self.running or not self.cap:
            return

        # Leer el siguiente frame de la webcam
        ret, frame = self.cap.read()
        # Si no se pudo leer el frame, salir
        if not ret:
            return

        # Voltear el frame horizontalmente para crear efecto espejo
        frame = cv2.flip(frame, 1)

        # Intentar detectar landmarks (puntos de referencia) de la mano en el frame
        try:
            landmarks = detection.detect_hand(frame, self.hands)
        except KeyboardInterrupt:
            # Manejar interrupción de teclado (Ctrl+C) cerrando la aplicación
            self.closeEvent(None)
            return

        # Dibujar los landmarks detectados sobre el frame de video
        detection.draw_hand_landmarks(frame, landmarks)

        # Verificar si se detecta el gesto de contacto entre pulgar e índice (pellizco)
        current_gesture = recognition.is_thumb_index_contact_gesture(landmarks)
        if current_gesture:
            # Acumular tiempo con gesto detectado (aprox. 0.03s por frame a 30 FPS)
            self.time_with_gestures += 0.03  # Acumular tiempo con gesto (~30 FPS)
            # Incrementar contador de gestos
            self.gesture_count += 1
            # Obtener timestamp actual
            current_time = time.time()
            # Verificar si ha pasado el tiempo de cooldown desde el último clic
            if current_time - self.last_press_time > self.cooldown:
                # Simular pulsación de la tecla flecha arriba
                self.keyboard.press(Key.up)
                self.keyboard.release(Key.up)
                # Actualizar timestamp del último clic
                self.last_press_time = current_time
                # Agregar timestamp a la lista de clicks
                self.click_timestamps.append(current_time)
                # Calcular índice para actualizar estadísticas por minuto
                minute_index = int((current_time - self.session_start) / 60)
                if minute_index < 10:
                    self.clicks_per_minute[minute_index] += 1
                # Calcular índice para actualizar estadísticas por hora
                hour_index = int((current_time - self.session_start) / 3600)
                if hour_index < 5:
                    self.clicks_per_hour[hour_index] += 1
        else:
            # Acumular tiempo sin gesto detectado
            self.time_without_gestures += 0.03 # Acumular tiempo sin gesto

        # Convertir el frame de OpenCV (BGR) a formato RGB para Qt
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame_rgb.shape
        bytes_per_line = ch * w
        # Crear objeto QImage desde los datos RGB
        qt_image = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        # Convertir QImage a QPixmap para mostrar en QLabel
        pixmap = QPixmap.fromImage(qt_image)

        self.video_label.setPixmap(pixmap) # Actualizar el label de video con el nuevo frame procesado
        self.stats.update_gesture_count(self.gesture_count) # Actualizar el contador de gestos

        # Calcular total de clicks y actualizar en el panel
        total_clicks = len(self.click_timestamps)
        self.stats.update_total_clicks(total_clicks)

        # Si hay clicks registrados, calcular estadísticas de intervalos
        if total_clicks > 0:
            # Verificar si hay suficientes timestamps para calcular intervalos
            if len(self.click_timestamps) > 1:
                # Calcular intervalos entre clicks consecutivos
                intervals = [self.click_timestamps[i+1] - self.click_timestamps[i] for i in range(len(self.click_timestamps)-1)]
                # Calcular promedio, mínimo y máximo de intervalos
                avg_interval = sum(intervals) / len(intervals)
                min_interval = min(intervals)
                max_interval = max(intervals)
            else:
                # Si solo hay un click, intervalos son cero
                avg_interval = 0
                min_interval = 0
                max_interval = 0

            # Actualizar estadísticas de tiempo promedio y min/max en el panel
            self.stats.update_avg_time(avg_interval)
            self.stats.update_min_max(min_interval, max_interval)
        else:
            # Sin clicks, actualizar con valores predeterminados
            self.stats.update_avg_time(0.00)
            self.stats.update_min_max(0.00, 0.00)

        # Actualizar todos los gráficos con los nuevos datos
        self.accuracy_chart.update_data(self.gesture_count, total_clicks)
        self.activity_chart.update_data(self.time_with_gestures, self.time_without_gestures)
        self.clicks_per_minute_chart.update_data(self.clicks_per_minute)
        self.clicks_line_chart.update_data(self.clicks_per_hour)

    # Evento que se ejecuta cuando la ventana se muestra inicialmente
    def showEvent(self, event):
        # Llamar al método padre
        super().showEvent(event)
        # Obtener la instancia de la aplicación y la geometría disponible de la pantalla
        app = QApplication.instance()
        screen = app.primaryScreen().availableGeometry()
        # Calcular coordenadas para centrar la ventana
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        # Mover la ventana al centro de la pantalla
        self.move(x, y)

    # Evento que se ejecuta cuando se cierra la aplicación
    def closeEvent(self, event):
        # Detener la detección y recursos
        self.running = False
        # Liberar la captura de video si existe
        if self.cap:
            self.cap.release()
        # Detener el temporizador
        self.timer.stop()
        # Aceptar el evento de cierre
        if event:
            event.accept()

# Punto de entrada principal para ejecutar la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv) # Crear instancia de la aplicación Qt
    window = MainWindow() # Crear instancia de la ventana principal
    window.show() # Mostrar la ventana
    sys.exit(app.exec()) # Ejecuta el bucle de eventos de Qt / Sale con el código de retorno
