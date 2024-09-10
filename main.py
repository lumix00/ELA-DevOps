import numpy as np
import cv2 as cv
import mediapipe as mp

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

# Start video capture
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

# Threshold for blinking detection (adjust as necessary)
BLINK_THRESHOLD = 0.20

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
 
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

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

    # Display the resulting frame
    cv.imshow('MediaPipe Face Mesh - Eye Blink Detection', frame)

    # Break the loop if 'q' is pressed
    if cv.waitKey(1) == ord('q'):
        break
 
# Release the capture and destroy all windows
cap.release()
cv.destroyAllWindows()
