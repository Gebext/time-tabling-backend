"""
Service layer for Guru (Teacher) operations.
"""

from app.repositories.guru_repository import GuruRepository
from app.schemas.guru import GuruCreate, GuruUpdate, GuruResponse


class GuruService:
    def __init__(self, repository: GuruRepository) -> None:
        self._repo = repository

    def get_all(self) -> list[GuruResponse]:
        rows = self._repo.get_all()
        return [GuruResponse(**row) for row in rows]

    def get_by_id(self, guru_id: int) -> GuruResponse:
        row = self._repo.get_by_id(guru_id, resource_name="Guru")
        return GuruResponse(**row)

    def create(self, payload: GuruCreate) -> GuruResponse:
        data = payload.model_dump()
        created = self._repo.create(data)
        return GuruResponse(**created)

    def update(self, guru_id: int, payload: GuruUpdate) -> GuruResponse:
        data = payload.model_dump(exclude_unset=True)
        updated = self._repo.update(guru_id, data, resource_name="Guru")
        return GuruResponse(**updated)

    def delete(self, guru_id: int) -> None:
        self._repo.delete(guru_id, resource_name="Guru")
