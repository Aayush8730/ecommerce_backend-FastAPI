from fastapi import FastAPI
from sqlalchemy.orm import Session
from .core.database import SessionLocal ,Base ,Engine
from sqlalchemy.exc import SQLAlchemyError
from app.auth.routes import router as auth_router
from app.products.routes import router as product_router
from app.products.public_routes import router as public_product_router
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel, SecurityScheme as SecuritySchemeModel
from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI, Security, Depends
from fastapi.security import OAuth2PasswordBearer

app = FastAPI(title="ecommerce backend using fastapi")


Base.metadata.create_all(bind=Engine)

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(product_router, prefix="/admin/products", tags=["Admin - Products"])
app.include_router(public_product_router, prefix="/products", tags=["Public - Products"])


@app.get("/") # decorater that wraps the function
async def root():
  return {"message":"This is the root path to all the api's"}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/signin")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Your API",
        version="1.0.0",
        description="API with JWT auth",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for operation in path.values():
            operation["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi




