"""
API v1 — Wali Kelas (Homeroom Teacher) endpoints.
"""

from fastapi import APIRouter, Depends

from app.dependencies import get_wali_kelas_service
from app.schemas.common import BaseResponse, MessageResponse
from app.schemas.wali_kelas import WaliKelasCreate, WaliKelasUpdate, WaliKelasResponse
from app.services.wali_kelas_service import WaliKelasService

router = APIRouter(prefix="/wali-kelas", tags=["Wali Kelas"])


@router.get("", response_model=BaseResponse[list[WaliKelasResponse]], summary="Get all homeroom teachers")
async def get_all(service: WaliKelasService = Depends(get_wali_kelas_service)):
    data = service.get_all()
    return BaseResponse(data=data, message=f"Ditemukan {len(data)} wali kelas")


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
