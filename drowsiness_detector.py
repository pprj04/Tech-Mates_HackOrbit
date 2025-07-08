import cv2
import time
import mediapipe as mp
from scipy.spatial import distance
from playsound import playsound
import threading

def sound_alarm():
    playsound("alarm.wav")

def eye_aspect_ratio(eye):
    # Vertical distances
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    # Horizontal distance
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

EAR_THRESHOLD = 0.25
SLEEP_TIME = 5.0

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1)
mp_drawing = mp.solutions.drawing_utils

# Indexes for left and right eyes (from Mediapipe FaceMesh)
LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]

cap = cv2.VideoCapture(0)
start_time = None
alarm_on = False

print("[INFO] Mediapipe Drowsiness Detection started. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("[ERROR] Could not read frame.")
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(frame_rgb)

    if results.multi_face_landmarks:
        mesh_points = results.multi_face_landmarks[0].landmark
        h, w, _ = frame.shape

        left_eye = [(int(mesh_points[p].x * w), int(mesh_points[p].y * h)) for p in LEFT_EYE]
        right_eye = [(int(mesh_points[p].x * w), int(mesh_points[p].y * h)) for p in RIGHT_EYE]

        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)
        ear = (left_ear + right_ear) / 2.0

        if ear < EAR_THRESHOLD:
            if start_time is None:
                start_time = time.time()
            elif (time.time() - start_time) > SLEEP_TIME:
                if not alarm_on:
                    alarm_on = True
                    threading.Thread(target=sound_alarm).start()
                cv2.putText(frame, "DROWSINESS DETECTED!", (30, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
        else:
            start_time = None
            alarm_on = False

        cv2.putText(frame, f"EAR: {ear:.2f}", (450, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.imshow("Driver Monitoring", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
