"""
Concrete repository for Guru (Teacher) data.
"""

from app.config import get_settings
from app.repositories.base_repository import BaseCSVRepository

import os


class GuruRepository(BaseCSVRepository):
    def __init__(self) -> None:
        csv_path = os.path.join(get_settings().DATA_DIR, "guru.csv")
        super().__init__(csv_path=csv_path, id_column="guru_id")
