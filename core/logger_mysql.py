import pymysql
import cv2
import os
from core.config import MYSQL_CONFIG
from core.utils import get_timestamp, get_timestamp_str

conn = pymysql.connect(**MYSQL_CONFIG)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME,
    name VARCHAR(255),
    image_path TEXT
)
''')
conn.commit()

def log_entry(name, frame, bbox):
    now = get_timestamp()
    time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    filename = f"{name}_{get_timestamp_str()}.jpg"
    image_dir = "data/logs/unknown_images"
    os.makedirs(image_dir, exist_ok=True)
    image_path = os.path.join(image_dir, filename)

    x, y, w, h = bbox
    face_img = frame[y:y+h, x:x+w]
    cv2.imwrite(image_path, face_img)

    cursor.execute(
        "INSERT INTO logs (timestamp, name, image_path) VALUES (%s, %s, %s)",
        (time_str, name, image_path)
    )
    conn.commit()

def get_all_logs():
    cursor.execute("SELECT * FROM logs ORDER BY timestamp DESC")
    return cursor.fetchall()

def get_logs_by_name(name):
    cursor.execute("SELECT * FROM logs WHERE name = %s ORDER BY timestamp DESC", (name,))
    return cursor.fetchall()