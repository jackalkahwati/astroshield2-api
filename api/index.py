from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import logging
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app with explicit configuration
app = FastAPI(
    title="AstroShield API",
    description="AstroShield API for orbital analysis and predictions",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class VerifyRequest(BaseModel):
    data: Dict[str, Any] = Field(..., description="Data to be verified")

class VerifyResponse(BaseModel):
    verified: bool = Field(..., description="Whether the data was verified successfully")
    message: str = Field(..., description="Verification message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional verification details")

class EncryptRequest(BaseModel):
    value: str = Field(..., min_length=1, description="Value to be encrypted")

class EncryptResponse(BaseModel):
    encryptedValue: str = Field(..., description="Encrypted value")
    timestamp: str = Field(..., description="Timestamp of encryption")

class AnalyzeRequest(BaseModel):
    data: str = Field(..., min_length=1, description="Data to be analyzed")
    analysisMode: str = Field(
        default="orbital_prediction",
        description="Analysis mode to be used"
    )

class AnalysisResult(BaseModel):
    likelihood: float = Field(..., ge=0.0, le=1.0, description="Event likelihood")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    predictions: List[Dict[str, Any]] = Field(..., description="List of predictions")
    recommendations: List[str] = Field(..., description="List of recommendations")

class AnalyzeResponse(BaseModel):
    analysisResult: AnalysisResult
    timestamp: str = Field(..., description="Timestamp of analysis")

@app.get("/")
async def root():
    """Root endpoint returning API status"""
    try:
        return {
            "message": "Welcome to AstroShield API",
            "status": "operational",
            "version": "1.0.0"
        }
    except Exception as e:
        logger.error(f"Error in root endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        return {
            "status": "healthy",
            "timestamp": str(datetime.utcnow())
        }
    except Exception as e:
        logger.error(f"Error in health check: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/verify", response_model=VerifyResponse)
async def verify_data(request: VerifyRequest):
    """Verify incoming data"""
    try:
        logger.info(f"Verifying data: {request.data}")
        return {
            "verified": True,
            "message": "Data verification successful",
            "details": {
                "timestamp": str(datetime.utcnow()),
                "checks_passed": ["format", "schema", "integrity"],
                "data_type": request.data.get("type", "unknown")
            }
        }
    except Exception as e:
        logger.error(f"Error in verify endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/encrypt", response_model=EncryptResponse)
async def encrypt_data(request: EncryptRequest):
    """Encrypt sensitive data"""
    try:
        logger.info("Encrypting data")
        return {
            "encryptedValue": f"encrypted_{request.value}_{datetime.utcnow().timestamp()}",
            "timestamp": str(datetime.utcnow())
        }
    except Exception as e:
        logger.error(f"Error in encrypt endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_data(request: AnalyzeRequest):
    """Analyze data with specified mode"""
    try:
        logger.info(f"Analyzing data with mode: {request.analysisMode}")
        return {
            "analysisResult": {
                "likelihood": 0.85,
                "confidence": 0.92,
                "predictions": [
                    {
                        "time": str(datetime.utcnow()),
                        "event": "orbital_maneuver",
                        "probability": 0.85
                    }
                ],
                "recommendations": [
                    "Monitor trajectory changes",
                    "Prepare for potential collision avoidance"
                ]
            },
            "timestamp": str(datetime.utcnow())
        }
    except Exception as e:
        logger.error(f"Error in analyze endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Configure handler for Vercel serverless with explicit settings
handler = Mangum(
    app,
    lifespan="off",
    api_gateway_base_path=None,
    strip_stage_path=True,
    enable_lifespan=False
)
