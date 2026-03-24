"""
Service layer for Mapel (Subject) operations.
"""

from app.core.exceptions import ValidationException
from app.repositories.mapel_repository import MapelRepository
from app.schemas.mapel import HARI_VALID, MapelCreate, MapelUpdate, MapelResponse


class MapelService:
    def __init__(self, repository: MapelRepository) -> None:
        self._repo = repository

    def get_all(self) -> list[MapelResponse]:
        rows = self._repo.get_all()
        return [MapelResponse(**row) for row in rows]

    def get_by_id(self, mapel_id: int) -> MapelResponse:
        row = self._repo.get_by_id(mapel_id, resource_name="Mapel")
        return MapelResponse(**row)

    def create(self, payload: MapelCreate) -> MapelResponse:
        if payload.mgmp not in HARI_VALID:
            raise ValidationException(f"MGMP harus salah satu dari: {HARI_VALID}")
        data = payload.model_dump()
        created = self._repo.create(data)
        return MapelResponse(**created)

    def update(self, mapel_id: int, payload: MapelUpdate) -> MapelResponse:
        if payload.mgmp is not None and payload.mgmp not in HARI_VALID:
            raise ValidationException(f"MGMP harus salah satu dari: {HARI_VALID}")
        data = payload.model_dump(exclude_unset=True)
        updated = self._repo.update(mapel_id, data, resource_name="Mapel")
        return MapelResponse(**updated)

    def delete(self, mapel_id: int) -> None:
        self._repo.delete(mapel_id, resource_name="Mapel")
