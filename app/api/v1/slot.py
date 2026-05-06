from fastapi import APIRouter, Depends, Query

from app.dependencies import get_slot_service

from app.schemas.common import BaseResponse, PaginatedResponse, MessageResponse

from app.schemas.slot import SlotCreate, SlotUpdate, SlotResponse

from app.services.slot_service import SlotService

router = APIRouter(prefix="/slot", tags=["Slot Waktu"])

@router.get("", response_model=PaginatedResponse[SlotResponse], summary="Get all time slots (paginated)")

async def get_all(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=1000),
    q: str | None = Query(default=None, description="Search query"),
    service: SlotService = Depends(get_slot_service),
):

    data, total = service.get_paginated(page, per_page, q)

    return PaginatedResponse(data=data, total=total, page=page, per_page=per_page, message=f"Ditemukan {total} slot")

@router.get("/{slot_id}", response_model=BaseResponse[SlotResponse], summary="Get slot by ID")

async def get_by_id(slot_id: int, service: SlotService = Depends(get_slot_service)):

    data = service.get_by_id(slot_id)

    return BaseResponse(data=data)

@router.post("", response_model=BaseResponse[SlotResponse], status_code=201, summary="Create time slot")

async def create(payload: SlotCreate, service: SlotService = Depends(get_slot_service)):

    data = service.create(payload)

    return BaseResponse(data=data, message="Slot berhasil ditambahkan")

@router.put("/{slot_id}", response_model=BaseResponse[SlotResponse], summary="Update time slot")

async def update(slot_id: int, payload: SlotUpdate, service: SlotService = Depends(get_slot_service)):

    data = service.update(slot_id, payload)

    return BaseResponse(data=data, message="Slot berhasil diperbarui")

@router.delete("/{slot_id}", response_model=MessageResponse, summary="Delete time slot")

async def delete(slot_id: int, service: SlotService = Depends(get_slot_service)):

    service.delete(slot_id)

    return MessageResponse(message="Slot berhasil dihapus")
