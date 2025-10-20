def is_fist_closed(landmarks):
    """
    Determina si la mano está cerrada en un puño basado en los landmarks.
    """
    if not landmarks:
        return False

    # Obtener posiciones de landmarks clave
    wrist = landmarks.landmark[0]  # Muñeca
    thumb_tip = landmarks.landmark[4]  # Punta del pulgar
    index_tip = landmarks.landmark[8]  # Punta del índice
    middle_tip = landmarks.landmark[12]  # Punta del medio
    ring_tip = landmarks.landmark[16]  # Punta del anular
    pinky_tip = landmarks.landmark[20]  # Punta del meñique

    # Función para calcular distancia euclidiana
    def distance(p1, p2):
        return ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5

    # Umbral para considerar el dedo cerrado (ajustar según necesidad)
    threshold = 0.15

    # Verificar si todas las puntas de los dedos están cerca de la muñeca
    fingers_closed = (
        distance(thumb_tip, wrist) < threshold and
        distance(index_tip, wrist) < threshold and
        distance(middle_tip, wrist) < threshold and
        distance(ring_tip, wrist) < threshold and
        distance(pinky_tip, wrist) < threshold
    )

    return fingers_closed
