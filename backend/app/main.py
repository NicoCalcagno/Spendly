from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.controllers import auth_router, categories_router, expenses_router, users_router

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered expense tracking API",
    version="1.0.0"
)

# CORS per permettere richieste da React Native
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In produzione, specifica il dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(categories_router, prefix="/api/v1")
app.include_router(expenses_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "message": "Welcome to Spendly API",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}