from fastapi import FastAPI
from sqlalchemy.orm import Session
from .core.database import SessionLocal ,Base ,Engine
from sqlalchemy.exc import SQLAlchemyError
from app.auth.routes import router as auth_router

app = FastAPI(title="ecommerce backend using fastapi")


Base.metadata.create_all(bind=Engine)

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

@app.get("/") # decorater that wraps the function
async def root():
  return {"message":"This is the root path to all the api's"}




