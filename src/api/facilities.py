from datetime import date

from fastapi import APIRouter, Body

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get(
    "", summary="Получение списка удобств", description="Возвращает весь список удобств"
)
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post(
    "",
    summary="Добавление удобства",
    description="Добавляет удобство",
)
async def create_facility(
    db: DBDep,
    facility_data: FacilityAdd = Body(),
):
    facility = await db.facilities.add(facility_data)
    await db.commit()
    return {"status": "OK", "data": facility}
