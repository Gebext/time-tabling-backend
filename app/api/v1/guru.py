from fastapi import APIRouter, Depends

from app.dependencies import get_guru_service

from app.schemas.common import BaseResponse, MessageResponse

from app.schemas.guru import GuruCreate, GuruUpdate, GuruResponse

from app.services.guru_service import GuruService

router = APIRouter(prefix="/guru", tags=["Guru"])

@router.get("", response_model=BaseResponse[list[GuruResponse]], summary="Get all teachers")

async def get_all(service: GuruService = Depends(get_guru_service)):

    data = service.get_all()

    return BaseResponse(data=data, message=f"Ditemukan {len(data)} guru")

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
