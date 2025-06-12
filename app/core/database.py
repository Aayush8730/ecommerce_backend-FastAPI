from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
from app.core.logging import logger

DATABASE_URL = settings.DATABASE_URL

Engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush=True,bind=Engine)

Base = declarative_base()

from sqlalchemy.exc import OperationalError
from app.core.database import SessionLocal
import logging
from fastapi import HTTPException, status

logger = logging.getLogger("ecommerce")

def get_db():
    try:
        db = SessionLocal()
        logger.info("Connected to the database")
        yield db
    except OperationalError as e:
        logger.critical(f"Database connection failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection error. Please try again later.",
        )
    finally:
            db.close()
            logger.info("Database connection closed")
    

