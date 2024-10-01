import numpy as np
import cv2 as cv
import mediapipe as mp
import tkinter as tk

# Valor de ajuste para visão
blinkAdjust = 0.15
flip_enabled = True

# Contar uma piscada por vez
is_blinking = False

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Drawing utilities
mp_drawing = mp.solutions.drawing_utils

# Indices for eyes landmarks in the face mesh
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [263, 387, 385, 362, 380, 373]

# Function to calculate the eye aspect ratio (EAR)
def calculate_ear(eye_landmarks):
    vertical_1 = np.linalg.norm(np.array(eye_landmarks[1]) - np.array(eye_landmarks[5]))
    vertical_2 = np.linalg.norm(np.array(eye_landmarks[2]) - np.array(eye_landmarks[4]))
    horizontal = np.linalg.norm(np.array(eye_landmarks[0]) - np.array(eye_landmarks[3]))
    ear = (vertical_1 + vertical_2) / (2.0 * horizontal)
    return ear

# Inicializando variáveis
selected_letters = []  # Para armazenar as letras selecionadas
left_keys = ['Q', 'W', 'E', 'R', 'T', 'A', 'S', 'D', 'F', 'G', 'Z', 'X', 'C', 'V']
right_keys = ['Y', 'U', 'I', 'O', 'P', 'H', 'J', 'K', 'L', 'B', 'N', 'M']
current_keys = (left_keys, right_keys)  # Teclas atuais em exibição

shrink_left = False
shrink_right = False

# Variáveis para rastrear o estado dos olhos
left_eye_closed = False
right_eye_closed = False

# Função para desenhar o teclado atualizado
def draw_keyboard(frame, left_keys, right_keys, selected_letters):
    height, width, _ = frame.shape
    keyboard_height = 200
    extended_frame = np.zeros((height + keyboard_height + 50, width, 3), dtype=np.uint8)
    extended_frame[:height, :width] = frame
    key_width = width // 10
    key_height = 50
    middle_line_x = width // 2

    # Desenhar as teclas na parte esquerda (se houver teclas)
    if left_keys:
        for i, key in enumerate(left_keys):
            x = (i % 5) * key_width  # 5 teclas por linha
            y = height + (i // 5) * key_height
            cv.rectangle(extended_frame, (x, y), (x + key_width, y + key_height), (255, 255, 255), -1)
            cv.putText(extended_frame, key, (x + 10, y + 35), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    # Desenhar as teclas na parte direita (se houver teclas)
    if right_keys:
        for i, key in enumerate(right_keys):
            x = middle_line_x + (i % 5) * key_width
            y = height + (i // 5) * key_height
            cv.rectangle(extended_frame, (x, y), (x + key_width, y + key_height), (255, 255, 255), -1)
            cv.putText(extended_frame, key, (x + 10, y + 35), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    # Exibir as letras selecionadas abaixo do teclado
    cv.putText(extended_frame, "Selected Letters: " + ''.join(selected_letters), (30, height + keyboard_height + 30), 
               cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    return extended_frame

# Função para dividir as teclas em duas partes
def divide_keys(keys):
    mid = len(keys) // 2
    return keys[:mid], keys[mid:]

# Start video capture
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

# Threshold for blinking detection (adjust as necessary)
BLINK_THRESHOLD = blinkAdjust

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if flip_enabled:
        frame = cv.flip(frame, 1)

    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            left_eye_landmarks = [(int(face_landmarks.landmark[i].x * frame.shape[1]), int(face_landmarks.landmark[i].y * frame.shape[0])) for i in LEFT_EYE]
            right_eye_landmarks = [(int(face_landmarks.landmark[i].x * frame.shape[1]), int(face_landmarks.landmark[i].y * frame.shape[0])) for i in RIGHT_EYE]

            left_ear = calculate_ear(left_eye_landmarks)
            right_ear = calculate_ear(right_eye_landmarks)

            # Detectar piscada do olho esquerdo
            if left_ear < BLINK_THRESHOLD and not left_eye_closed:
                if current_keys[1]:  # Se ainda há teclas à direita
                    current_keys = (current_keys[0], [])  # Apaga as teclas do lado direito
                    shrink_right = True
                left_eye_closed = True  # Marca que o olho está fechado

            # Detectar piscada do olho direito
            elif right_ear < BLINK_THRESHOLD and not right_eye_closed:
                if current_keys[0]:  # Se ainda há teclas à esquerda
                    current_keys = ([], current_keys[1])  # Apaga as teclas do lado esquerdo
                    shrink_left = True
                right_eye_closed = True  # Marca que o olho está fechado

            # Verificar se ambos os olhos estão piscando para adicionar um espaço
            if left_ear < BLINK_THRESHOLD and right_ear < BLINK_THRESHOLD:
                if len(selected_letters) == 0 or selected_letters[-1] != ' ':  # Evitar espaços consecutivos
                    selected_letters.append(' ')  # Adiciona um espaço
                left_eye_closed = True
                right_eye_closed = True

            # Verificar se o olho esquerdo foi aberto novamente
            if left_ear >= BLINK_THRESHOLD:
                left_eye_closed = False  # Marca que o olho foi aberto

            # Verificar se o olho direito foi aberto novamente
            if right_ear >= BLINK_THRESHOLD:
                right_eye_closed = False  # Marca que o olho foi aberto

    # Após a remoção das teclas de um lado, dividir as teclas restantes
    if shrink_right and current_keys[0]:  # Se o lado direito foi removido
        shrink_right = False
        current_keys = divide_keys(current_keys[0])  # Divide o lado esquerdo em dois

    elif shrink_left and current_keys[1]:  # Se o lado esquerdo foi removido
        shrink_left = False
        current_keys = divide_keys(current_keys[1])  # Divide o lado direito em dois

    # Se restar apenas uma tecla em qualquer lado, adicionar ao array
    if len(current_keys[0]) == 1 and len(current_keys[1]) == 0:
        selected_letters.append(current_keys[0].pop())
        current_keys = (left_keys, right_keys)  # Reinicia o teclado
    elif len(current_keys[1]) == 1 and len(current_keys[0]) == 0:
        selected_letters.append(current_keys[1].pop())
        current_keys = (left_keys, right_keys)  # Reinicia o teclado

    # Desenhar o teclado e exibir
    frame_with_keyboard = draw_keyboard(frame, current_keys[0], current_keys[1], selected_letters)
    cv.imshow('MediaPipe Face Mesh - Eye Blink Detection with Keyboard', frame_with_keyboard)

    # Controles de teclado
    key = cv.waitKey(1)
    if key == ord('f'):
        flip_enabled = not flip_enabled
    elif key == ord('q'):
        break

# Limpar e fechar janelas
cap.release()
cv.destroyAllWindows()
