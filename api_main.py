from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from datetime import datetime
import shutil
import json

app = FastAPI()

# CORS config (allow frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# File paths
DATA_DIR = "data"
ENCODE_FILE = os.path.join(DATA_DIR, "known_faces.pkl")
LOG_FILE = os.path.join(DATA_DIR, "logs.json")
IMAGE_DIR = os.path.join(DATA_DIR, "images")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)

# GET: Serve known_faces.pkl
@app.get("/known_faces.pkl")
def get_known_faces():
    if os.path.exists(ENCODE_FILE):
        return FileResponse(ENCODE_FILE, media_type='application/octet-stream')
    return JSONResponse(status_code=404, content={"message": "Encoding file not found"})

# POST: Raspberry Pi ส่งข้อมูล log
@app.post("/api/log")
def receive_log(name: str = Form(...), timestamp: str = Form(...), image: UploadFile = File(...)):
    filename = f"{name}_{timestamp.replace(':', '-')}.jpg"
    save_path = os.path.join(IMAGE_DIR, filename)
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    log_entry = {
        "name": name,
        "timestamp": timestamp,
        "image": f"/images/{filename}"
    }

    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            logs = json.load(f)

    logs.append(log_entry)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2)

    return {"status": "success", "log": log_entry}

# GET: ดึง log ทั้งหมดมาแสดงผล
@app.get("/api/logs")
def get_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Serve static images
@app.get("/images/{image_name}")
def get_image(image_name: str):
    image_path = os.path.join(IMAGE_DIR, image_name)
    if os.path.exists(image_path):
        return FileResponse(image_path)
    return JSONResponse(status_code=404, content={"message": "Image not found"})
