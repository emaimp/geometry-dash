import cv2

def init_capture():
    """
    Inicializa la captura de video desde la webcam.
    """
    cap = cv2.VideoCapture(0)  # 0 para la webcam predeterminada
    if not cap.isOpened():
        raise ValueError("No se pudo abrir la webcam")
    return cap

def get_frame(cap):
    """
    Obtiene un frame de la captura de video.
    """
    ret, frame = cap.read()
    if not ret:
        return None
    return frame

def release_capture(cap):
    """
    Libera la captura de video.
    """
    cap.release()
