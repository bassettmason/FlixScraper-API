import psycopg2
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# Fetch the DATABASE_URL from environment variable
DATABASE_URL = os.environ['DATABASE_URL']

# Establish a connection to the PostgreSQL database using psycopg2
conn = psycopg2.connect(DATABASE_URL)

# Create a SQLAlchemy engine using the same DATABASE_URL
engine = create_engine(DATABASE_URL)

# Create a SQLAlchemy session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Define a SQLAlchemy model using declarative_base()
Base = declarative_base()

