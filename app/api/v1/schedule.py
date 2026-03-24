from fastapi import APIRouter, Depends

from app.dependencies import get_schedule_service

from app.schemas.common import BaseResponse

from app.schemas.schedule import (

    ScheduleRequest,

    ScheduleStatusResponse,

    ScheduleResult,

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
