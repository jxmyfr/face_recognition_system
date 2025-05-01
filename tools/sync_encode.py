import requests
import os

# URL ของ Server ที่เก็บ known_faces.pkl
ENCODE_URL = "http://<YOUR_SERVER_IP>/known_faces.pkl"
SAVE_PATH = "data/known_faces.pkl"


def download_encoded_file():
    try:
        response = requests.get(ENCODE_URL)
        response.raise_for_status()

        os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
        with open(SAVE_PATH, 'wb') as f:
            f.write(response.content)

        print(f"✅ Synced known_faces.pkl from {ENCODE_URL}")
    except Exception as e:
        print(f"❌ Failed to sync encoding: {e}")


if __name__ == "__main__":
    download_encoded_file()