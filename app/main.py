"""
FastAPI application entry point.

Main application configuration with CORS, routers, and error handling.
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from app.routers import (
    auth,
    students,
    classes,
    attendance,
    evaluations,
    finance,
    dashboard
)
from app import db

# Initialize FastAPI app
app = FastAPI(
    title="Academia Digital API",
    description="Backend API for Academia Digital POC - FastAPI with JSON file storage",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
# Allow all origins for development (restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(students.router)
app.include_router(classes.router)
app.include_router(attendance.router)
app.include_router(evaluations.router)
app.include_router(finance.router)
app.include_router(dashboard.router)


@app.on_event("startup")
async def startup_event():
    """Initialize data files on startup."""
    # Ensure all JSON files exist with empty lists
    db.ensure_file_exists('students.json')
    db.ensure_file_exists('classes.json')
    db.ensure_file_exists('attendance.json')
    db.ensure_file_exists('evaluations.json')
    db.ensure_file_exists('finance.json')
    db.ensure_file_exists('users.json')


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors."""
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "message": str(exc) if str(exc) else "An unexpected error occurred"
        }
    )


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "message": "Academia Digital API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
