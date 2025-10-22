import cv2
import time
from pynput.keyboard import Key, Controller
from core import detection, capture, recognition

def main():
    # Inicializar componentes
    cap = capture.init_capture()
    hands = detection.init_hands()
    keyboard = Controller()

    # Variables para controlar la simulación de tecla
    last_press_time = 0
    cooldown = 0.01  # Segundos entre presiones
    last_landmarks = None

    print("Presiona 'q' en la ventana de video para salir.")

    try:
        while True:
            frame = capture.get_frame(cap)
            if frame is None:
                break

            # Voltear el frame horizontalmente para efecto espejo
            frame = cv2.flip(frame, 1)

            # Detectar mano cada frame
            last_landmarks = detection.detect_hand(frame, hands)

            # Dibujar landmarks (opcional) usando los últimos landmarks detectados
            detection.draw_hand_landmarks(frame, last_landmarks)

            # Verificar si el gesto de contacto pulgar-índice está activo usando los últimos landmarks
            if recognition.is_thumb_index_contact_gesture(last_landmarks):
                current_time = time.time()
                if current_time - last_press_time > cooldown:
                    keyboard.press(Key.space)
                    keyboard.release(Key.space)
                    last_press_time = current_time
                    print("Tecla 'espacio' presionada")

            # Redimensionar el frame para reducir el tamaño de la ventana
            display_frame = cv2.resize(frame, (400, 400)) # Ancho, Alto

            # Mostrar frame
            cv2.imshow('Hand Detection', display_frame)

            # Salir con 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("Interrupción detectada")

    finally:
        # Liberar recursos
        capture.release_capture(cap)
        cv2.destroyAllWindows()
        print("Recursos liberados")

if __name__ == "__main__":
    main()
