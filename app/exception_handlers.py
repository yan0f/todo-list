from advanced_alchemy.exceptions import NotFoundError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse


async def not_found_exception_handler(_: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={'message': f'{exc}'},
    )
