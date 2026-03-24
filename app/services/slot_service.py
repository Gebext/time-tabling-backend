"""
Service layer for Slot (Time Slot) operations.
"""

from app.repositories.slot_repository import SlotRepository
from app.schemas.slot import SlotCreate, SlotUpdate, SlotResponse


class SlotService:
    def __init__(self, repository: SlotRepository) -> None:
        self._repo = repository

    def get_all(self) -> list[SlotResponse]:
        rows = self._repo.get_all()
        return [SlotResponse(**row) for row in rows]

    def get_by_id(self, slot_id: int) -> SlotResponse:
        row = self._repo.get_by_id(slot_id, resource_name="Slot")
        return SlotResponse(**row)

    def create(self, payload: SlotCreate) -> SlotResponse:
        data = payload.model_dump()
        created = self._repo.create(data)
        return SlotResponse(**created)

    def update(self, slot_id: int, payload: SlotUpdate) -> SlotResponse:
        data = payload.model_dump(exclude_unset=True)
        updated = self._repo.update(slot_id, data, resource_name="Slot")
        return SlotResponse(**updated)

    def delete(self, slot_id: int) -> None:
        self._repo.delete(slot_id, resource_name="Slot")
