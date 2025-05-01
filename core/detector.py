import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=5,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

def detect_faces(rgb_frame):
    h, w, _ = rgb_frame.shape
    results = face_mesh.process(rgb_frame)
    faces = []
    if results.multi_face_landmarks:
        for landmarks in results.multi_face_landmarks:
            xs = [int(pt.x * w) for pt in landmarks.landmark]
            ys = [int(pt.y * h) for pt in landmarks.landmark]
            x_min, x_max = max(0, min(xs)), min(w, max(xs))
            y_min, y_max = max(0, min(ys)), min(h, max(ys))
            bbox = (x_min, y_min, x_max - x_min, y_max - y_min)
            roi = rgb_frame[y_min:y_max, x_min:x_max]
            faces.append((bbox, roi))
    return faces