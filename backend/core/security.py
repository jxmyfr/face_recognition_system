class Role(str, Enum): ADMIN="admin"; TEACHER="teacher"; STUDENT="student"

def create_access_token(user):
    payload = {
        "sub": str(user.id),
        "role": user.role,
        "schoolId": user.school_id,
        "classIds": user.class_ids,   # [] สำหรับ admin/student แล้วแต่ระบบ
        "iss": settings.JWT_ISS, "aud": settings.JWT_AUD,
        "iat": now, "exp": now + timedelta(hours=8),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")