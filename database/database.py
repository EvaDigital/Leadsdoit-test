from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
from dotenv import load_dotenv
import os

load_dotenv()

# Get database environment variables from .env file.
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Construct the SQLAlchemy database URL using environment variables.
SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@db/{DB_NAME}"

# Create an SQLAlchemy engine for the database connection.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create database tables based on the models defined in the Base class.
Base.metadata.create_all(bind=engine)

# Create a sessionmaker to handle database sessions.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

