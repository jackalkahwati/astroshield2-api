from fastapi import FastAPI
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def root():
    return {"message": "Hello from AstroShield on Vercel!"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": str(datetime.utcnow())
    }

handler = Mangum(app)
