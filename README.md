# 🚗 Driver Monitoring System (DMS) with Drowsiness Detection

A real-time Driver Monitoring System that detects drowsiness using eye aspect ratio (EAR) and Mediapipe, triggers an alarm, and logs incidents. The system includes a web dashboard and Flask backend for remote interaction and log viewing.

---

## 🧠 Features

- Real-time drowsiness detection using eye landmarks
- EAR (Eye Aspect Ratio) based drowsiness logic
- Snapshot capture of drowsy moments
- Alarm sound on drowsiness detection
- Logs detection events with timestamps
- Flask API backend to control/start detection
- Web dashboard for user interaction

---

## 🗂️ Project Structure

```
📦 dms-project
├── app.py                        # Flask backend (API)
├── drowsiness_detector_enhanced.py  # Drowsiness detection model (Mediapipe)
├── config.txt                   # Dynamic config for EAR and sleep threshold
├── drowsiness_log.csv           # CSV log of drowsiness events
├── snapshots/                   # Folder for captured snapshots
├── alarm.wav                    # Alarm sound
└── driver_monitoring_app.html   # Web dashboard frontend
```

---

## ⚙️ Technologies Used
- Python 3.9
- OpenCV
- Mediapipe
- Flask
- HTML + JavaScript (for dashboard)
- Git & GitHub

---

## 🚀 How to Run

### 📌 1. Clone the Repo
```bash
git clone https://github.com/pprj04/Tech-Mates_HackOrbit.git
cd Tech-Mates_HackOrbit
```

### 📌 2. Setup Environment
```bash
python -m venv dms-env
./dms-env/Scripts/activate  # or source dms-env/bin/activate (Linux/Mac)
pip install -r requirements.txt
```

### 📌 3. Run the Flask Backend
```bash
python app.py
```

### 📌 4. Open Dashboard
Open `driver_monitoring_app.html` in your browser.

---

## 📡 Flask API Endpoints

### `POST /start-monitoring`
- Starts the drowsiness detection
- Accepts: `earThreshold`, `sleepTime`

### `GET /logs`
- Downloads the CSV log file

---

## 🎯 Usage Scenario
- Start the backend
- Set EAR threshold and sleep time on dashboard
- Start monitoring
- Alarm rings after eyes closed for defined duration
- Snapshots are saved, and logs are recorded

---

## 🤖 Future Scope
- Android app integration
- Fall detection
- Cloud deployment with real-time dashboards
- GPS + Alert system integration

---

## 🛡️ Contributors
👤 Pushkaraj Potdar  
👤 Himanshi Pandey
👤 Sujal Wagh
👥 Team Tech-Mates – HackOrbit 2025

---

> "Built for HackOrbit 2025 – with the mission to make roads safer using AI."
