# 🌾 Oilseed Hedging Platform

**AI-Powered Price Prediction & Blockchain Forward Contracts for Indian Farmers**

A complete MVP solution for the Smart India Hackathon problem statement on hedging platform for oilseed price risk management. This platform combines machine learning price forecasting with blockchain-based smart contracts to help farmers and buyers manage price volatility.

---

## 🎯 Problem Statement

Indian oilseed farmers face heavy price volatility due to lack of hedging tools. This platform enables farmers and buyers to virtually hedge their crop prices using:

- **AI Predictive Analytics** - 7-day price forecasts using ARIMA models
- **Blockchain Forward Contracts** - Transparent, immutable contracts on Polygon Mumbai testnet

---

## ✨ Features

### 1️⃣ AI Price Prediction
- ARIMA-based forecasting model
- 7-day price predictions for oilseeds (Soybean, Mustard, Groundnut)
- Market trend analysis and recommendations
- Historical price data visualization

### 2️⃣ Blockchain Smart Contracts
- Create forward contracts with commodity, quantity, price, and delivery date
- Farmer and buyer signing mechanism
- Automatic contract settlement when both parties sign
- Event emission for ContractCreated, Signed, and Settled
- Deployed on Polygon Mumbai Testnet

### 3️⃣ REST API Backend
- FastAPI-based high-performance API
- `/predict` - Get price predictions
- `/create_contract` - Create blockchain contracts
- `/sign_contract` - Sign existing contracts
- `/get_contract/{id}` - Retrieve contract details

### 4️⃣ Interactive Frontend
- Streamlit-based user interface
- Real-time price prediction visualization
- Contract creation and management
- Blockchain status monitoring

---

## 📁 Project Structure

```
.
├── backend/
│   ├── app.py              # FastAPI main application
│   ├── ml_model.py         # ARIMA price prediction model
│   └── blockchain.py       # Web3 blockchain integration
├── blockchain/
│   ├── ForwardContract.sol # Solidity smart contract
│   └── DEPLOYMENT.md       # Blockchain deployment guide
├── data/
│   └── prices.csv          # Sample oilseed price dataset
├── frontend/
│   └── streamlit_app.py    # Streamlit web interface
├── .env.example            # Environment variables template
├── README.md               # This file
└── DEPLOYMENT.md           # Detailed deployment instructions
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12
- MetaMask wallet with Polygon Mumbai testnet configured
- Infura account or PublicNode RPC access

### Installation

1. **Install Dependencies**
```bash
pip install fastapi uvicorn pandas numpy statsmodels web3 python-dotenv streamlit plotly requests
```

2. **Configure Environment**
```bash
cp .env.example .env
# Edit .env and add your blockchain credentials
```

3. **Run Backend API**
```bash
cd backend
python app.py
```
API will be available at `http://localhost:8000`

4. **Run Frontend (in new terminal)**
```bash
streamlit run frontend/streamlit_app.py
```
Frontend will open at `http://localhost:8501`

---

## 🔗 Blockchain Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete blockchain deployment instructions.

**Quick Overview:**

1. Deploy `ForwardContract.sol` to Polygon Mumbai using Remix IDE
2. Copy contract address to `.env`
3. Add your wallet private key to `.env`
4. Test contract creation via API

---

## 📊 API Endpoints

### Price Prediction
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"commodity": "Soybean", "days": 7}'
```

### Create Contract
```bash
curl -X POST http://localhost:8000/create_contract \
  -H "Content-Type: application/json" \
  -d '{
    "commodity": "Soybean",
    "quantity": 100,
    "price_per_unit": 5000,
    "delivery_date": "2025-12-31",
    "farmer_address": "0x..."
  }'
```

### Get Contract Details
```bash
curl http://localhost:8000/get_contract/1
```

---

## 🧪 How It Works

### AI Price Prediction
1. Historical price data loaded from `prices.csv`
2. ARIMA(2,1,2) model trained on historical prices
3. Forecast generated for next 7 days
4. Trend analysis and recommendations provided

### Blockchain Contracts
1. **Farmer** creates forward contract with commodity details
2. Contract stored immutably on Polygon Mumbai blockchain
3. **Buyer** discovers and signs the contract
4. Once both parties sign, contract automatically settles
5. All events recorded on blockchain for transparency

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| Backend | FastAPI + Python 3.12 |
| ML Model | ARIMA (statsmodels) |
| Blockchain | Solidity + Web3.py |
| Network | Polygon Mumbai Testnet |
| Frontend | Streamlit + Plotly |
| Data Processing | Pandas + NumPy |

---

## 📈 Sample Use Case

**Scenario:** A soybean farmer wants to hedge against price drops

1. Farmer checks AI prediction → sees prices may fall by 5%
2. Farmer creates forward contract at current price (₹5000/quintal)
3. Buyer accepts contract on blockchain
4. Both parties sign → contract settled
5. Farmer protected from price volatility

**Result:** Farmer has price certainty, buyer gets supply guarantee

---

## 🔐 Security Notes

- Never commit `.env` file with private keys
- Use testnet for development
- Mainnet deployment requires security audit
- Store private keys securely (hardware wallet recommended)

---

## 📝 Environment Variables

Create `.env` file with:

```bash
POLYGON_RPC_URL=https://rpc-mumbai.maticvigil.com
CONTRACT_ADDRESS=your_deployed_contract_address
PRIVATE_KEY=your_wallet_private_key
API_BASE_URL=http://localhost:8000
```

---

## 🎓 Learning Resources

- [Polygon Mumbai Faucet](https://faucet.polygon.technology/) - Get test MATIC
- [Remix IDE](https://remix.ethereum.org/) - Deploy smart contracts
- [Web3.py Docs](https://web3py.readthedocs.io/) - Python blockchain integration
- [FastAPI Docs](https://fastapi.tiangolo.com/) - API framework

---

## 🤝 Contributing

This is a hackathon MVP. For production use:
- Add comprehensive testing
- Implement authentication
- Add oracle integration for real-time prices
- Deploy to Polygon mainnet
- Add escrow mechanism for payments

---

## 📄 License

MIT License - Free for educational and commercial use

---

## 👥 Team

Built for Smart India Hackathon 2025

**Problem Statement:** Hedging Platform for Oilseed Price Risk Management

---

## 📞 Support

For issues or questions:
- Check DEPLOYMENT.md for setup help
- Ensure blockchain is configured properly
- Verify API is running before using frontend

---

**Made with ❤️ for Indian Farmers**
# Blockchain
