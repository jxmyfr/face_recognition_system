# Face Recognition System

ระบบจดจำใบหน้าแบบ Real-time พร้อม Web Dashboard + Raspberry Pi Sync

## Features
- ตรวจจับใบหน้าด้วย MediaPipe
- Encode ใบหน้าบน Server → Raspberry Pi sync
- ส่งข้อมูลแบบ real-time ไปยัง Web API
- Dashboard เขียนด้วย Next.js + Tailwind
- Auth สำหรับ Admin

## Structure
- Backend API → Flask/FastAPI
- Frontend → Next.js (admin only)
- Raspberry Pi → Run detector + sync encode
