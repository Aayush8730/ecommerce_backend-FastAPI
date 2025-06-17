# handlers.py
from fastapi.responses import JSONResponse
from fastapi import Request

class ProductNotFound(Exception):
    def __init__(self, product_id: int):
        self.product_id = product_id

class UnauthorizedAction(Exception):
    def __init__(self, message: str = "You are not authorized to perform this action"):
        self.message = message

class InvalidQueryParam(Exception):
    def __init__(self, message: str):
        self.message = message

async def product_not_found_handler(request: Request, exc: ProductNotFound):
    return JSONResponse(
        status_code=404,
        content={"detail": f"Product with ID {exc.product_id} not found"}
    )

async def unauthorized_action_handler(request: Request, exc: UnauthorizedAction):
    return JSONResponse(
        status_code=403,
        content={"detail": exc.message}
    )


async def invalid_query_param_handler(request: Request, exc: InvalidQueryParam):
    return JSONResponse(status_code=400, content={"detail": exc.message})