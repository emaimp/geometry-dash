import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils  # Opcional para dibujar landmarks

def init_hands():
    """
    Inicializa el detector de manos de MediaPipe.
    """
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5
    )
    return hands

def detect_hand(frame, hands):
    """
    Detecta la mano en el frame y devuelve los landmarks.
    """
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    if results.multi_hand_landmarks:
        return results.multi_hand_landmarks[0]  # Devuelve landmarks de la primera mano
    return None

def draw_hand_landmarks(frame, landmarks):
    """
    Dibuja los landmarks de la mano en el frame (opcional para depuración).
    """
    if landmarks:
        mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)
