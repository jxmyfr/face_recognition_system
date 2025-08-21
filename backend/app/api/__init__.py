from .students import router as students_router
from .teachers import router as teachers_router
from .subjects import router as subjects_router
from .rooms import router as rooms_router
from .timetable import router as timetable_router
from .attendances import router as attendances_router
from .auth import router as auth_router

all_routers = [
    students_router,
    teachers_router,
    subjects_router,
    rooms_router,
    timetable_router,
    attendances_router,
    auth_router
]