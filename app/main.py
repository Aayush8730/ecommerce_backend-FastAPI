from fastapi import FastAPI
from sqlalchemy.orm import Session
from .core.database import SessionLocal ,Base ,Engine
from sqlalchemy.exc import SQLAlchemyError

app = FastAPI(title="ecommerce backend using fastapi")


Base.metadata.create_all(bind=Engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/") # decorater that wraps the function
async def root():
  return {"message":"This is the root path to all the api's"}



