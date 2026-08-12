from fastapi import APIRouter

router = APIRouter(prefix='/users', tags=["Суперпользователь"])


@router.patch("/login")
async def update_booking(booking_id: int):
    pass