import cv2
import time
import mediapipe as mp
from scipy.spatial import distance
from playsound import playsound
import threading
import csv
from datetime import datetime
import os


# ========== Config ==========

# === Read EAR threshold and sleep time from config ===
EAR_THRESHOLD = 0.25
SLEEP_TIME = 5.0
try:
    with open("config.txt", "r") as cfg:
        ear_str, sleep_str = cfg.read().split(",")
        EAR_THRESHOLD = float(ear_str)
        SLEEP_TIME = float(sleep_str)
except:
    print("[WARNING] Using default EAR and SleepTime")

LOG_FILE = "drowsiness_log.csv"
SNAPSHOT_DIR = "snapshots"
os.makedirs(SNAPSHOT_DIR, exist_ok=True)

# ========== Mediapipe Setup ==========
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1)
mp_drawing = mp.solutions.drawing_utils

# Indexes for left and right eyes (FaceMesh)
LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]

# ========== Helper Functions ==========
def sound_alarm():
    playsound("alarm.wav")

def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

def log_drowsiness_event():
    with open(LOG_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "Drowsiness Detected"])

def capture_snapshot(frame):
    filename = f"{SNAPSHOT_DIR}/drowsy_{int(time.time())}.jpg"
    cv2.imwrite(filename, frame)

# ========== Main ==========
cap = cv2.VideoCapture(0)
start_time = None
alarm_on = False

print("[INFO] Drowsiness Detection started. Press 'q' to quit.")

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

        # Display EAR on screen
        cv2.putText(frame, f"EAR: {ear:.2f}", (450, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Drowsiness Logic
        if ear < EAR_THRESHOLD:
            if start_time is None:
                start_time = time.time()
            elif (time.time() - start_time) > SLEEP_TIME:
                if not alarm_on:
                    alarm_on = True
                    threading.Thread(target=sound_alarm).start()
                    log_drowsiness_event()
                    capture_snapshot(frame)
                cv2.putText(frame, "DROWSINESS DETECTED!", (30, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
        else:
            start_time = None
            alarm_on = False

    cv2.imshow("Driver Monitoring", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
