"""
Base CSV Repository — generic CRUD operations on a CSV file.

To migrate to a database later, only this layer needs to change.
The service layer remains untouched.
"""

import os
import threading
from typing import Any

import pandas as pd

from app.core.exceptions import NotFoundException
from app.core.logging import get_logger

logger = get_logger(__name__)


class BaseCSVRepository:
    """
    Thread-safe generic repository backed by a CSV file.

    Parameters
    ----------
    csv_path : str
        Absolute path to the CSV file.
    id_column : str
        Name of the primary‑key column.
    """

    def __init__(self, csv_path: str, id_column: str):
        self._csv_path = csv_path
        self._id_column = id_column
        self._lock = threading.Lock()
        self._df: pd.DataFrame = self._load()
        logger.info("Loaded %d rows from %s", len(self._df), os.path.basename(csv_path))

    # ── Private helpers ──────────────────────────────────

    def _load(self) -> pd.DataFrame:
        if not os.path.exists(self._csv_path):
            raise FileNotFoundError(f"CSV not found: {self._csv_path}")
        return pd.read_csv(self._csv_path)

    def _persist(self) -> None:
        self._df.to_csv(self._csv_path, index=False)

    def _next_id(self) -> int:
        if self._df.empty:
            return 1
        return int(self._df[self._id_column].max()) + 1

    # ── Public CRUD ──────────────────────────────────────

    def get_all(self) -> list[dict[str, Any]]:
        """Return all rows as a list of dicts."""
        with self._lock:
            return self._df.to_dict(orient="records")

    def get_by_id(self, record_id: int, resource_name: str = "Data") -> dict[str, Any]:
        """Return a single row by its primary key."""
        with self._lock:
            mask = self._df[self._id_column] == record_id
            if not mask.any():
                raise NotFoundException(resource_name, record_id)
            return self._df.loc[mask].iloc[0].to_dict()

    def create(self, data: dict[str, Any], auto_id: bool = True) -> dict[str, Any]:
        """Insert a new row. Returns the created record."""
        with self._lock:
            if auto_id:
                data[self._id_column] = self._next_id()
            new_row = pd.DataFrame([data])
            self._df = pd.concat([self._df, new_row], ignore_index=True)
            self._persist()
            logger.info("Created %s=%s", self._id_column, data[self._id_column])
            return data

    def update(self, record_id: int, data: dict[str, Any], resource_name: str = "Data") -> dict[str, Any]:
        """Update an existing row by primary key. Returns updated record."""
        with self._lock:
            mask = self._df[self._id_column] == record_id
            if not mask.any():
                raise NotFoundException(resource_name, record_id)
            idx = self._df.index[mask][0]
            for key, value in data.items():
                if value is not None:
                    self._df.at[idx, key] = value
            self._persist()
            logger.info("Updated %s=%s", self._id_column, record_id)
            return self._df.loc[idx].to_dict()

    def delete(self, record_id: int, resource_name: str = "Data") -> None:
        """Delete a row by primary key."""
        with self._lock:
            mask = self._df[self._id_column] == record_id
            if not mask.any():
                raise NotFoundException(resource_name, record_id)
            self._df = self._df[~mask].reset_index(drop=True)
            self._persist()
            logger.info("Deleted %s=%s", self._id_column, record_id)

    def get_dataframe(self) -> pd.DataFrame:
        """Return a copy of the underlying DataFrame (for algorithm use)."""
        with self._lock:
            return self._df.copy()

    def reload(self) -> None:
        """Force reload from disk."""
        with self._lock:
            self._df = self._load()
