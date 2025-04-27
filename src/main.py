from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from .routers import scenarios, documents, variables
from .core.config import settings

app = FastAPI(
    title="AI-Powered Business Process Automation",
    description="API for automating business processes using AI agents",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(scenarios.router, prefix="/scenarios", tags=["scenarios"])
app.include_router(documents.router, prefix="/documents", tags=["documents"])
app.include_router(variables.router, prefix="/variables", tags=["variables"])

@app.get("/")
async def root():
    return {"message": "Welcome to AI-Powered Business Process Automation API"} 