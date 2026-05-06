from fastapi import APIRouter, Depends, Query

from app.dependencies import get_kelas_service

from app.schemas.common import BaseResponse, PaginatedResponse, MessageResponse

from app.schemas.kelas import KelasCreate, KelasUpdate, KelasResponse

from app.services.kelas_service import KelasService

router = APIRouter(prefix="/kelas", tags=["Kelas"])

@router.get("", response_model=PaginatedResponse[KelasResponse], summary="Get all classes (paginated)")

async def get_all(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=1000),
    q: str | None = Query(default=None, description="Search query"),
    service: KelasService = Depends(get_kelas_service),
):

    data, total = service.get_paginated(page, per_page, q)

    return PaginatedResponse(data=data, total=total, page=page, per_page=per_page, message=f"Ditemukan {total} kelas")

@router.get("/{kelas_id}", response_model=BaseResponse[KelasResponse], summary="Get class by ID")

async def get_by_id(kelas_id: int, service: KelasService = Depends(get_kelas_service)):

    data = service.get_by_id(kelas_id)

    return BaseResponse(data=data)

@router.post("", response_model=BaseResponse[KelasResponse], status_code=201, summary="Create class")

async def create(payload: KelasCreate, service: KelasService = Depends(get_kelas_service)):

    data = service.create(payload)

    return BaseResponse(data=data, message="Kelas berhasil ditambahkan")

@router.put("/{kelas_id}", response_model=BaseResponse[KelasResponse], summary="Update class")

async def update(kelas_id: int, payload: KelasUpdate, service: KelasService = Depends(get_kelas_service)):

    data = service.update(kelas_id, payload)

    return BaseResponse(data=data, message="Kelas berhasil diperbarui")

@router.delete("/{kelas_id}", response_model=MessageResponse, summary="Delete class")

async def delete(kelas_id: int, service: KelasService = Depends(get_kelas_service)):

    service.delete(kelas_id)

    return MessageResponse(message="Kelas berhasil dihapus")
