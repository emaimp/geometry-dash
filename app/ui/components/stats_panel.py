from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout

class StatsPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Layout principal vertical
        self.main_layout = QVBoxLayout(self)

        # Primera fila: contadores
        counters_layout = QHBoxLayout()
        self.main_layout.addLayout(counters_layout)

        # Contenedor para gestos detectados
        self.counter_container = QWidget()
        self.counter_container.setStyleSheet("""
            QWidget {
                border-radius: 3px;
                padding: 5px;
            }
        """)
        counter_layout = QVBoxLayout(self.counter_container)
        self.counter_label = QLabel("Gestos Detectados: 0", self.counter_container)
        self.counter_label.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #065a80, stop:1 #0f233d);
                border-radius: 3px;
                padding: 5px;
                color: #ffffff;
                font-weight: bold;
                font-size: 16px;
                qproperty-alignment: AlignCenter;
            }
        """)
        counter_layout.addWidget(self.counter_label)
        counters_layout.addWidget(self.counter_container)

        # Contenedor para clicks totales
        self.total_container = QWidget()
        self.total_container.setStyleSheet("""
            QWidget {
                border-radius: 3px;
                padding: 5px;
            }
        """)
        total_layout = QVBoxLayout(self.total_container)
        self.total_label = QLabel("Clicks Totales: 0", self.total_container)
        self.total_label.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #065a80, stop:1 #0f233d);
                border-radius: 3px;
                padding: 5px;
                color: #ffffff;
                font-weight: bold;
                font-size: 16px;
                qproperty-alignment: AlignCenter;
            }
        """)
        total_layout.addWidget(self.total_label)
        counters_layout.addWidget(self.total_container)

        # Segunda fila: tiempos
        times_layout = QHBoxLayout()
        self.main_layout.addLayout(times_layout)

        # Contenedor para tiempo promedio
        self.avg_container = QWidget()
        self.avg_container.setStyleSheet("""
            QWidget {
                border-radius: 3px;
                padding: 5px;
            }
        """)
        avg_layout = QVBoxLayout(self.avg_container)
        self.avg_label = QLabel("Tiempo Promedio: 0.00s", self.avg_container)
        self.avg_label.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #065a80, stop:1 #0f233d);
                border-radius: 3px;
                padding: 5px;
                color: #ffffff;
                font-weight: bold;
                font-size: 16px;
                qproperty-alignment: AlignCenter;
            }
        """)
        avg_layout.addWidget(self.avg_label)
        times_layout.addWidget(self.avg_container)

        # Contenedor para min/max
        self.min_max_container = QWidget()
        self.min_max_container.setStyleSheet("""
            QWidget {
                border-radius: 3px;
                padding: 5px;
            }
        """)
        min_max_layout = QVBoxLayout(self.min_max_container)
        self.min_max_label = QLabel("Min/Max: 0.00s / 0.00s", self.min_max_container)
        self.min_max_label.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #065a80, stop:1 #0f233d);
                border-radius: 3px;
                padding: 5px;
                color: #ffffff;
                font-weight: bold;
                font-size: 16px;
                qproperty-alignment: AlignCenter;
            }
        """)
        min_max_layout.addWidget(self.min_max_label)
        times_layout.addWidget(self.min_max_container)

        self.setLayout(self.main_layout)

        # Variables para tracking de cambios y resaltado
        self.current_gesture_count = 0
        self.current_total_clicks = 0
        self.highlight_timer = QTimer(self)
        self.highlight_timer.timeout.connect(self.reset_highlight)
        self.highlighted_labels = set()

    def update_gesture_count(self, count):
        if count != self.current_gesture_count:
            self.current_gesture_count = count
            self.highlight_label(self.counter_label)
        self.counter_label.setText(f"Gestos Detectados: {count}")

    def update_total_clicks(self, total):
        if total != self.current_total_clicks:
            self.current_total_clicks = total
            self.highlight_label(self.total_label)
        self.total_label.setText(f"Clicks Totales: {total}")

    def update_avg_time(self, avg_time):
        self.avg_label.setText(f"Tiempo Promedio: {avg_time:.2f}s")

    def update_min_max(self, min_time, max_time):
        self.min_max_label.setText(f"Min/Max: {min_time:.2f}s / {max_time:.2f}s")

    def highlight_label(self, label):
        if label not in self.highlighted_labels:
            self.highlighted_labels.add(label)
            original_style = label.styleSheet()
            label.setProperty("original_style", original_style)
            # Resaltar con color sólido azul
            highlighted_style = """
            QLabel {
                background-color: #c7e85b;
                border-radius: 3px;
                padding: 5px;
                color: #000000;
                font-weight: bold;
                font-size: 16px;
                qproperty-alignment: AlignCenter;
            }
            """
            label.setStyleSheet(highlighted_style)
            self.highlight_timer.start(500)

    def reset_highlight(self):
        for label in list(self.highlighted_labels):
            original_style = label.property("original_style")
            if original_style:
                label.setStyleSheet(original_style)
            label.setProperty("original_style", None)
        self.highlighted_labels.clear()
        self.highlight_timer.stop()

    def set_error_message(self, message):
        self.counter_label.setText(message)
