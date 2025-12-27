from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings

settings = get_settings()

app = FastAPI(title=settings.APP_NAME)

# CORS per permettere richieste da React Native
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In produzione, specifica il dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to Spendly API"}


@app.get("/health")
async def health():
    return {"status": "healthy"}