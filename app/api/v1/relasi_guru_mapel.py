from fastapi import APIRouter, Depends

from app.dependencies import get_relasi_guru_mapel_service

from app.schemas.common import BaseResponse, MessageResponse

from app.schemas.relasi_guru_mapel import RelasiGuruMapelCreate, RelasiGuruMapelResponse

from app.services.relasi_guru_mapel_service import RelasiGuruMapelService

router = APIRouter(prefix="/relasi-guru-mapel", tags=["Relasi Guru-Mapel"])

@router.get("", response_model=BaseResponse[list[RelasiGuruMapelResponse]], summary="Get all relations")

async def get_all(service: RelasiGuruMapelService = Depends(get_relasi_guru_mapel_service)):

    data = service.get_all()

    return BaseResponse(data=data, message=f"Ditemukan {len(data)} relasi")

@router.get("/guru/{guru_id}", response_model=BaseResponse[list[RelasiGuruMapelResponse]], summary="Get relations by teacher")

async def get_by_guru(guru_id: int, service: RelasiGuruMapelService = Depends(get_relasi_guru_mapel_service)):

    data = service.get_by_guru(guru_id)

    return BaseResponse(data=data, message=f"Ditemukan {len(data)} relasi untuk guru {guru_id}")

@router.get("/mapel/{mapel_id}", response_model=BaseResponse[list[RelasiGuruMapelResponse]], summary="Get relations by subject")

async def get_by_mapel(mapel_id: int, service: RelasiGuruMapelService = Depends(get_relasi_guru_mapel_service)):

    data = service.get_by_mapel(mapel_id)

    return BaseResponse(data=data, message=f"Ditemukan {len(data)} relasi untuk mapel {mapel_id}")

@router.post("", response_model=BaseResponse[RelasiGuruMapelResponse], status_code=201, summary="Create relation")

async def create(payload: RelasiGuruMapelCreate, service: RelasiGuruMapelService = Depends(get_relasi_guru_mapel_service)):

    data = service.create(payload)

    return BaseResponse(data=data, message="Relasi berhasil ditambahkan")

@router.delete("", response_model=MessageResponse, summary="Delete relation by composite key")

async def delete(

    guru_id: int,

    mapel_id: int,

    tingkatan: int,

    service: RelasiGuruMapelService = Depends(get_relasi_guru_mapel_service),

):

    service.delete(guru_id, mapel_id, tingkatan)

    return MessageResponse(message="Relasi berhasil dihapus")
