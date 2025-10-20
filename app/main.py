import time
import cv2
from pynput.keyboard import Key, Controller

from capture import init_capture, get_frame, release_capture
from detection import init_hands, detect_hand, draw_hand_landmarks
from recognition import is_fist_closed

def main():
    # Inicializar componentes
    cap = init_capture()
    hands = init_hands()
    keyboard = Controller()

    # Variables para controlar la simulación de tecla
    last_press_time = 0
    cooldown = 0.5  # Segundos entre presiones

    print("Presiona 'q' en la ventana de video para salir.")

    try:
        while True:
            frame = get_frame(cap)
            if frame is None:
                break

            # Detectar mano
            landmarks = detect_hand(frame, hands)

            # Dibujar landmarks (opcional)
            draw_hand_landmarks(frame, landmarks)

            # Verificar si el puño está cerrado
            if is_fist_closed(landmarks):
                current_time = time.time()
                if current_time - last_press_time > cooldown:
                    keyboard.press(Key.space)
                    keyboard.release(Key.space)
                    last_press_time = current_time
                    print("Tecla 'espacio' presionada")

            # Mostrar frame
            cv2.imshow('Hand Detection', frame)

            # Salir con 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("Interrupción detectada")

    finally:
        # Liberar recursos
        release_capture(cap)
        cv2.destroyAllWindows()
        print("Recursos liberados")

if __name__ == "__main__":
    main()
