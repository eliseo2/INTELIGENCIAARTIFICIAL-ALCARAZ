import cv2
import mediapipe as mp
import numpy as np
import math

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Variable para controlar la rotación
angulo_rotacion = 0

# Función para rotar un punto alrededor de un centro
def rotar_punto(x, y, cx, cy, angulo):
    """Rota un punto (x,y) alrededor de (cx,cy) por 'angulo' grados"""
    rad = math.radians(angulo)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    
    # Trasladar al origen
    x -= cx
    y -= cy
    
    # Rotar
    x_nuevo = x * cos_a - y * sin_a
    y_nuevo = x * sin_a + y * cos_a
    
    # Trasladar de vuelta
    return int(x_nuevo + cx), int(y_nuevo + cy)

# Función para determinar la letra según la posición de los dedos
def reconocer_letra(hand_landmarks, frame, angulo):
    h, w, _ = frame.shape  # Tamaño de la imagen
    
    # Obtener coordenadas de los puntos clave en píxeles
    dedos = [(int(hand_landmarks.landmark[i].x * w), int(hand_landmarks.landmark[i].y * h)) for i in range(21)]
    
    # Obtener posiciones clave (puntas de los dedos)
    pulgar, indice, medio, anular, meñique = dedos[4], dedos[8], dedos[12], dedos[16], dedos[20]

    # Mostrar los números de los landmarks en la imagen
    for i, (x, y) in enumerate(dedos):
        cv2.circle(frame, (x, y), 5, (233, 23, 0), -1)  # Puntos azules
        cv2.putText(frame, str(i), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

    # Calcular distancias en píxeles
    distancia_pulgar_indice = np.linalg.norm(np.array(pulgar) - np.array(indice))
    distancia_indice_medio = np.linalg.norm(np.array(indice) - np.array(medio))

    centro_rect = (pulgar[0], pulgar[1])
    
    ancho_rect = max(int(distancia_pulgar_indice), 20) 
    alto_rect = int(ancho_rect * 0.6) 

    p1 = rotar_punto(centro_rect[0] - ancho_rect//2, centro_rect[1] - alto_rect//2, centro_rect[0], centro_rect[1], angulo)
    p2 = rotar_punto(centro_rect[0] + ancho_rect//2, centro_rect[1] - alto_rect//2, centro_rect[0], centro_rect[1], angulo)
    p3 = rotar_punto(centro_rect[0] + ancho_rect//2, centro_rect[1] + alto_rect//2, centro_rect[0], centro_rect[1], angulo)
    p4 = rotar_punto(centro_rect[0] - ancho_rect//2, centro_rect[1] + alto_rect//2, centro_rect[0], centro_rect[1], angulo)
    
    pts = np.array([p1, p2, p3, p4], np.int32)
    overlay = frame.copy()
    cv2.fillPoly(overlay, [pts], (255, 100, 50))
    cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)
    
    cv2.polylines(frame, [pts], True, (255, 150, 100), 3)

    # Lógica para reconocer algunas letras
    if distancia_pulgar_indice < 30 and distancia_indice_medio > 50:
        return "A"
    elif indice[1] < medio[1] and medio[1] < anular[1] and anular[1] < meñique[1]:
        return "B"
    elif distancia_pulgar_indice > 50 and distancia_indice_medio > 50:
        return "C"

    return "Desconocido"

# Captura de video en tiempo real
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    angulo_rotacion = (angulo_rotacion + 2) % 360

    # Convertir a RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Procesar la imagen con MediaPipe
    results = hands.process(frame_rgb)

    # Dibujar puntos de la mano y reconocer letras
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            letra_detectada = reconocer_letra(hand_landmarks, frame, angulo_rotacion)

            cv2.putText(frame, f"Letra: {letra_detectada}", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Mostrar el video
    cv2.imshow("Reconocimiento con Rectangulo Rotatorio", frame)

    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()