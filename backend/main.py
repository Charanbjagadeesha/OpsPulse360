from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from routers.sales import router as sales_router
from routers.customers import router as customers_router
from routers.inventory import router as inventory_router
from routers.delivery import router as delivery_router
from routers.alerts import router as alerts_router
from routers.stream import router as stream_router
app = FastAPI(
    title="OpsPulse 360 API",
    description="Backend API for the OpsPulse 360 analytics platform",
    version="1.0.0"
)

app.include_router(sales_router)
app.include_router(customers_router)
app.include_router(inventory_router)
app.include_router(delivery_router)
app.include_router(alerts_router)
app.include_router(stream_router)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "An internal server error occurred."
        }
    )

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "OpsPulse 360 API"
    }
