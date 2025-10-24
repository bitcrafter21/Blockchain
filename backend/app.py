from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import os
from ml_model import PricePredictionModel
from blockchain import BlockchainService
import shutil

app = FastAPI(
    title="Oilseed Hedging Platform API",
    description="AI-powered price prediction and blockchain-based forward contracts for oilseed farmers",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ml_model = PricePredictionModel()
blockchain_service = BlockchainService()


class PredictRequest(BaseModel):
    commodity: str = "Soybean"
    days: int = 7


class CreateContractRequest(BaseModel):
    commodity: str
    quantity: int
    price_per_unit: int
    delivery_date: str
    farmer_address: str


class SignContractRequest(BaseModel):
    contract_id: int
    buyer_address: str


@app.get("/")
async def root():
    """API health check and information"""
    return {
        "message": "Oilseed Hedging Platform API",
        "version": "1.0.0",
        "status": "operational",
        "blockchain_configured": blockchain_service.is_configured(),
        "endpoints": {
            "predict": "/predict - Get AI price predictions",
            "historical": "/historical - Get historical price data",
            "create_contract": "/create_contract - Create blockchain forward contract",
            "sign_contract": "/sign_contract - Buyer signs contract",
            "get_contract": "/get_contract/{contract_id} - Get contract details",
            "blockchain_status": "/blockchain/status - Check blockchain connection"
        }
    }


@app.post("/predict")
async def predict_prices(request: PredictRequest):
    """
    Predict future oilseed prices using ARIMA model
    
    - **commodity**: Name of commodity (default: Soybean)
    - **days**: Number of days to forecast (default: 7, max: 30)
    """
    try:
        if request.days < 1 or request.days > 30:
            raise HTTPException(status_code=400, detail="Days must be between 1 and 30")
        
        predictions = ml_model.predict_prices(
            commodity=request.commodity,
            days=request.days
        )
        
        return {
            "success": True,
            "data": predictions
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.get("/historical")
async def get_historical_data(commodity: str = "Soybean", days: int = 30):
    """
    Get historical price data for a commodity
    
    - **commodity**: Name of commodity
    - **days**: Number of recent days to retrieve
    """
    try:
        data = ml_model.get_historical_data(commodity=commodity, days=days)
        return {
            "success": True,
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload_prices")
async def upload_prices(file: UploadFile = File(...)):
    """
    Upload new price data CSV file
    
    CSV format: date,commodity,price_per_quintal
    """
    try:
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="File must be a CSV")
        
        file_location = "data/prices.csv"
        
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        ml_model.load_data()
        
        return {
            "success": True,
            "message": "Price data uploaded successfully",
            "filename": file.filename
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload error: {str(e)}")


@app.get("/blockchain/status")
async def blockchain_status():
    """Check blockchain connection and configuration status"""
    try:
        is_configured = blockchain_service.is_configured()
        total_contracts = blockchain_service.get_total_contracts() if is_configured else 0
        
        return {
            "success": True,
            "configured": is_configured,
            "connected": blockchain_service.w3.is_connected() if blockchain_service.w3 else False,
            "rpc_url": blockchain_service.rpc_url,
            "contract_address": blockchain_service.contract_address if is_configured else None,
            "total_contracts": total_contracts,
            "message": "Blockchain service is operational" if is_configured else "Blockchain not configured. Set CONTRACT_ADDRESS and PRIVATE_KEY in .env"
        }
    except Exception as e:
        return {
            "success": False,
            "configured": False,
            "error": str(e)
        }


@app.post("/create_contract")
async def create_contract(request: CreateContractRequest):
    """
    Create a forward contract on blockchain
    
    - **commodity**: Commodity name
    - **quantity**: Quantity in quintals
    - **price_per_unit**: Price per quintal (in smallest currency unit, e.g., paise)
    - **delivery_date**: Delivery date (YYYY-MM-DD format)
    - **farmer_address**: Ethereum address of the farmer
    """
    try:
        delivery_timestamp = int(datetime.strptime(request.delivery_date, '%Y-%m-%d').timestamp())
        
        result = blockchain_service.create_contract(
            commodity=request.commodity,
            quantity=request.quantity,
            price_per_unit=request.price_per_unit,
            delivery_date_timestamp=delivery_timestamp,
            farmer_address=request.farmer_address
        )
        
        return {
            "success": True,
            "message": "Contract created successfully on blockchain",
            "data": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/sign_contract")
async def sign_contract(request: SignContractRequest):
    """
    Buyer signs a forward contract
    
    - **contract_id**: ID of the contract to sign
    - **buyer_address**: Ethereum address of the buyer
    """
    try:
        result = blockchain_service.sign_contract(
            contract_id=request.contract_id,
            buyer_address=request.buyer_address
        )
        
        return {
            "success": True,
            "message": "Contract signed successfully",
            "data": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get_contract/{contract_id}")
async def get_contract(contract_id: int):
    """
    Get details of a specific contract
    
    - **contract_id**: ID of the contract
    """
    try:
        contract_details = blockchain_service.get_contract_details(contract_id)
        
        return {
            "success": True,
            "data": contract_details
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
