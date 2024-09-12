import numpy as np
import cv2 as cv
import mediapipe as mp

#Valor de ajuste para visão
blinkAdjust = 0.15
flip_enabled = True

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

# Função para desenhar um teclado retangular com uma linha dividindo as teclas
def draw_keyboard(frame):
    # Adicionar um espaço extra para o teclado abaixo da imagem da webcam
    height, width, _ = frame.shape
    keyboard_height = 200  # Definir uma altura maior para o teclado completo
    extended_frame = np.zeros((height + keyboard_height, width, 3), dtype=np.uint8)
    extended_frame[:height, :width] = frame

    # Definir todas as teclas em uma única lista
    keys = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 
            'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 
            'Z', 'X', 'C', 'V', 'B', 'N', 'M']

    # Dividir as teclas em duas partes
    half = len(keys) // 2
    left_keys = keys[:half]
    right_keys = keys[half:]

    # Definir tamanho das teclas e posição da linha divisória
    key_width = width // 10
    key_height = 50
    middle_line_x = width // 2

    # Desenhar as teclas na parte esquerda
    for i, key in enumerate(left_keys):
        x = (i % 5) * key_width  # 5 teclas por linha
        y = height + (i // 5) * key_height  # Nova linha a cada 5 teclas
        cv.rectangle(extended_frame, (x, y), (x + key_width, y + key_height), (255, 255, 255), -1)
        cv.putText(extended_frame, key, (x + 10, y + 35), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    # Desenhar as teclas na parte direita
    for i, key in enumerate(right_keys):
        x = middle_line_x + (i % 5) * key_width  # 5 teclas por linha, depois da linha divisória
        y = height + (i // 5) * key_height
        cv.rectangle(extended_frame, (x, y), (x + key_width, y + key_height), (255, 255, 255), -1)
        cv.putText(extended_frame, key, (x + 10, y + 35), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    # Desenhar a linha divisória no meio
    cv.line(extended_frame, (middle_line_x, height), (middle_line_x, height + keyboard_height), (255, 0, 0), 2)

    return extended_frame

# Start video capture
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

# Threshold for blinking detection (adjust as necessary)
BLINK_THRESHOLD = blinkAdjust

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
 
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    if flip_enabled:
        frame = cv.flip(frame, 1)

    # Convert the frame to RGB (required for MediaPipe)
    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    # Process the frame to detect face mesh
    results = face_mesh.process(rgb_frame)

    # If a face is detected, process the landmarks
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Extract landmarks for left and right eye
            left_eye_landmarks = [(int(face_landmarks.landmark[i].x * frame.shape[1]), int(face_landmarks.landmark[i].y * frame.shape[0])) for i in LEFT_EYE]
            right_eye_landmarks = [(int(face_landmarks.landmark[i].x * frame.shape[1]), int(face_landmarks.landmark[i].y * frame.shape[0])) for i in RIGHT_EYE]

            # Draw the eyes landmarks
            for (x, y) in left_eye_landmarks:
                cv.circle(frame, (x, y), 2, (0, 255, 0), -1)
            for (x, y) in right_eye_landmarks:
                cv.circle(frame, (x, y), 2, (0, 255, 0), -1)

            # Calculate EAR for both eyes
            left_ear = calculate_ear(left_eye_landmarks)
            right_ear = calculate_ear(right_eye_landmarks)

            # Determine if either eye is blinking
            if left_ear < BLINK_THRESHOLD:
                cv.putText(frame, 'Left Eye Blinked', (30, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            if right_ear < BLINK_THRESHOLD:
                cv.putText(frame, 'Right Eye Blinked', (30, 100), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Adicionar o teclado abaixo da janela da webcam
    frame_with_keyboard = draw_keyboard(frame)

    # Display the resulting frame
    cv.imshow('MediaPipe Face Mesh - Eye Blink Detection', frame_with_keyboard)

    # Break the loop if 'q' is pressed
    key = cv.waitKey(1)
    if key == ord('f'):
        flip_enabled = not flip_enabled  # Alterna a inversão
    elif key == ord('q'):
        break
 
# Release the capture and destroy all windows
cap.release()
cv.destroyAllWindows()
