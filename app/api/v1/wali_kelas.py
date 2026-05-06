from fastapi import APIRouter, Depends, Query

from app.dependencies import get_wali_kelas_service

from app.schemas.common import BaseResponse, PaginatedResponse, MessageResponse

from app.schemas.wali_kelas import WaliKelasCreate, WaliKelasUpdate, WaliKelasResponse

from app.services.wali_kelas_service import WaliKelasService

router = APIRouter(prefix="/wali-kelas", tags=["Wali Kelas"])

@router.get("", response_model=PaginatedResponse[WaliKelasResponse], summary="Get all homeroom teachers (paginated)")

async def get_all(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=1000),
    q: str | None = Query(default=None, description="Search query"),
    service: WaliKelasService = Depends(get_wali_kelas_service),
):

    data, total = service.get_paginated(page, per_page, q)

    return PaginatedResponse(data=data, total=total, page=page, per_page=per_page, message=f"Ditemukan {total} wali kelas")

@router.get("/{guru_id}", response_model=BaseResponse[WaliKelasResponse], summary="Get homeroom teacher by guru ID")

async def get_by_id(guru_id: int, service: WaliKelasService = Depends(get_wali_kelas_service)):

    data = service.get_by_guru_id(guru_id)

    return BaseResponse(data=data)

@router.post("", response_model=BaseResponse[WaliKelasResponse], status_code=201, summary="Assign homeroom teacher")

async def create(payload: WaliKelasCreate, service: WaliKelasService = Depends(get_wali_kelas_service)):

    data = service.create(payload)

    return BaseResponse(data=data, message="Wali kelas berhasil ditambahkan")

@router.put("/{guru_id}", response_model=BaseResponse[WaliKelasResponse], summary="Update homeroom teacher assignment")

async def update(guru_id: int, payload: WaliKelasUpdate, service: WaliKelasService = Depends(get_wali_kelas_service)):

    data = service.update(guru_id, payload)

    return BaseResponse(data=data, message="Wali kelas berhasil diperbarui")

@router.delete("/{guru_id}", response_model=MessageResponse, summary="Remove homeroom teacher assignment")

async def delete(guru_id: int, service: WaliKelasService = Depends(get_wali_kelas_service)):

    service.delete(guru_id)

    return MessageResponse(message="Wali kelas berhasil dihapus")
