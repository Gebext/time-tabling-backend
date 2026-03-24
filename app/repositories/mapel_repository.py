import os

from app.config import get_settings

from app.repositories.base_repository import BaseCSVRepository

class MapelRepository(BaseCSVRepository):

    def __init__(self) -> None:

        csv_path = os.path.join(get_settings().DATA_DIR, "mapel.csv")

        super().__init__(csv_path=csv_path, id_column="mapel_id")
