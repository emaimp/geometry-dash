import sys
import cv2
import time
from core import detection, recognition
from .components import charts, stats_panel
from pynput.keyboard import Key, Controller
from PySide6.QtCore import QTimer, Qt, QSize
from PySide6.QtGui import QPixmap, QImage, QIcon, QMovie
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control de Gestos")
        self.setWindowIcon(QIcon("app/assets/geometry-dash-icon-150px.png"))
        self.resize(1440, 900)  # Establecer tamaño inicial

        # Inicializar detector de manos y controlador de teclado
        self.hands = detection.init_hands()
        self.keyboard = Controller()

        # Variables principales para estadísticas y control
        self.gesture_count = 0 # Contador de gestos detectados
        self.last_press_time = 0 # Timestamp del último clic
        self.cooldown = 0.1 # Tiempo mínimo entre clicks (segundos)
        self.cap = None # Captura de video
        self.running = False # Estado de la detección
        self.click_timestamps = [] # Lista de timestamps de clicks
        self.session_start = time.time() # Inicio de la sesión
        self.time_with_gestures = 0 # Tiempo acumulado con gestos
        self.time_without_gestures = 0 # Tiempo acumulado sin gestos
        self.clicks_per_minute = [0] * 10 # Clicks por cada minuto (últimos 10)
        self.clicks_per_hour = [0] * 5 # Clicks por cada hora (próximas 5)

        # Layout principal dividido en izquierda y derecha
        layout = QHBoxLayout()

        # Panel izquierdo: video y estadísticas básicas
        left_layout = QVBoxLayout()

        # Video label
        self.video_label = QLabel(self)
        self.video_label.setFixedSize(550, 450)
        self.video_label.setStyleSheet("border: 2px solid white;")
        left_layout.addWidget(self.video_label)

        # Panel de estadísticas
        self.stats_panel = stats_panel.StatsPanel()
        left_layout.addWidget(self.stats_panel)

        # Panel derecho: gráficos
        right_layout = QVBoxLayout()

        # Charts layout top
        top_charts_layout = QHBoxLayout()

        self.accuracy_chart = charts.AccuracyChart()
        top_charts_layout.addWidget(self.accuracy_chart)

        self.activity_chart = charts.ActivityTimeChart()
        top_charts_layout.addWidget(self.activity_chart)

        right_layout.addLayout(top_charts_layout)

        # Icon label
        self.icon_label = QLabel()
        self.icon_movie = QMovie("app/assets/geometry-dash-animated.gif")
        self.icon_movie.setScaledSize(QSize(325, 163))
        self.icon_label.setMovie(self.icon_movie)
        self.icon_movie.start()
        self.icon_label.setAlignment(Qt.AlignCenter)

        # Icon between charts
        right_layout.addWidget(self.icon_label)

        # Charts layout bottom
        bottom_charts_layout = QHBoxLayout()

        self.clicks_per_minute_chart = charts.ClicksPerMinuteChart()
        bottom_charts_layout.addWidget(self.clicks_per_minute_chart)

        self.clicks_line_chart = charts.ClicksLineChart()
        bottom_charts_layout.addWidget(self.clicks_line_chart)

        right_layout.addLayout(bottom_charts_layout)

        # Agregar paneles al layout principal
        layout.addLayout(left_layout)
        layout.addLayout(right_layout)

        self.setLayout(layout)

        # Establecer degradado de fondo
        self.setStyleSheet("background: #202020;");

        # Timer for updating video
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        # Start detection
        self.start_detection()

    def start_detection(self):
        # Iniciar captura de video y timer para procesamiento
        if not self.running:
            self.cap = cv2.VideoCapture(0)  # Cámara predeterminada
            if not self.cap.isOpened():
                self.stats_panel.set_error_message("Error: No se pudo abrir la webcam")
                return
            self.running = True
            self.timer.start(30)  # ~30 FPS

    def update_frame(self):
        # Método llamado por el timer para procesar cada frame
        if not self.running or not self.cap:
            return

        ret, frame = self.cap.read()
        if not ret:
            return

        # Voltear frame horizontalmente para efecto espejo
        frame = cv2.flip(frame, 1)

        # Detectar landmarks de la mano
        try:
            landmarks = detection.detect_hand(frame, self.hands)
        except KeyboardInterrupt:
            # Manejar interrupción de teclado (Ctrl+C)
            self.closeEvent(None)
            return

        # Dibujar landmarks en el frame
        detection.draw_hand_landmarks(frame, landmarks)

        # Verificar si se detecta el gesto de pellizco
        current_gesture = recognition.is_thumb_index_contact_gesture(landmarks)
        if current_gesture:
            self.time_with_gestures += 0.03  # Acumular tiempo con gesto (~30 FPS)
            self.gesture_count += 1
            current_time = time.time()
            if current_time - self.last_press_time > self.cooldown:
                # Simular presión de tecla y registrar clic
                self.keyboard.press(Key.up)
                self.keyboard.release(Key.up)
                self.last_press_time = current_time
                self.click_timestamps.append(current_time)
                # Actualizar contadores por minuto y hora
                minute_index = int((current_time - self.session_start) / 60)
                if minute_index < 10:
                    self.clicks_per_minute[minute_index] += 1
                hour_index = int((current_time - self.session_start) / 3600)
                if hour_index < 5:
                    self.clicks_per_hour[hour_index] += 1
        else:
            self.time_without_gestures += 0.03  # Acumular tiempo sin gesto

        # Convertir a QImage
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame_rgb.shape
        bytes_per_line = ch * w
        qt_image = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)

        # Actualizar label
        self.video_label.setPixmap(pixmap)

        # Actualizar estadísticas
        self.stats_panel.update_gesture_count(self.gesture_count)

        total_clicks = len(self.click_timestamps)
        self.stats_panel.update_total_clicks(total_clicks)

        if total_clicks > 0:
            if len(self.click_timestamps) > 1:
                intervals = [self.click_timestamps[i+1] - self.click_timestamps[i] for i in range(len(self.click_timestamps)-1)]
                avg_interval = sum(intervals) / len(intervals)
                min_interval = min(intervals)
                max_interval = max(intervals)
            else:
                avg_interval = 0
                min_interval = 0
                max_interval = 0

            self.stats_panel.update_avg_time(avg_interval)
            self.stats_panel.update_min_max(min_interval, max_interval)
        else:
            self.stats_panel.update_avg_time(0.00)
            self.stats_panel.update_min_max(0.00, 0.00)

        # Actualizar gráficos
        self.accuracy_chart.update_data(self.gesture_count, total_clicks)
        self.activity_chart.update_data(self.time_with_gestures, self.time_without_gestures)
        self.clicks_per_minute_chart.update_data(self.clicks_per_minute)
        self.clicks_line_chart.update_data(self.clicks_per_hour)

    def showEvent(self, event):
        super().showEvent(event)
        # Recalcular y mover la ventana al centro de la pantalla
        app = QApplication.instance()
        screen = app.primaryScreen().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def closeEvent(self, event):
        self.running = False
        if self.cap:
            self.cap.release()
        self.timer.stop()
        if event:
            event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
