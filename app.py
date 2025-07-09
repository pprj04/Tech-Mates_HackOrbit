from flask import Flask, request, jsonify, send_file
import os
import subprocess
import threading
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
detection_process = None

@app.route('/')
def home():
    return "✅ Driver Monitoring Backend is Running"

@app.route('/start-monitoring', methods=['POST'])
def start_monitoring():
    global detection_process
    ear = request.json.get("earThreshold", 0.25)
    sleep_time = request.json.get("sleepTime", 5.0)

    with open("config.txt", "w") as f:
        f.write(f"{ear},{sleep_time}")

    if detection_process is None or not detection_process.is_alive():
        detection_process = threading.Thread(target=run_detection)
        detection_process.start()

    return jsonify({"status": "Monitoring started", "EAR": ear, "sleepTime": sleep_time})

@app.route('/logs', methods=['GET'])
def get_logs():
    if os.path.exists("drowsiness_log.csv"):
        return send_file("drowsiness_log.csv", mimetype='text/csv')
    else:
        return "Log file not found", 404

def run_detection():
    os.system("python drowsiness_detector_enhanced.py")

if __name__ == '__main__':
    app.run(debug=True)
