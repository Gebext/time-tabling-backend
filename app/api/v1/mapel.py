"""
API v1 — Mapel (Subject) endpoints.
"""

from fastapi import APIRouter, Depends

from app.dependencies import get_mapel_service
from app.schemas.common import BaseResponse, MessageResponse
from app.schemas.mapel import MapelCreate, MapelUpdate, MapelResponse
from app.services.mapel_service import MapelService

router = APIRouter(prefix="/mapel", tags=["Mapel"])


@router.get("", response_model=BaseResponse[list[MapelResponse]], summary="Get all subjects")
async def get_all(service: MapelService = Depends(get_mapel_service)):
    data = service.get_all()
    return BaseResponse(data=data, message=f"Ditemukan {len(data)} mapel")


@router.get("/{mapel_id}", response_model=BaseResponse[MapelResponse], summary="Get subject by ID")
async def get_by_id(mapel_id: int, service: MapelService = Depends(get_mapel_service)):
    data = service.get_by_id(mapel_id)
    return BaseResponse(data=data)


@router.post("", response_model=BaseResponse[MapelResponse], status_code=201, summary="Create subject")
async def create(payload: MapelCreate, service: MapelService = Depends(get_mapel_service)):
    data = service.create(payload)
    return BaseResponse(data=data, message="Mapel berhasil ditambahkan")


@router.put("/{mapel_id}", response_model=BaseResponse[MapelResponse], summary="Update subject")
async def update(mapel_id: int, payload: MapelUpdate, service: MapelService = Depends(get_mapel_service)):
    data = service.update(mapel_id, payload)
    return BaseResponse(data=data, message="Mapel berhasil diperbarui")


@router.delete("/{mapel_id}", response_model=MessageResponse, summary="Delete subject")
async def delete(mapel_id: int, service: MapelService = Depends(get_mapel_service)):
    service.delete(mapel_id)
    return MessageResponse(message="Mapel berhasil dihapus")
