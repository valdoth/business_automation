from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import auth, documents, variables, scenarios
from src.core.config import settings
from src.db import init_db

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
@app.on_event("startup")
async def startup_event():
    init_db()

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(documents.router, prefix="/documents", tags=["documents"])
app.include_router(variables.router, prefix="/variables", tags=["variables"])
app.include_router(scenarios.router, prefix="/scenarios", tags=["scenarios"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Business Process Automation API"} 