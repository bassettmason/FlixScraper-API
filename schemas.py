from pydantic import BaseModel, constr
from typing import List

class Movie(BaseModel):
    title: constr(strip_whitespace=True, strict=True, max_length=100)

    class Config:
        orm_mode = True

class TVShow(BaseModel):
    title: constr(strip_whitespace=True, strict=True, max_length=100)

    class Config:
        orm_mode = True

class TopMovie(BaseModel):
    movie: Movie
    rank: int

    class Config:
        orm_mode = True

class TopTVShow(BaseModel):
    tv_show: TVShow
    rank: int

    class Config:
        orm_mode = True

class Platform(BaseModel):
    platform_name: constr(strip_whitespace=True, strict=True, max_length=100)
    top_movies: List[TopMovie]
    top_tv_shows: List[TopTVShow]

    class Config:
        orm_mode = True

class PlatformWithMovies(BaseModel):
    platform_name: constr(strip_whitespace=True, strict=True, max_length=100)
    movies: List[TopMovie]
    length: int

    class Config:
        orm_mode = True

class PlatformWithTVShows(BaseModel):
    platform_name: constr(strip_whitespace=True, strict=True, max_length=100)
    tv_shows: List[TopTVShow]
    length: int

    class Config:
        orm_mode = True