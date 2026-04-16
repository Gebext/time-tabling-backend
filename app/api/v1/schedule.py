from fastapi import APIRouter, Depends

from fastapi.responses import FileResponse

from app.dependencies import get_schedule_service

from app.schemas.common import BaseResponse, MessageResponse

from app.schemas.schedule import (

    ScheduleRequest,

    ScheduleStatusResponse,

    ScheduleResult,

    ScheduleSummary,

    ScheduleDetailResponse,

)

from app.services.schedule_service import ScheduleService

router = APIRouter(prefix="/schedule", tags=["Penjadwalan"])

@router.post(

    "/generate",

    response_model=BaseResponse[ScheduleStatusResponse],

    summary="Start schedule generation",

)

async def generate(

    params: ScheduleRequest,

    service: ScheduleService = Depends(get_schedule_service),

):

    status = service.generate(params)

    return BaseResponse(data=status, message="Proses penjadwalan dimulai")

@router.post(
    "/cancel",
    response_model=BaseResponse[ScheduleStatusResponse],
    summary="Cancel schedule generation",
)
async def cancel(service: ScheduleService = Depends(get_schedule_service)):
    status = service.cancel()
    return BaseResponse(data=status, message="Proses penjadwalan dibatalkan")

@router.get(

    "/status",

    response_model=BaseResponse[ScheduleStatusResponse],

    summary="Get generation status",

)

async def get_status(service: ScheduleService = Depends(get_schedule_service)):

    status = service.get_status()

    return BaseResponse(data=status)

@router.get(

    "/latest",

    response_model=BaseResponse[ScheduleResult],

    summary="Get latest schedule result",

)

async def get_latest(service: ScheduleService = Depends(get_schedule_service)):

    result = service.get_latest_result()

    return BaseResponse(data=result, message="Hasil penjadwalan terakhir")

@router.get(

    "/saved",

    response_model=BaseResponse[list[ScheduleSummary]],

    summary="List all saved schedules",

)

async def list_saved(service: ScheduleService = Depends(get_schedule_service)):

    data = service.get_saved_schedules()

    return BaseResponse(data=data, message=f"Ditemukan {len(data)} jadwal tersimpan")

@router.get(

    "/saved/{schedule_id}",

    response_model=BaseResponse[ScheduleDetailResponse],

    summary="Get saved schedule detail",

)

async def get_saved(schedule_id: int, service: ScheduleService = Depends(get_schedule_service)):

    data = service.get_saved_schedule(schedule_id)

    return BaseResponse(data=data)

@router.get(

    "/saved/{schedule_id}/download",

    summary="Download schedule as CSV",

)

async def download_saved(schedule_id: int, service: ScheduleService = Depends(get_schedule_service)):

    csv_path = service.get_schedule_csv_path(schedule_id)

    return FileResponse(

        path=csv_path,

        media_type="text/csv",

        filename=f"schedule_{schedule_id}.csv",

    )

@router.delete(

    "/saved/{schedule_id}",

    response_model=MessageResponse,

    summary="Delete saved schedule",

)

async def delete_saved(schedule_id: int, service: ScheduleService = Depends(get_schedule_service)):

    service.delete_saved_schedule(schedule_id)

    return MessageResponse(message=f"Jadwal #{schedule_id} berhasil dihapus")

