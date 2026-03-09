import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from routes.auth import router as auth_router
from routes.cases import router as cases_router
from routes.ai import router as ai_router

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Nyaysetu Case Management System",
    description="API for judicial case management system",
    version="1.0.0"
)

# CORS configuration (NFR2.5)
# Load allowed origins from environment variable, default to localhost:3000 for development
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
cors_origins = [origin.strip() for origin in cors_origins]  # Remove whitespace

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000", "http://localhost:8000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# Include routers
app.include_router(auth_router)
app.include_router(cases_router)
app.include_router(ai_router)

@app.get("/")
def read_root():
    return {"message": "Nyaysetu Case Management System API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
