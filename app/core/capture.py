import cv2

"""
Inicializa la captura de video desde la webcam.
"""
def init_capture():
    cap = cv2.VideoCapture(0) # 0 para la webcam predeterminada
    if not cap.isOpened():
        raise ValueError("No se pudo abrir la webcam")
    return cap

"""
Obtiene un frame de la captura de video.
"""
def get_frame(cap):
    ret, frame = cap.read()
    if not ret:
        return None
    return frame

"""
Libera la captura de video.
"""
def release_capture(cap):
    cap.release()
