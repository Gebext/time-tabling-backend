from fastapi import APIRouter

from app.api.v1 import (

    guru,

    kelas,

    mapel,

    slot,

    relasi_guru_mapel,

    wali_kelas,

    schedule,

)

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(guru.router)

api_router.include_router(kelas.router)

api_router.include_router(mapel.router)

api_router.include_router(slot.router)

api_router.include_router(relasi_guru_mapel.router)

api_router.include_router(wali_kelas.router)

api_router.include_router(schedule.router)
