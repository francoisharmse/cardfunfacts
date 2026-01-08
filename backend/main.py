from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from api.aircraft import router as aircraft_router
from api.sports_cars import router as sports_cars_router

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = FastAPI(
    title="Flash Facts Fun API",
    description="Backend API for Flash Facts Fun application",
    version="0.1.0",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(aircraft_router)
app.include_router(sports_cars_router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Flash Facts Fun API",
        "version": "0.1.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
