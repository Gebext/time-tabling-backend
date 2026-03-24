"""
Concrete repository for Slot (Time Slot) data.
"""

import os

from app.config import get_settings
from app.repositories.base_repository import BaseCSVRepository


class SlotRepository(BaseCSVRepository):
    def __init__(self) -> None:
        csv_path = os.path.join(get_settings().DATA_DIR, "slot.csv")
        super().__init__(csv_path=csv_path, id_column="slot_id")
