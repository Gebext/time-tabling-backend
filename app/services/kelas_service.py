from app.repositories.kelas_repository import KelasRepository

from app.schemas.kelas import KelasCreate, KelasUpdate, KelasResponse

class KelasService:

    def __init__(self, repository: KelasRepository) -> None:

        self._repo = repository

    def get_all(self) -> list[KelasResponse]:

        rows = self._repo.get_all()

        return [KelasResponse(**row) for row in rows]

    def get_paginated(
        self, page: int = 1, per_page: int = 10, search: str | None = None
    ) -> tuple[list[KelasResponse], int]:

        rows, total = self._repo.get_paginated_filtered(page, per_page, search)

        return [KelasResponse(**row) for row in rows], total

    def get_by_id(self, kelas_id: int) -> KelasResponse:

        row = self._repo.get_by_id(kelas_id, resource_name="Kelas")

        return KelasResponse(**row)

    def create(self, payload: KelasCreate) -> KelasResponse:

        data = payload.model_dump()

        created = self._repo.create(data)

        return KelasResponse(**created)

    def update(self, kelas_id: int, payload: KelasUpdate) -> KelasResponse:

        data = payload.model_dump(exclude_unset=True)

        updated = self._repo.update(kelas_id, data, resource_name="Kelas")

        return KelasResponse(**updated)

    def delete(self, kelas_id: int) -> None:

        self._repo.delete(kelas_id, resource_name="Kelas")
