import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import crud, schemas
from database import SessionLocal
from sqlalchemy.exc import SQLAlchemyError
import webscraper
from typing import List
from exception_handlers import sqlalchemy_exception_handler
import logging
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sentry_sdk.integrations.logging import LoggingIntegration
import os

# Configure logging and Sentry
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

sentry_logging = LoggingIntegration(
    level=logging.INFO,        # Capture info and above as breadcrumbs
    event_level=logging.ERROR  # Send errors as events
)

sentry_sdk.init(
    dsn=os.environ['SENTRY_DSN'],
    integrations=[sentry_logging],
    traces_sample_rate=1.0,
)

app = FastAPI()
app.add_middleware(SentryAsgiMiddleware)
app.exception_handler(SQLAlchemyError)(sqlalchemy_exception_handler)
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Allows cors for everyone **Ignore**
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.get("/")
def main():
    logger.debug("Redirecting to /docs")
    return RedirectResponse(url="/docs")
    
@app.get("/sentry-debug")
def trigger_error():
    division_by_zero = 1 / 0

@app.get("/top-movies/{platform_name}", response_model=schemas.PlatformWithMovies, tags=["Movies"])
def get_top_movies_by_platform(platform_name: str, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    top_movies = crud.get_top_movies_by_platform(db, platform_name, skip, limit)
    if not top_movies:
        raise HTTPException(status_code=404, detail="Platform not found")
    movies = [top_movie for top_movie in top_movies]
    print(type(movies))
    print(movies)
    return schemas.PlatformWithMovies(platform_name=platform_name, movies=movies, length=len(movies))

@app.get("/top-tv-shows/{platform_name}", response_model=schemas.PlatformWithTVShows, tags=["TV Shows"])
def get_top_tv_shows_by_platform(platform_name: str, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    top_tv_shows = crud.get_top_tv_shows_by_platform(db, platform_name, skip, limit)
    if not top_tv_shows:
        raise HTTPException(status_code=404, detail="Platform not found")
    tv_shows = [top_tv_show for top_tv_show in top_tv_shows]
    print(type(tv_shows))
    print(tv_shows)
    return schemas.PlatformWithTVShows(platform_name=platform_name, tv_shows=tv_shows, length=len(tv_shows))

@app.post("/update", status_code=500)
def update_database(db: Session = Depends(get_db)):
    try:
        platforms_data = webscraper.get_all_platforms()
        crud.update_platforms(db, platforms_data)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(detail=f"Failed to update the database: {str(e)}")
    except Exception as e:
        raise HTTPException(detail=f"Failed to update the database: {str(e)}")
    else:
        db.commit()
        return {"message": "Database updated successfully!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
