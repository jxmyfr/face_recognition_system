import cv2
from concurrent.futures import ThreadPoolExecutor
from core import detector, logger_mysql, recognizer, utils, config

executor = ThreadPoolExecutor(max_workers=2)
last_seen = {}

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Camera error.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = detector.detect_faces(rgb)
    for bbox, face_roi in faces:
        name = recognizer.recognize_face(face_roi)
        now = utils.get_timestamp()
        last_time = last_seen.get(name, now)
        if (now - last_time).total_seconds() > config.LOG_INTERVAL_SECONDS:
            logger_mysql.log_entry(name, frame, bbox)
            last_seen[name] = now

        x, y, w, h = bbox
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow("Face Recognition", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
executor.shutdown()