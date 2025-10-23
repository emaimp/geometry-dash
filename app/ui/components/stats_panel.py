from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QGroupBox

class StatsPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # GroupBox para estadísticas
        self.stats_groupbox = QGroupBox("Mediciones")
        self.stats_groupbox.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #ffffff;
                border-radius: 5px;
                margin-top: 1ex;
                background-color: #006064;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #ffffff;
            }
        """)
        stats_layout = QVBoxLayout()

        # Primera fila: contadores
        counters_layout = QHBoxLayout()

        self.counter_label = QLabel("Gestos Detectados: 0", self)
        self.counter_label.setStyleSheet("""
            QLabel {
                background-color: #e3f2fd;
                border: 1px solid #2196f3;
                border-radius: 3px;
                padding: 5px;
                color: #0d47a1;
                font-weight: bold;
                qproperty-alignment: AlignCenter;
            }
        """)
        counters_layout.addWidget(self.counter_label)

        self.total_label = QLabel("Clicks Totales: 0", self)
        self.total_label.setStyleSheet("""
            QLabel {
                background-color: #e3f2fd;
                border: 1px solid #2196f3;
                border-radius: 3px;
                padding: 5px;
                color: #0d47a1;
                font-weight: bold;
                qproperty-alignment: AlignCenter;
            }
        """)
        counters_layout.addWidget(self.total_label)
        stats_layout.addLayout(counters_layout)

        # Segunda fila: tiempos
        times_layout = QHBoxLayout()

        self.avg_label = QLabel("Tiempo Promedio: 0.00s", self)
        self.avg_label.setStyleSheet("""
            QLabel {
                background-color: #ffebee;
                border: 1px solid #f44336;
                border-radius: 3px;
                padding: 5px;
                color: #b71c1c;
                font-weight: bold;
                qproperty-alignment: AlignCenter;
            }
        """)
        times_layout.addWidget(self.avg_label)

        self.min_max_label = QLabel("Min/Max: 0.00s / 0.00s", self)
        self.min_max_label.setStyleSheet("""
            QLabel {
                background-color: #ffebee;
                border: 1px solid #f44336;
                border-radius: 3px;
                padding: 5px;
                color: #b71c1c;
                font-weight: bold;
                qproperty-alignment: AlignCenter;
            }
        """)
        times_layout.addWidget(self.min_max_label)
        stats_layout.addLayout(times_layout)

        self.stats_groupbox.setLayout(stats_layout)

        # Layout principal del widget
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stats_groupbox)
        self.setLayout(main_layout)

    def update_gesture_count(self, count):
        self.counter_label.setText(f"Gestos Detectados: {count}")

    def update_total_clicks(self, total):
        self.total_label.setText(f"Clicks Totales: {total}")

    def update_avg_time(self, avg_time):
        self.avg_label.setText(f"Tiempo Promedio: {avg_time:.2f}s")

    def update_min_max(self, min_time, max_time):
        self.min_max_label.setText(f"Min/Max: {min_time:.2f}s / {max_time:.2f}s")

    def set_error_message(self, message):
        self.counter_label.setText(message)
