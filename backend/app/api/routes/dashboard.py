from fastapi import APIRouter, Depends
from app.core.security import get_current_user  # เขียนให้คืน user {id, role, school_id, class_ids}
from app.core import policy
from app.services.dashboard_service import get_overview, get_recent_events, get_events

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/stats/overview")
def stats_overview(current_user = Depends(get_current_user)):
    scope = policy.for_overview(current_user)
    return get_overview(scope)

@router.get("/events/recent")
def events_recent(limit: int = 20, current_user = Depends(get_current_user)):
    scope = policy.can_read_events(current_user, {})
    return get_recent_events(limit, scope)

@router.get("/events")
def events(date: str | None = None, classId: str | None = None, q: str | None = None,
           page: int = 1, current_user = Depends(get_current_user)):
    scope = policy.can_read_events(current_user, {"date": date, "classId": classId, "q": q, "page": page})
    return get_events(scope)