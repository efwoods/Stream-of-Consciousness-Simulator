from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, Response

import uvicorn
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from contextlib import asynccontextmanager

# Configurations & Metrics
from core.config import settings
from core.monitoring import metrics
from core.logging import logger
from service.simulate import load_simulated_eeg_data

# API Routes
from api.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize Mock data
    if load_simulated_eeg_data():
        logger.info("Simulated EEG data loaded successfully")
    else:
        logger.error("Failed to load simulated EEG data")
        raise RuntimeError("Simulated EEG data loading failed")
    
    yield  # Application runs here

    # Shutdown: (optional cleanup)
    # e.g., release resources or shutdown thread pools

app = FastAPI(title="Simulated EEG Data Generation", root_path="/stream-of-consciousness-simulator-api", lifespan=lifespan)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, prefix="/simulate", tags=["Simulate"])

@app.get("/")
async def root(request: Request):
    return RedirectResponse(url=request.scope.get("root_path", "") + "/docs")

@app.get("/health")
async def health():
    metrics.health_requests.inc()
    return {"status": "healthy"}