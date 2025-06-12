import os

class Settings:
    SECRET_KEY = "hello"
    DATABASE_URL = "postgresql://postgres:123456@localhost:5432/ecommerce"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    REFRESH_TOKEN_EXPIRE_DAYS = 7
    ALGORITHM = "HS256"

settings = Settings()
