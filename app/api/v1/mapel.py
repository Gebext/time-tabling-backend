from fastapi import APIRouter, Depends, Query

from app.dependencies import get_mapel_service

from app.schemas.common import BaseResponse, PaginatedResponse, MessageResponse

from app.schemas.mapel import MapelCreate, MapelUpdate, MapelResponse

from app.services.mapel_service import MapelService

router = APIRouter(prefix="/mapel", tags=["Mapel"])

@router.get("", response_model=PaginatedResponse[MapelResponse], summary="Get all subjects (paginated)")

async def get_all(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=1000),
    q: str | None = Query(default=None, description="Search query"),
    service: MapelService = Depends(get_mapel_service),
):

    data, total = service.get_paginated(page, per_page, q)

    return PaginatedResponse(data=data, total=total, page=page, per_page=per_page, message=f"Ditemukan {total} mapel")

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
