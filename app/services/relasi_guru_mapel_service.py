"""
Service layer for Relasi Guru-Mapel (Teacher-Subject Relation) operations.
"""

from app.repositories.relasi_guru_mapel_repository import RelasiGuruMapelRepository
from app.schemas.relasi_guru_mapel import (
    RelasiGuruMapelCreate,
    RelasiGuruMapelResponse,
)


class RelasiGuruMapelService:
    def __init__(self, repository: RelasiGuruMapelRepository) -> None:
        self._repo = repository

    def get_all(self) -> list[RelasiGuruMapelResponse]:
        rows = self._repo.get_all()
        return [RelasiGuruMapelResponse(**row) for row in rows]

    def get_by_guru(self, guru_id: int) -> list[RelasiGuruMapelResponse]:
        rows = self._repo.get_by_guru(guru_id)
        return [RelasiGuruMapelResponse(**row) for row in rows]

    def get_by_mapel(self, mapel_id: int) -> list[RelasiGuruMapelResponse]:
        rows = self._repo.get_by_mapel(mapel_id)
        return [RelasiGuruMapelResponse(**row) for row in rows]

    def create(self, payload: RelasiGuruMapelCreate) -> RelasiGuruMapelResponse:
        data = payload.model_dump()
        created = self._repo.create(data)
        return RelasiGuruMapelResponse(**created)

    def delete(self, guru_id: int, mapel_id: int, tingkatan: int) -> None:
        self._repo.delete_by_composite(guru_id, mapel_id, tingkatan)
