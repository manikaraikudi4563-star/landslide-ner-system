"""
NER-LEWS: AI-Based Landslide Risk Monitoring and Early Warning System for North Eastern Region of India.
FastAPI Application Entry Point.
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

from app.config import settings
from app.database import init_db
from app.routes import all_routers

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize database tables and seed records
    print("==================================================")
    print("NER-LEWS: Initializing SQLite Database & Seed Data")
    init_db()
    print("NER-LEWS: Database & Geospatial Layers Ready.")
    print("==================================================")
    yield
    print("NER-LEWS: Shutting down.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Early warning and geotechnical monitoring system for the 8 North Eastern States of India.",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register All API Routers
for r in all_routers:
    app.include_router(r)

# Mount Static Assets
if os.path.exists(settings.STATIC_DIR):
    app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")

@app.get("/")
async def serve_dashboard():
    index_file = os.path.join(settings.STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return JSONResponse(status_code=404, content={"message": "Frontend static file index.html not found"})

# Global Error Handler
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "ERROR",
            "error_code": exc.status_code,
            "detail": exc.detail,
            "path": request.url.path
        }
    )

@app.exception_handler(Exception)
async def custom_general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "status": "SERVER_ERROR",
            "error_code": 500,
            "detail": str(exc),
            "path": request.url.path
        }
    )
