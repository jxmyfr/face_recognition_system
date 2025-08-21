from datetime import datetime, timedelta

def get_overview(scope):
    # TODO: ต่อ DB จริงภายหลัง; ตอนนี้คืน mock ตาม role scope
    if "user_id" in scope:   # student
        return {"present": 18, "absent": 2, "late": 1, "devicesOnline": 0}
    if "class_ids" in scope: # teacher
        return {"present": 120, "absent": 8, "late": 5, "devicesOnline": 4}
    return {"present": 850, "absent": 45, "late": 21, "devicesOnline": 12}  # admin

def get_recent_events(limit, scope):
    now = datetime.utcnow()
    rows = []
    for i in range(limit):
        rows.append({
            "id": f"ev_{i}",
            "studentName": f"Student {i}",
            "className": "M.4/1",
            "time": (now - timedelta(minutes=i*3)).isoformat()+"Z",
            "status": ["present","late","absent"][i % 3],
        })
    return rows

def get_events(scope):
    # TODO: รองรับ filter date/class/q/page
    return {"items": get_recent_events(20, scope), "page": 1, "total": 200}