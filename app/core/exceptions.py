from fastapi import HTTPException, Request, status

from fastapi.responses import JSONResponse

class AppException(Exception):

    def __init__(self, message: str = "Terjadi kesalahan internal."):

        self.message = message

        super().__init__(self.message)

class NotFoundException(AppException):

    def __init__(self, resource: str, identifier: int | str):

        super().__init__(f"{resource} dengan ID {identifier} tidak ditemukan.")

        self.resource = resource

        self.identifier = identifier

class DuplicateException(AppException):

    def __init__(self, resource: str, detail: str = ""):

        message = f"Data {resource} sudah ada."

        if detail:

            message += f" {detail}"

        super().__init__(message)

class ValidationException(AppException):

    def __init__(self, message: str):

        super().__init__(message)

class AlgorithmException(AppException):

    def __init__(self, message: str = "Gagal menjalankan algoritma."):

        super().__init__(message)

async def not_found_handler(_: Request, exc: NotFoundException) -> JSONResponse:

    return JSONResponse(

        status_code=status.HTTP_404_NOT_FOUND,

        content={"success": False, "message": exc.message},

    )

async def duplicate_handler(_: Request, exc: DuplicateException) -> JSONResponse:

    return JSONResponse(

        status_code=status.HTTP_409_CONFLICT,

        content={"success": False, "message": exc.message},

    )

async def validation_handler(_: Request, exc: ValidationException) -> JSONResponse:

    return JSONResponse(

        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,

        content={"success": False, "message": exc.message},

    )

async def algorithm_handler(_: Request, exc: AlgorithmException) -> JSONResponse:

    return JSONResponse(

        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,

        content={"success": False, "message": exc.message},

    )

async def generic_handler(_: Request, exc: AppException) -> JSONResponse:

    return JSONResponse(

        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,

        content={"success": False, "message": exc.message},

    )

EXCEPTION_HANDLERS: dict[type[Exception], object] = {

    NotFoundException: not_found_handler,

    DuplicateException: duplicate_handler,

    ValidationException: validation_handler,

    AlgorithmException: algorithm_handler,

    AppException: generic_handler,

}
