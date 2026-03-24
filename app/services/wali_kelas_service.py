"""
Service layer for Wali Kelas (Homeroom Teacher) operations.
"""

from app.repositories.wali_kelas_repository import WaliKelasRepository
from app.schemas.wali_kelas import WaliKelasCreate, WaliKelasUpdate, WaliKelasResponse


class WaliKelasService:
    def __init__(self, repository: WaliKelasRepository) -> None:
        self._repo = repository

    def get_all(self) -> list[WaliKelasResponse]:
        rows = self._repo.get_all()
        return [WaliKelasResponse(**row) for row in rows]

    def get_by_guru_id(self, guru_id: int) -> WaliKelasResponse:
        row = self._repo.get_by_id(guru_id, resource_name="Wali Kelas")
        return WaliKelasResponse(**row)

    def create(self, payload: WaliKelasCreate) -> WaliKelasResponse:
        data = payload.model_dump()
        created = self._repo.create(data, auto_id=False)
        return WaliKelasResponse(**created)

    def update(self, guru_id: int, payload: WaliKelasUpdate) -> WaliKelasResponse:
        data = payload.model_dump(exclude_unset=True)
        updated = self._repo.update(guru_id, data, resource_name="Wali Kelas")
        return WaliKelasResponse(**updated)

    def delete(self, guru_id: int) -> None:
        self._repo.delete(guru_id, resource_name="Wali Kelas")
