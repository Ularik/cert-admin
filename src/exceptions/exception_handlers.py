from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from src.exceptions import exceptions


def register_exception_handlers(app):

    @app.exception_handler(exceptions.DepartmentNotFoundException)
    async def not_found_handler(request: Request, exc: exceptions.DepartmentNotFoundException):
        raise HTTPException(status_code=404, detail=exc.detail)

    @app.exception_handler(exceptions.TaskAlreadyExistException)
    async def exist_exception_handler(request: Request, exc: exceptions.TaskAlreadyExistException):
        raise HTTPException(status_code=400, detail=exc.detail)

    @app.exception_handler(exceptions.NoResultException)
    async def not_found_handler(request: Request, exc: exceptions.NoResultException):
        raise HTTPException(status_code=404, detail=exc.detail)
