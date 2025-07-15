from src.schemas.facilities import FacilityAdd, Facility
from src.services.base import BaseService
from src.tasks.tasks import test_task


class FacilityService(BaseService):
    async def create_facility(
            self,
            facility_data: FacilityAdd
    ) -> Facility:
        facility = await self.db.facilities.add(facility_data)
        await self.db.commit()

        test_task.delay()  # type: ignore
        return facility

    async def get_facilities(self) -> list[Facility]:
        return await self.db.facilities.get_all()