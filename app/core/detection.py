import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils # Dibuja el landmarks

"""
Inicializa el detector de manos de MediaPipe
"""
def init_hands():
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        model_complexity=0, # Modelo más ligero para optimización
        min_detection_confidence=0.2, # Umbral más bajo para detección rápida
        min_tracking_confidence=0.2 # Umbral más bajo para seguimiento rápido
    )
    return hands

"""
Detecta la mano en el frame y devuelve los landmarks
"""
def detect_hand(frame, hands):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resized_rgb_frame = cv2.resize(rgb_frame, (320, 240)) # Reduce a la mitad del tamaño típico (640x480)
    results = hands.process(resized_rgb_frame)

    if results.multi_hand_landmarks:
        return results.multi_hand_landmarks[0] # Devuelve landmarks de la primera mano
    return None

"""
Dibuja los landmarks de la mano en el frame (opcional para depuración)
"""
def draw_hand_landmarks(frame, landmarks):
    if landmarks:
        mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)
