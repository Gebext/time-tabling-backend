from fastapi import APIRouter, Depends, Query

from app.dependencies import get_guru_service

from app.schemas.common import BaseResponse, PaginatedResponse, MessageResponse

from app.schemas.guru import GuruCreate, GuruUpdate, GuruResponse

from app.services.guru_service import GuruService

router = APIRouter(prefix="/guru", tags=["Guru"])

@router.get("", response_model=PaginatedResponse[GuruResponse], summary="Get all teachers (paginated)")

async def get_all(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=1000),
    q: str | None = Query(default=None, description="Search query"),
    service: GuruService = Depends(get_guru_service),
):

    data, total = service.get_paginated(page, per_page, q)

    return PaginatedResponse(data=data, total=total, page=page, per_page=per_page, message=f"Ditemukan {total} guru")

@router.get("/{guru_id}", response_model=BaseResponse[GuruResponse], summary="Get teacher by ID")

async def get_by_id(guru_id: int, service: GuruService = Depends(get_guru_service)):

    data = service.get_by_id(guru_id)

    return BaseResponse(data=data)

@router.post("", response_model=BaseResponse[GuruResponse], status_code=201, summary="Create teacher")

async def create(payload: GuruCreate, service: GuruService = Depends(get_guru_service)):

    data = service.create(payload)

    return BaseResponse(data=data, message="Guru berhasil ditambahkan")

@router.put("/{guru_id}", response_model=BaseResponse[GuruResponse], summary="Update teacher")

async def update(guru_id: int, payload: GuruUpdate, service: GuruService = Depends(get_guru_service)):

    data = service.update(guru_id, payload)

    return BaseResponse(data=data, message="Guru berhasil diperbarui")

@router.delete("/{guru_id}", response_model=MessageResponse, summary="Delete teacher")

async def delete(guru_id: int, service: GuruService = Depends(get_guru_service)):

    service.delete(guru_id)

    return MessageResponse(message="Guru berhasil dihapus")
