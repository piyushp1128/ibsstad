# ibsstad
Defense sector project :- Intelligent Border Surveillance System for Threat Automated  Detection 

A real-time object detection system for restricted zones using YOLOv8. It detects unauthorized human or vehicle presence via 
webcam, sounds an alert buzzer on threat detection, and logs all events with timestamps through a Flask web interface 
Tech Stack used: 
● Computer Vision: OpenCV- for real time video capture and annotation. 
● Deep Learning: YOLOv8 (via Ultralytics)- for fast and accurate object detection. 
● Backend: Flask- for handling server-side logic, routing, and API endpoints. 
●  Audio Alerts: Pygame- for playing buzzer sound on threat detection. 
● Data Logging: CSV and Python datetime- to maintain a structured detection report. 
● Frontend: HTML, CSS (via Flask templates)- to stream the live video feed in a web interface. 
