from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from fastapi import FastAPI, Depends, HTTPException, Request

def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=500,
        content={"detail": f"An error occurred while interacting with the database: {str(exc)}"},
    )

def handle_db_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error occurred: {str(e)}")
    return wrapper

