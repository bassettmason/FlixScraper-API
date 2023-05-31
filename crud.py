from sqlalchemy.orm import Session
from contextlib import contextmanager
import models
from database import SessionLocal
from exception_handlers import handle_db_errors
from pprint import pprint

@handle_db_errors
def get_platform(db: Session, platform_id: int):
    print(platform_id)
    return db.query(models.Platform).filter(models.Platform.id == platform_id).first()
    
@handle_db_errors
def get_platform_by_name(db: Session, name: str):
    print(name)
    return db.query(models.Platform).filter(models.Platform.name == name).first()

@handle_db_errors
def create_platform(db: Session, platform: models.Platform):
    db.add(platform)
    db.commit()
    db.refresh(platform)
    return platform

@handle_db_errors
def get_movie(db: Session, movie_id: int):
    return db.query(models.Movie).filter(models.Movie.id == movie_id).first()

@handle_db_errors
def get_movie_by_title(db: Session, title: str):
    return db.query(models.Movie).filter(models.Movie.title == title).first()

@handle_db_errors
def create_movie(db: Session, movie: models.Movie):
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie

@handle_db_errors
def get_tv_show(db: Session, tv_show_id: int):
    return db.query(models.TVShow).filter(models.TVShow.id == tv_show_id).first()

@handle_db_errors
def get_tv_show_by_title(db: Session, title: str):
    return db.query(models.TVShow).filter(models.TVShow.title == title).first()

@handle_db_errors
def create_tv_show(db: Session, tv_show: models.TVShow):
    db.add(tv_show)
    db.commit()
    db.refresh(tv_show)
    return tv_show

@handle_db_errors
def create_top_movie(db: Session, top_movie: models.TopMovie):
    db.add(top_movie)
    db.commit()
    db.refresh(top_movie)
    return top_movie

@handle_db_errors
def create_top_tv_show(db: Session, top_tv_show: models.TopTVShow):
    db.add(top_tv_show)
    db.commit()
    db.refresh(top_tv_show)
    return top_tv_show
    
@handle_db_errors
def get_top_movies_by_platform(db: Session, platform_name: str, skip: int = 0, limit: int = 10):
    platform = db.query(models.Platform).filter(models.Platform.name == platform_name).first()
    if platform is None:
        return None
    return_answer = db.query(models.TopMovie).filter(models.TopMovie.platform == platform).order_by(models.TopMovie.rank).offset(skip).limit(limit).all()
    print(type(return_answer))
    pprint(return_answer[0].rank)
    return db.query(models.TopMovie).filter(models.TopMovie.platform == platform).order_by(models.TopMovie.rank).offset(skip).limit(limit).all()

@handle_db_errors
def get_top_tv_shows_by_platform(db: Session, platform_name: str, skip: int = 0, limit: int = 10):
    platform = db.query(models.Platform).filter(models.Platform.name == platform_name).first()
    if platform is None:
        return None
    return_answer = db.query(models.TopTVShow).filter(models.TopTVShow.platform == platform).order_by(models.TopTVShow.rank).offset(skip).limit(limit).all()
    print(type(return_answer))
    pprint(return_answer[0].rank)
    return db.query(models.TopTVShow).filter(models.TopTVShow.platform == platform).order_by(models.TopTVShow.rank).offset(skip).limit(limit).all()
@handle_db_errors
def update_platforms(db: Session, platforms_data: dict):
    for platform_name, platform_data in platforms_data.items():
        platform = db.query(models.Platform).filter(models.Platform.name == platform_name).first()
        if not platform:
            platform = models.Platform(name=platform_name)
            db.add(platform)

        # Delete previous day's top movies
        db.query(models.TopMovie).filter(models.TopMovie.platform_id == platform.id).delete()
        # Update top movies
        for rank, title in platform_data['movies'].items():
            movie = db.query(models.Movie).filter(models.Movie.title == title["title"]).first()

            if not movie:
                movie = models.Movie(title=title["title"])
                db.add(movie)
                db.flush()  # Ensure the movie is added to the database so that it has an id

            platform_id = platform.id  # Add a check for platform_id
            if not platform_id:
                # If platform_id is None, get the platform from the database again to ensure that it has been assigned an id
                platform = get_platform_by_name(db, platform_name)
                platform_id = platform.id

            top_movie = models.TopMovie(movie_id=movie.id, platform_id=platform_id, rank=rank)
            create_top_movie(db, top_movie)

        # Delete previous day's top TV shows
        db.query(models.TopTVShow).filter(models.TopTVShow.platform_id == platform.id).delete()
        # Update top TV shows
        for rank, title in platform_data['tv_shows'].items():
            tv_show = db.query(models.TVShow).filter(models.TVShow.title == title["title"]).first()

            if not tv_show:
                tv_show = models.TVShow(title=title["title"])
                db.add(tv_show)
                db.flush()  # Ensure the TV show is added to the database so that it has an id

            platform_id = platform.id  # Add a check for platform_id
            if not platform_id:
                # If platform_id is None, get the platform from the database again to ensure that it has been assigned an id
                platform = get_platform_by_name(db, platform_name)
                platform_id = platform.id

            top_tv_show = models.TopTVShow(tv_show_id=tv_show.id, platform_id=platform_id, rank=rank)
            create_top_tv_show(db, top_tv_show)

    db.commit()
