from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd
from src.services.facilities import FacilityService

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get(
    "", summary="Получение списка удобств", description="Возвращает весь список удобств"
)
@cache(expire=10)
async def get_facilities(db: DBDep):
    return await FacilityService(db).get_facilities()


@router.post(
    "",
    summary="Добавление удобства",
    description="Добавляет удобство",
)
async def create_facility(
    db: DBDep,
    facility_data: FacilityAdd = Body(),
):
    facility = await FacilityService(db).create_facility(facility_data)
    return {"status": "OK", "data": facility}
