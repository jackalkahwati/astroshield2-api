from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="AstroShield API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    try:
        return {
            "message": "Welcome to AstroShield API",
            "status": "operational",
            "version": "1.0.0"
        }
    except Exception as e:
        logger.error(f"Error in root endpoint: {str(e)}")
        return {"error": "Internal server error", "detail": str(e)}

@app.get("/health")
async def health_check():
    try:
        return {
            "status": "healthy",
            "timestamp": str(datetime.utcnow())
        }
    except Exception as e:
        logger.error(f"Error in health check: {str(e)}")
        return {"error": "Internal server error", "detail": str(e)}

# Configure handler for Vercel serverless
handler = Mangum(app, lifespan="off")
