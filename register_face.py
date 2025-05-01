import os
import cv2

FACES_DIR = 'data/faces'
IMG_EXTS = ('.jpg', '.jpeg', '.png')
IMG_WIDTH = 320
IMG_HEIGHT = 240


def get_next_index(folder):
    existing = [f for f in os.listdir(folder) if f.lower().endswith(IMG_EXTS)]
    nums = sorted([int(f.split('.')[0]) for f in existing if f.split('.')[0].isdigit()])
    for i in range(len(nums) + 1):
        if i not in nums:
            return i
    return len(nums)


def register_face():
    person_name = input("Enter name to register: ").strip()
    person_path = os.path.join(FACES_DIR, person_name)
    os.makedirs(person_path, exist_ok=True)

    cap = cv2.VideoCapture(1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, IMG_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, IMG_HEIGHT)

    print("Press 's' to save image, 'q' to quit.")
    index = get_next_index(person_path)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read from camera.")
            break

        cv2.imshow(f"Register: {person_name}", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):
            filename = f"{index}.jpg"
            path = os.path.join(person_path, filename)
            cv2.imwrite(path, frame)
            print(f"Saved: {path}")
            index = get_next_index(person_path)  # เช็กใหม่ทุกครั้ง

        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    register_face()