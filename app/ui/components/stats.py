from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout

"""
Panel de estadísticas en la interfaz
"""
class StatsPanel(QWidget):
    # Método constructor del panel de estadísticas
    def __init__(self, parent=None):
        # Inicializar QWidget base
        super().__init__(parent)

        # Crear layout vertical principal para organizar los elementos
        self.main_layout = QVBoxLayout(self)

        # Crear layout horizontal para la primera fila de contadores
        counters_layout = QHBoxLayout()
        # Agregar el layout de contadores al layout principal
        self.main_layout.addLayout(counters_layout)

        # Crear contenedor widget para el contador de gestos detectados
        self.counter_container = QWidget()
        # Configurar estilo CSS para el contenedor con borde redondeado y padding
        self.counter_container.setStyleSheet("""
            QWidget {
                border-radius: 3px;
                padding: 5px;
            }
        """)
        # Crear layout vertical para el contenedor del contador
        counter_layout = QVBoxLayout(self.counter_container)
        # Crear label para mostrar el contador de gestos con texto inicial
        self.counter_label = QLabel("Gestos Detectados: 0", self.counter_container)
        # Aplicar estilo CSS con gradiente azul para el label
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
        # Agregar el label al layout del contenedor
        counter_layout.addWidget(self.counter_label)
        # Agregar el contenedor de contador al layout de contadores
        counters_layout.addWidget(self.counter_container)

        # Crear contenedor widget para el contador de clicks totales
        self.total_container = QWidget()
        # Configurar estilo CSS idéntico para consistencia visual
        self.total_container.setStyleSheet("""
            QWidget {
                border-radius: 3px;
                padding: 5px;
            }
        """)
        # Crear layout vertical para el contenedor de clicks totales
        total_layout = QVBoxLayout(self.total_container)
        # Crear label para mostrar clicks totales con texto inicial
        self.total_label = QLabel("Clicks Totales: 0", self.total_container)
        # Aplicar el mismo estilo CSS de gradiente azul
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
        # Agregar el label al layout del contenedor
        total_layout.addWidget(self.total_label)
        # Agregar el contenedor de clicks al layout de contadores
        counters_layout.addWidget(self.total_container)

        # Crear layout horizontal para la segunda fila de tiempos
        times_layout = QHBoxLayout()
        # Agregar el layout de tiempos al layout principal
        self.main_layout.addLayout(times_layout)

        # Crear contenedor para el tiempo promedio entre gestos
        self.avg_container = QWidget()
        # Aplicar estilo CSS consistente para el contenedor
        self.avg_container.setStyleSheet("""
            QWidget {
                border-radius: 3px;
                padding: 5px;
            }
        """)
        # Crear layout vertical para el contenedor de tiempo promedio
        avg_layout = QVBoxLayout(self.avg_container)
        # Crear label para mostrar tiempo promedio con valor inicial
        self.avg_label = QLabel("Tiempo Promedio: 0.00s", self.avg_container)
        # Aplicar estilo CSS de gradiente azul para el label
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
        # Agregar el label al layout del contenedor de promedio
        avg_layout.addWidget(self.avg_label)
        # Agregar el contenedor de promedio al layout de tiempos
        times_layout.addWidget(self.avg_container)

        # Crear contenedor para mostrar tiempo mínimo y máximo entre gestos
        self.min_max_container = QWidget()
        # Configurar estilo CSS idéntico para consistencia
        self.min_max_container.setStyleSheet("""
            QWidget {
                border-radius: 3px;
                padding: 5px;
            }
        """)
        # Crear layout vertical para el contenedor min/max
        min_max_layout = QVBoxLayout(self.min_max_container)
        # Crear label para mostrar min/max con valores iniciales
        self.min_max_label = QLabel("Min/Max: 0.00s / 0.00s", self.min_max_container)
        # Aplicar estilo CSS de gradiente azul
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
        # Agregar el label al layout del contenedor min/max
        min_max_layout.addWidget(self.min_max_label)
        # Agregar el contenedor min/max al layout de tiempos
        times_layout.addWidget(self.min_max_container)

        # Establecer el layout principal como layout del widget
        self.setLayout(self.main_layout)

        # Variables para seguimiento de cambios en los valores y resaltado visual
        self.current_gesture_count = 0  # Valor actual del contador de gestos para detectar cambios
        self.current_total_clicks = 0   # Valor actual de clicks totales para detectar cambios
        self.highlight_timer = QTimer(self)  # Temporizador para controlar el tiempo de resaltado
        self.highlight_timer.timeout.connect(self.reset_highlight) # Conectar el timeout del temporizador a la función de reset
        self.highlighted_labels = set() # Conjunto para mantener registro de labels resaltados

    # Método para actualizar el contador de gestos detectados
    def update_gesture_count(self, count):
        # Verificar si el valor cambió para aplicar resaltado
        if count != self.current_gesture_count:
            # Actualizar el valor actual
            self.current_gesture_count = count
            # Resaltar el label de gestos para indicar cambio
            self.highlight_label(self.counter_label)
        # Actualizar el texto del label con el nuevo conteo
        self.counter_label.setText(f"Gestos Detectados: {count}")

    # Método para actualizar el contador de clicks totales
    def update_total_clicks(self, total):
        # Verificar si el valor cambió para aplicar resaltado
        if total != self.current_total_clicks:
            # Actualizar el valor actual
            self.current_total_clicks = total
            # Resaltar el label de clicks para indicar cambio
            self.highlight_label(self.total_label)
        # Actualizar el texto del label con el nuevo total
        self.total_label.setText(f"Clicks Totales: {total}")

    # Método para actualizar el tiempo promedio entre gestures
    def update_avg_time(self, avg_time):
        # Formatear y mostrar el tiempo promedio con 2 decimales
        self.avg_label.setText(f"Tiempo Promedio: {avg_time:.2f}s")

    # Método para actualizar los tiempos mínimos y máximos entre gestures
    def update_min_max(self, min_time, max_time):
        # Formatear y mostrar min y max con 2 decimales separados por "/"
        self.min_max_label.setText(f"Min/Max: {min_time:.2f}s / {max_time:.2f}s")

    # Método para resaltar visualmente un label cuando cambia su valor
    def highlight_label(self, label):
        # Verificar que el label no esté ya resaltado
        if label not in self.highlighted_labels:
            # Agregar el label al conjunto de resaltados
            self.highlighted_labels.add(label)
            # Guardar el estilo original para poder restaurarlo
            original_style = label.styleSheet()
            label.setProperty("original_style", original_style)
            # Aplicar estilo de resaltado con fondo amarillo verde y texto negro
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
            # Cambiar el estilo del label a resaltado
            label.setStyleSheet(highlighted_style)
            # Iniciar temporizador para quitar el resaltado después de 500ms
            self.highlight_timer.start(500)

    # Método llamado por el temporizador para quitar el resaltado de labels
    def reset_highlight(self):
        # Iterar sobre copia de la lista de labels resaltados
        for label in list(self.highlighted_labels):
            # Recuperar el estilo original guardado como propiedad
            original_style = label.property("original_style")
            if original_style:
                # Restaurar el estilo original del label
                label.setStyleSheet(original_style)
            # Limpiar la propiedad guardada
            label.setProperty("original_style", None)
        # Limpiar el conjunto de labels resaltados
        self.highlighted_labels.clear()
        # Detener el temporizador ya que ya no hay labels resaltados
        self.highlight_timer.stop()

    # Método para mostrar mensajes de error en el panel (reemplaza contador de gestos)
    def set_error_message(self, message):
        # Establecer el mensaje de error como texto del label de gestos
        self.counter_label.setText(message)
