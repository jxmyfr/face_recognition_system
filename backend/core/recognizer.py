import pickle
import numpy as np
import face_recognition
from core.config import ENCODING_FILE, MATCH_THRESHOLD

with open(ENCODING_FILE, 'rb') as f:
    known_faces = pickle.load(f)

known_names = list(known_faces.keys())
known_encodings = np.array(list(known_faces.values()))

def recognize_face(face_image):
    h, w, _ = face_image.shape
    face_locations = [(0, w, h, 0)]
    encodings = face_recognition.face_encodings(face_image, known_face_locations=face_locations)
    if not encodings:
        return "Unknown"
    face_encoding = encodings[0]
    distances = face_recognition.face_distance(known_encodings, face_encoding)
    best_idx = np.argmin(distances)
    if distances[best_idx] < MATCH_THRESHOLD:
        return known_names[best_idx]
    return "Unknown"