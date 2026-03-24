from fastapi import APIRouter, Depends

from app.dependencies import get_kelas_service

from app.schemas.common import BaseResponse, MessageResponse

from app.schemas.kelas import KelasCreate, KelasUpdate, KelasResponse

from app.services.kelas_service import KelasService

router = APIRouter(prefix="/kelas", tags=["Kelas"])

@router.get("", response_model=BaseResponse[list[KelasResponse]], summary="Get all classes")

async def get_all(service: KelasService = Depends(get_kelas_service)):

    data = service.get_all()

    return BaseResponse(data=data, message=f"Ditemukan {len(data)} kelas")

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
