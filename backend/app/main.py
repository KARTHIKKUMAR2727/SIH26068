from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import db_manager

from app.api.auth import router as auth_router
from app.api.weather import router as weather_router
from app.api.forecast import router as forecast_router
from app.api.alerts import router as alerts_router
from app.api.climate import router as climate_router
from app.api.history import router as history_router
from app.api.nwp import router as nwp_router
from app.api.chat import router as chat_router
from app.api.advisory import router as advisory_router
from app.api.location import router as location_router
from app.api.reports import router as reports_router
from app.api.health import router as health_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: connect to database (or initialize fallback JSON store)
    await db_manager.connect()
    yield
    # Shutdown
    if db_manager.client:
        db_manager.client.close()

app = FastAPI(
    title=f"{settings.PROJECT_NAME} API",
    version=settings.PROJECT_VERSION,
    description="Conversational AI Platform for Weather Forecasting, Extreme Weather Alerts, Climate Analysis, and Decision Support",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(health_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(weather_router, prefix="/api")
app.include_router(forecast_router, prefix="/api")
app.include_router(alerts_router, prefix="/api")
app.include_router(climate_router, prefix="/api")
app.include_router(history_router, prefix="/api")
app.include_router(nwp_router, prefix="/api")
app.include_router(chat_router, prefix="/api")
app.include_router(advisory_router, prefix="/api")
app.include_router(location_router, prefix="/api")
app.include_router(reports_router, prefix="/api")

@app.get("/")
def root():
    return {
        "platform": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "status": "Online",
        "documentation": "/docs"
    }
