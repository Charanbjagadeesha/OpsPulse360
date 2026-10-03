from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from routers.sales import router as sales_router
from routers.customers import router as customers_router
from routers.inventory import router as inventory_router
from routers.delivery import router as delivery_router
from routers.alerts import router as alerts_router
from routers.stream import router as stream_router
from routers.ml import router as ml_router
from routers.marketing import router as marketing_router

app = FastAPI(
    title="OpsPulse 360 API",
    description="Backend API for the OpsPulse 360 analytics platform",
    version="1.0.0"
)


# Allow the React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://localhost:5175",
        "https://opspulse360-dashboard.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(sales_router)
app.include_router(customers_router)
app.include_router(inventory_router)
app.include_router(delivery_router)
app.include_router(alerts_router)
app.include_router(stream_router)
app.include_router(ml_router)
app.include_router(marketing_router)

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
