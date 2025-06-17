from fastapi import FastAPI, Security, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer

from .core.database import SessionLocal, Base, Engine
from app.auth.routes import router as auth_router
from app.products.routes import router as product_router
from app.products.public_routes import router as public_product_router
from app.cart.routes import router as cart_router
from app.checkout.routes import router as checkout_router
from app.orders.routes import router as orders_router
from app.core.logging import logger
from app.utils.handlers import (
    ProductNotFound,
    UnauthorizedAction,
    InvalidQueryParam,
    product_not_found_handler,
    unauthorized_action_handler,
    invalid_query_param_handler
)


app = FastAPI(title="ecommerce backend using fastapi")
logger.info("App restarted")


app.add_exception_handler(ProductNotFound, product_not_found_handler)
app.add_exception_handler(UnauthorizedAction, unauthorized_action_handler)
app.add_exception_handler(InvalidQueryParam, invalid_query_param_handler)


Base.metadata.create_all(bind=Engine)


app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(product_router, prefix="/admin/products", tags=["Admin - Products"])
app.include_router(public_product_router, prefix="/products", tags=["Public - Products"])
app.include_router(cart_router, prefix="/cart", tags=["User - Cart"])
app.include_router(checkout_router, prefix="", tags=["User - Checkout"])
app.include_router(orders_router, prefix="/orders", tags=["Order History and Details"])

# Root route
@app.get("/")
async def root():
    return {"message": "This is the root path to all the api's"}

# Swagger Auth
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
