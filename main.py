from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import JSONResponse

from database import Base, create_tables_if_not_exist
from server.router import router

app = FastAPI(
    title='DummyMessenger'
)


@app.on_event("startup")
async def startup_event():
    """Создаёт все таблицы при запуске приложения"""
    create_tables_if_not_exist()


@app.exception_handler(ResponseValidationError)
async def validation_exception_handler(request: Request, exc: ResponseValidationError):
    """Exception_handler - это декоратор, который обрабатывает ошибки.
    ResponseValidationError работает только для response_model.
    Функция позволяет показать ошибку пользователю"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({'detail': exc.errors()})
    )


app.include_router(router)
