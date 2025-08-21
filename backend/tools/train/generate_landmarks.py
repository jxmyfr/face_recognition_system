import os
import json
import cv2
import mediapipe as mp

FACES_DIR = 'data/faces'
ANNOTATIONS_DIR = 'data/annotations'
INDEX_FILE = 'data/landmark_index.json'
IMG_EXTS = ('.jpg', '.jpeg', '.png')
DELETE_NO_FACE = True

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5
)

if os.path.exists(INDEX_FILE):
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        landmark_index = json.load(f)
else:
    landmark_index = {}

os.makedirs(ANNOTATIONS_DIR, exist_ok=True)

def generate_landmarks():
    for person_name in os.listdir(FACES_DIR):
        person_path = os.path.join(FACES_DIR, person_name)
        if not os.path.isdir(person_path):
            continue

        save_path = os.path.join(ANNOTATIONS_DIR, person_name)
        os.makedirs(save_path, exist_ok=True)
        detected_images = landmark_index.get(person_name, [])

        index = len(detected_images)
        for img_name in sorted(os.listdir(person_path)):
            if not img_name.lower().endswith(IMG_EXTS):
                continue
            if img_name in detected_images:
                continue

            img_path = os.path.join(person_path, img_name)
            image = cv2.imread(img_path)
            if image is None:
                print(f"[SKIP] Cannot read: {img_path}")
                continue

            h, w, _ = image.shape
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            result = face_mesh.process(rgb)

            if not result.multi_face_landmarks:
                print(f"[SKIP] No face in: {img_path}")
                if DELETE_NO_FACE:
                    os.remove(img_path)
                    print(f"[DEL] Removed: {img_path}")
                continue

            landmarks = [
                [int(lm.x * w), int(lm.y * h)]
                for lm in result.multi_face_landmarks[0].landmark
            ]

            output = {
                "image": img_path.replace('\\', '/'),
                "landmarks": landmarks
            }

            json_name = f"{index}.json"
            json_path = os.path.join(save_path, json_name)
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=2)

            print(f"[OK] Saved: {json_path}")
            detected_images.append(img_name)
            index += 1

        if detected_images:
            landmark_index[person_name] = detected_images

    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(landmark_index, f, indent=2)

    print(f"\n✅ Landmark index saved to {INDEX_FILE}")

if __name__ == '__main__':
    generate_landmarks()
