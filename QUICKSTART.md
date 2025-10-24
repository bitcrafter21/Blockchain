# 🚀 Quick Start Guide

Get your Oilseed Hedging Platform running in 5 minutes!

## ✅ What's Included

This is a **complete, working MVP** for the Smart India Hackathon combining:
- 🤖 **AI Price Forecasting** - ARIMA model predicting 7-day prices for Soybean, Mustard, and Groundnut
- 🔗 **Blockchain Contracts** - Solidity smart contract on Polygon Mumbai testnet
- 🌐 **REST API** - FastAPI backend with all endpoints functional
- 💻 **Web Interface** - Streamlit dashboard for easy interaction

## 🎯 Current Status

✅ **Application is RUNNING** on port 5000  
✅ **All 3 commodities working** (Soybean, Mustard, Groundnut)  
✅ **API endpoints tested** and functional  
⚠️ **Blockchain requires configuration** (see below)

## 📱 Access the Application

**Open the web interface:** The Streamlit app is running on port 5000

### Available Features Right Now:

1. **Price Prediction Tab** 
   - Select commodity (Soybean, Mustard, or Groundnut)
   - Adjust forecast days (1-30)
   - Click "Get Prediction"
   - View interactive charts and recommendations

2. **Blockchain Features** (requires setup)
   - Create forward contracts
   - Sign contracts as buyer
   - View contract details

## 🧪 Test the API Directly

```bash
# Get price prediction for Soybean
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"commodity": "Soybean", "days": 7}'

# Check API status
curl http://localhost:8000/

# Check blockchain status
curl http://localhost:8000/blockchain/status
```

## 🔧 Blockchain Setup (Optional for Demo)

To enable blockchain features:

1. **Deploy Smart Contract**
   - Open [Remix IDE](https://remix.ethereum.org/)
   - Load `blockchain/ForwardContract.sol`
   - Deploy to Polygon Mumbai testnet
   - Copy contract address

2. **Get Test MATIC**
   - Visit [Polygon Faucet](https://faucet.polygon.technology/)
   - Request test tokens for gas fees

3. **Configure Environment**
   - Create `.env` file (copy from `.env.example`)
   - Add your contract address and private key
   - Restart the application

**See DEPLOYMENT.md for detailed blockchain setup instructions**

## 📊 Sample Use Cases

### Use Case 1: Price Forecasting
1. Open the web interface
2. Select "Mustard" from dropdown
3. Set forecast to 7 days
4. Click "Get Prediction"
5. View trend analysis and recommendation

### Use Case 2: Forward Contract (with blockchain)
1. Get price prediction showing upward trend
2. Go to "Create Contract" tab
3. Enter commodity, quantity, and price
4. Submit to blockchain
5. Share contract ID with buyer

## 🎓 Hackathon Demo Tips

1. **Show AI Prediction First**
   - Demonstrate all 3 commodities working
   - Explain ARIMA model briefly
   - Show price trend recommendations

2. **Show Smart Contract**
   - Display `ForwardContract.sol` code
   - Explain farmer/buyer signing process
   - Show event emissions

3. **Show Architecture**
   - FastAPI + Web3.py integration
   - Polygon Mumbai deployment
   - End-to-end flow diagram

4. **Business Impact**
   - Price certainty for farmers
   - Supply guarantee for buyers
   - Transparent blockchain records

## 📁 Project Structure

```
.
├── backend/          # FastAPI server + ML model
├── blockchain/       # Solidity smart contract
├── data/             # Price datasets (3 commodities)
├── frontend/         # Streamlit web interface
├── README.md         # Full documentation
├── DEPLOYMENT.md     # Deployment guide
└── QUICKSTART.md     # This file
```

## 🆘 Common Issues

**"Blockchain Not Configured"**
- Normal! Blockchain features require manual setup
- The AI prediction features work without blockchain
- See DEPLOYMENT.md to enable blockchain

**"API Connection Error"**
- Ensure both backend and frontend are running
- Check if port 8000 is accessible
- Restart the application

**"Prediction Failed"**
- Check commodity name spelling
- Ensure data file exists
- Restart application to reload data

## 📖 Learn More

- **README.md** - Complete project documentation
- **DEPLOYMENT.md** - Step-by-step blockchain deployment
- **backend/app.py** - API endpoint documentation
- **blockchain/ForwardContract.sol** - Smart contract source

## 💡 Next Steps

1. ✅ Test all 3 commodity predictions
2. ✅ Review smart contract code
3. ⚠️ Deploy to Polygon Mumbai (optional)
4. ⚠️ Configure blockchain credentials
5. ✅ Prepare hackathon presentation

---

**Built for Smart India Hackathon 2025**  
**Made with ❤️ for Indian Farmers**
