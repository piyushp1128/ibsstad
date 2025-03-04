import cv2
import os
import csv
from datetime import datetime
from flask import Flask, render_template, Response, send_file, jsonify
import pygame
from ultralytics import YOLO

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure secret key for session management

# Initialize Pygame for audio
pygame.mixer.init()
BUZZER_FILE_PATH = "static/buzzer.mp3"  # Path to buzzer sound
buzzer_sound = pygame.mixer.Sound(BUZZER_FILE_PATH)

# YOLO model setup for detection
human_classes = [0]  # COCO class ID for 'person'
vehicle_classes = [2, 3, 5, 7, 8]  # COCO class IDs for vehicles
target_classes = human_classes + vehicle_classes  # Combined target classes

# Load YOLO model (ensure you have the correct model weights file)
model = YOLO("weights/yolov8n.pt", "v8")

# Load COCO class names (this should be your coco.txt file)
with open("utils/coco.txt", "r") as file:
    class_list = file.read().splitlines()

# Define the home page route (dashboard)
@app.route('/')
def index():
    return render_template('index.html')

# Path for storing the detection report
report_path = 'detection_report.csv'

# Check if the report file exists and create it if it doesn't
if not os.path.exists(report_path):
    with open(report_path, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Timestamp', 'Object', 'Confidence', 'Bounding Box'])

# Video streaming route
def generate_video():
    cap = cv2.VideoCapture(0)  # Open the webcam (0 is usually the default webcam)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    threat_detected = False  # Initialize threat detection status

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame")
            break

        # Perform YOLO detection on the frame
        results = model.predict(source=frame, conf=0.45, classes=target_classes, save=False)
        
        # Reset threat detection flag for each frame
        threat_detected = False

        # Loop over all detected boxes
        for box in results[0].boxes:
            clsID = int(box.cls.numpy()[0])  # Class ID of the detected object
            conf = box.conf.numpy()[0]  # Confidence score
            bb = box.xyxy.numpy()[0]  # Bounding box coordinates

            # Add detection information to the report (CSV)
            with open(report_path, mode='a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                 class_list[clsID], conf, f"{bb[0]}, {bb[1]}, {bb[2]}, {bb[3]}"])

            # Check if the object is a human or vehicle to trigger alert
            if clsID in human_classes or clsID in vehicle_classes:
                threat_detected = True  # Set flag to True if threat (human or vehicle) is detected
                color = (0, 0, 255)  # Red for threats
                label = f"Threat: {class_list[clsID]} {conf:.2f}%"
            else:
                continue

            # Draw the bounding box and label on the frame
            cv2.rectangle(frame, (int(bb[0]), int(bb[1])), (int(bb[2]), int(bb[3])), color, 2)
            cv2.putText(frame, label, (int(bb[0]), int(bb[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # Send detection status to the frontend (whether a threat is detected)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame)[1].tobytes() + b'\r\n')

        # Play buzzer sound if threat is detected
        if threat_detected:
            buzzer_sound.play(-1)  # Loop the sound
        else:
            buzzer_sound.stop()  # Stop the sound if no threat

    cap.release()

# Video feed route (for streaming)
@app.route('/video_feed')
def video_feed():
    return Response(generate_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Report download route
@app.route('/download_report')
def download_report():
    return send_file(report_path, as_attachment=True)

# Endpoint to check if a threat is detected
@app.route('/check_threat', methods=['GET'])
def check_threat():
    # Return a response indicating whether a threat is detected
    return jsonify({'threat_detected': threat_detected})

# Start the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)