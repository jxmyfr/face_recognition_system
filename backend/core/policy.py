from fastapi import HTTPException

def for_overview(user):
    if user.role == "admin":
        return {"school_id": user.school_id}
    if user.role == "teacher":
        return {"class_ids": user.class_ids}
    if user.role == "student":
        return {"user_id": user.id}
    raise HTTPException(status_code=403, detail="Forbidden")

def can_read_events(user, query):
    return for_overview(user)