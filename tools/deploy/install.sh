#!/bin/bash

echo "🚀 เริ่มติดตั้งระบบ Face Recognition สำหรับ Raspberry Pi..."

# 1. อัปเดตระบบ
sudo apt-get update
sudo apt-get upgrade -y

# 2. ติดตั้ง build tools ที่จำเป็นสำหรับ dlib
sudo apt-get install -y build-essential cmake
sudo apt-get install -y libopenblas-dev liblapack-dev
sudo apt-get install -y libx11-dev libgtk-3-dev libboost-all-dev
sudo apt-get install -y python3-dev python3-venv

# 3. สร้าง virtual environment
python3 -m venv venv
source venv/bin/activate

# 4. อัปเกรด pip
pip install --upgrade pip

# 5. ติดตั้ง Python libraries
pip install opencv-python
pip install mediapipe
pip install numpy
pip install pandas
pip install dlib
pip install face_recognition

# 6. สร้างโฟลเดอร์และไฟล์พื้นฐานถ้ายังไม่มี
mkdir -p data/faces
mkdir -p data/logs/unknown_images

if [ ! -f data/known_faces.pkl ]; then
  echo "⚠️  ยังไม่มี data/known_faces.pkl — จะสร้างไฟล์เปล่าไว้ให้ก่อน"
  echo "{}" | python3 -c "import pickle, sys; pickle.dump(eval(sys.stdin.read()), open('data/known_faces.pkl', 'wb'))"
fi

echo "✅ ติดตั้งและเตรียมระบบเรียบร้อยแล้ว!"
echo "📸 พร้อมใช้งาน: รัน 'source venv/bin/activate' และ 'python app/recognition_main.py'"
