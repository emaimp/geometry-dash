"""
Determina si se realiza el gesto de contactar pulgar e índice.
"""
def is_thumb_index_contact_gesture(landmarks):
    if not landmarks:
        return False

    # Obtiene las posiciones del landmarks
    thumb_tip = landmarks.landmark[4]   # Punta del pulgar
    index_tip = landmarks.landmark[8]   # Punta del índice
    middle_tip = landmarks.landmark[12] # Punta del medio
    ring_tip = landmarks.landmark[16]   # Punta del anular
    pinky_tip = landmarks.landmark[20]  # Punta del meñique

    # Función para calcular distancia euclidiana (incluyendo el eje Z para mayor precisión)
    def distance(p1, p2):
        return ((p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2)**0.5

    # Umbral de distancia entre pulgar e índice para considerar contacto
    threshold_contact = 0.10

    # Umbral para asegurar que el resto de los dedos no están en contacto con el pulgar
    threshold_no_contact = 0.20 # Debe ser mayor para evitar falsos positivos

    # Verificar contacto entre pulgar e índice
    thumb_index_close = distance(thumb_tip, index_tip) < threshold_contact

    # Verificar que el pulgar no esté cerca del medio, anular, meñique (resto cerrados)
    thumb_middle_far = distance(thumb_tip, middle_tip) > threshold_no_contact
    thumb_ring_far = distance(thumb_tip, ring_tip) > threshold_no_contact
    thumb_pinky_far = distance(thumb_tip, pinky_tip) > threshold_no_contact

    # El gesto es válido si pulgar-índice están cerca y pulgar lejos del resto.
    return thumb_index_close and thumb_middle_far and thumb_ring_far and thumb_pinky_far
