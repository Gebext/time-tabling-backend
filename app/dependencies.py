from functools import lru_cache

from app.config import get_settings

from app.repositories.guru_repository import GuruRepository

from app.repositories.kelas_repository import KelasRepository

from app.repositories.mapel_repository import MapelRepository

from app.repositories.slot_repository import SlotRepository

from app.repositories.relasi_guru_mapel_repository import RelasiGuruMapelRepository

from app.repositories.wali_kelas_repository import WaliKelasRepository

from app.repositories.schedule_repository import ScheduleRepository

from app.services.guru_service import GuruService

from app.services.kelas_service import KelasService

from app.services.mapel_service import MapelService

from app.services.slot_service import SlotService

from app.services.relasi_guru_mapel_service import RelasiGuruMapelService

from app.services.wali_kelas_service import WaliKelasService

from app.services.schedule_service import ScheduleService

from app.algorithm.dictionary import DataDictionary

@lru_cache()

def get_data_dictionary() -> DataDictionary:

    return DataDictionary(get_settings().DATA_DIR)

@lru_cache()

def get_guru_repo() -> GuruRepository:

    return GuruRepository()

@lru_cache()

def get_kelas_repo() -> KelasRepository:

    return KelasRepository()

@lru_cache()

def get_mapel_repo() -> MapelRepository:

    return MapelRepository()

@lru_cache()

def get_slot_repo() -> SlotRepository:

    return SlotRepository()

@lru_cache()

def get_relasi_guru_mapel_repo() -> RelasiGuruMapelRepository:

    return RelasiGuruMapelRepository()

@lru_cache()

def get_wali_kelas_repo() -> WaliKelasRepository:

    return WaliKelasRepository()

@lru_cache()

def get_guru_service() -> GuruService:

    return GuruService(get_guru_repo())

@lru_cache()

def get_kelas_service() -> KelasService:

    return KelasService(get_kelas_repo())

@lru_cache()

def get_mapel_service() -> MapelService:

    return MapelService(get_mapel_repo())

@lru_cache()

def get_slot_service() -> SlotService:

    return SlotService(get_slot_repo())

@lru_cache()

def get_relasi_guru_mapel_service() -> RelasiGuruMapelService:

    return RelasiGuruMapelService(get_relasi_guru_mapel_repo())

@lru_cache()

def get_wali_kelas_service() -> WaliKelasService:

    return WaliKelasService(get_wali_kelas_repo())

@lru_cache()

def get_schedule_repo() -> ScheduleRepository:

    return ScheduleRepository()

@lru_cache()

def get_schedule_service() -> ScheduleService:

    return ScheduleService(get_data_dictionary(), get_schedule_repo())
