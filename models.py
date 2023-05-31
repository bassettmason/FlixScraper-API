from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
from database import Base

class Platform(Base):
    __tablename__ = 'platforms'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    top_movies = relationship("TopMovie", back_populates="platform")
    top_tv_shows = relationship("TopTVShow", back_populates="platform")

class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), unique=True, nullable=False)

class TVShow(Base):
    __tablename__ = 'tv_shows'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), unique=True, nullable=False)

class TopMovie(Base):
    __tablename__ = 'top_movies'

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False)
    platform_id = Column(Integer, ForeignKey('platforms.id'), nullable=False)
    rank = Column(Integer, nullable=False)
    
    platform = relationship("Platform", back_populates="top_movies")
    movie = relationship("Movie")

class TopTVShow(Base):
    __tablename__ = 'top_tv_shows'

    id = Column(Integer, primary_key=True, index=True)
    tv_show_id = Column(Integer, ForeignKey('tv_shows.id'), nullable=False)
    platform_id = Column(Integer, ForeignKey('platforms.id'), nullable=False)
    rank = Column(Integer, nullable=False)
    
    platform = relationship("Platform", back_populates="top_tv_shows")
    tv_show = relationship("TVShow")

