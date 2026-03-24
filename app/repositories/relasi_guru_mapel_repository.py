"""
Concrete repository for Relasi Guru-Mapel (Teacher-Subject Relation) data.

Note: This table uses a composite key (guru_id, mapel_id, tingkatan).
We still use a CSV but override specific methods for composite-key handling.
"""

import os
from typing import Any

import pandas as pd

from app.config import get_settings
from app.core.exceptions import NotFoundException
from app.repositories.base_repository import BaseCSVRepository


class RelasiGuruMapelRepository(BaseCSVRepository):
    """
    Relasi Guru-Mapel doesn't have a single auto-increment ID.
    We use (guru_id, mapel_id, tingkatan) as composite key.
    """

    def __init__(self) -> None:
        csv_path = os.path.join(get_settings().DATA_DIR, "relasi_guru_mapel.csv")
        # Use guru_id as a pseudo id_column; real lookups use composite key.
        super().__init__(csv_path=csv_path, id_column="guru_id")

    def get_all(self) -> list[dict[str, Any]]:
        return super().get_all()

    def get_by_composite(self, guru_id: int, mapel_id: int, tingkatan: int) -> dict[str, Any]:
        with self._lock:
            mask = (
                (self._df["guru_id"] == guru_id)
                & (self._df["mapel_id"] == mapel_id)
                & (self._df["tingkatan"] == tingkatan)
            )
            if not mask.any():
                raise NotFoundException(
                    "Relasi Guru-Mapel",
                    f"guru={guru_id}, mapel={mapel_id}, tingkatan={tingkatan}",
                )
            return self._df.loc[mask].iloc[0].to_dict()

    def get_by_guru(self, guru_id: int) -> list[dict[str, Any]]:
        with self._lock:
            mask = self._df["guru_id"] == guru_id
            return self._df.loc[mask].to_dict(orient="records")

    def get_by_mapel(self, mapel_id: int) -> list[dict[str, Any]]:
        with self._lock:
            mask = self._df["mapel_id"] == mapel_id
            return self._df.loc[mask].to_dict(orient="records")

    def create(self, data: dict[str, Any], auto_id: bool = False) -> dict[str, Any]:
        """Insert — no auto-increment ID for composite key table."""
        with self._lock:
            new_row = pd.DataFrame([data])
            self._df = pd.concat([self._df, new_row], ignore_index=True)
            self._persist()
            return data

    def delete_by_composite(self, guru_id: int, mapel_id: int, tingkatan: int) -> None:
        with self._lock:
            mask = (
                (self._df["guru_id"] == guru_id)
                & (self._df["mapel_id"] == mapel_id)
                & (self._df["tingkatan"] == tingkatan)
            )
            if not mask.any():
                raise NotFoundException(
                    "Relasi Guru-Mapel",
                    f"guru={guru_id}, mapel={mapel_id}, tingkatan={tingkatan}",
                )
            self._df = self._df[~mask].reset_index(drop=True)
            self._persist()
