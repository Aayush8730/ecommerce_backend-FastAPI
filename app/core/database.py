from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_URL = 'postgresql://postgres:123456@localhost:5432/ecommerce'

Engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush=True,bind=Engine)

Base = declarative_base()

