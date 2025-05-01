import os
import pickle
import json
import face_recognition

FACES_DIR = 'data/faces'
ENCODING_FILE = 'data/known_faces.pkl'
META_FILE = 'data/encoding_meta.json'
LANDMARK_INDEX_FILE = 'data/landmark_index.json'
IMG_EXTS = ('.jpg', '.jpeg', '.png')

def load_encodings():
    if os.path.exists(ENCODING_FILE):
        with open(ENCODING_FILE, 'rb') as f:
            encodings = pickle.load(f)
    else:
        encodings = {}
    return encodings

def load_metadata():
    if os.path.exists(META_FILE):
        with open(META_FILE, 'r', encoding='utf-8') as f:
            meta = json.load(f)
    else:
        meta = {}
    return meta

def save_metadata(meta):
    with open(META_FILE, 'w', encoding='utf-8') as f:
        json.dump(meta, f, indent=2)

def load_landmark_index():
    if os.path.exists(LANDMARK_INDEX_FILE):
        with open(LANDMARK_INDEX_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def encode_faces():
    known_encodings = load_encodings()
    metadata = load_metadata()
    landmark_index = load_landmark_index()
    updated = 0

    for person_name in os.listdir(FACES_DIR):
        person_path = os.path.join(FACES_DIR, person_name)
        if not os.path.isdir(person_path):
            continue

        if person_name not in landmark_index:
            print(f"[SKIP] No landmark info for: {person_name}")
            continue

        current_images = sorted(landmark_index[person_name], key=lambda x: int(os.path.splitext(x)[0]))

        if (person_name not in known_encodings) or (person_name not in metadata) or (set(current_images) != set(metadata[person_name])):
            print(f"\n[ENCODING] {person_name} - valid landmark images found")
            encodings = []
            valid_images = []

            for img_name in current_images:
                img_path = os.path.join(person_path, img_name)
                if not os.path.exists(img_path):
                    print(f"[SKIP] File missing: {img_path}")
                    continue

                image = face_recognition.load_image_file(img_path)
                faces = face_recognition.face_encodings(image)

                if faces:
                    encodings.append(faces[0])
                    valid_images.append(img_name)
                else:
                    print(f"[WARNING] No face encoded: {img_path}")

            if encodings:
                avg_encoding = sum(encodings) / len(encodings)
                known_encodings[person_name] = avg_encoding
                metadata[person_name] = valid_images
                updated += 1
            else:
                print(f"[WARNING] No valid encodings for: {person_name}")
        else:
            print(f"[SKIP] {person_name} has no new landmark-based images")

    with open(ENCODING_FILE, 'wb') as f:
        pickle.dump(known_encodings, f)

    save_metadata(metadata)

    print(f"\n✅ Updated {updated} person(s). Saved to {ENCODING_FILE} and {META_FILE}")

if __name__ == '__main__':
    encode_faces()
