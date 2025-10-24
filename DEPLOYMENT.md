# 🚀 Deployment Guide - Oilseed Hedging Platform

Complete step-by-step guide to deploy the blockchain-based hedging platform.

---

## 📋 Prerequisites

### 1. MetaMask Wallet Setup
1. Install [MetaMask](https://metamask.io/) browser extension
2. Create a new wallet or import existing one
3. **Save your seed phrase securely!**

### 2. Polygon Mumbai Testnet Configuration

Add Mumbai network to MetaMask:
- **Network Name:** Polygon Mumbai
- **RPC URL:** `https://rpc-mumbai.maticvigil.com`
- **Chain ID:** 80001
- **Currency Symbol:** MATIC
- **Block Explorer:** `https://mumbai.polygonscan.com/`

### 3. Get Test MATIC

Visit [Polygon Faucet](https://faucet.polygon.technology/) and request test MATIC tokens (needed for gas fees).

---

## 🔧 Step 1: Environment Setup

### Install Python Dependencies

```bash
pip install fastapi uvicorn pandas numpy statsmodels web3 python-dotenv streamlit plotly requests
```

### Verify Installation

```bash
python --version  # Should be 3.12+
pip list | grep -E "fastapi|web3|statsmodels|streamlit"
```

---

## 📝 Step 2: Deploy Smart Contract to Polygon Mumbai

### Option A: Using Remix IDE (Recommended for Beginners)

1. **Open Remix IDE**
   - Go to [https://remix.ethereum.org/](https://remix.ethereum.org/)

2. **Create New File**
   - Create `ForwardContract.sol`
   - Copy contents from `blockchain/ForwardContract.sol`

3. **Compile Contract**
   - Click "Solidity Compiler" tab
   - Select compiler version `0.8.0` or higher
   - Click "Compile ForwardContract.sol"
   - Ensure no errors

4. **Deploy to Mumbai**
   - Click "Deploy & Run Transactions" tab
   - Environment: Select "Injected Provider - MetaMask"
   - MetaMask will popup → Connect your wallet
   - Ensure network is "Polygon Mumbai"
   - Click "Deploy"
   - Confirm transaction in MetaMask

5. **Copy Contract Address**
   - After deployment, copy the contract address from Remix
   - Example: `0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb`

### Option B: Using Hardhat (Advanced)

```bash
cd blockchain
npm install --save-dev hardhat @nomicfoundation/hardhat-toolbox
npx hardhat init
```

Create `hardhat.config.js`:
```javascript
require("@nomicfoundation/hardhat-toolbox");

module.exports = {
  solidity: "0.8.0",
  networks: {
    mumbai: {
      url: "https://rpc-mumbai.maticvigil.com",
      accounts: ["YOUR_PRIVATE_KEY_HERE"]
    }
  }
};
```

Create `scripts/deploy.js`:
```javascript
async function main() {
  const ForwardContract = await ethers.getContractFactory("ForwardContract");
  const contract = await ForwardContract.deploy();
  await contract.deployed();
  console.log("ForwardContract deployed to:", contract.address);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
```

Deploy:
```bash
npx hardhat run scripts/deploy.js --network mumbai
```

---

## ⚙️ Step 3: Configure Environment Variables

1. **Copy Environment Template**
```bash
cp .env.example .env
```

2. **Edit .env File**
```bash
# Polygon Mumbai RPC
POLYGON_RPC_URL=https://rpc-mumbai.maticvigil.com

# Your deployed contract address (from Step 2)
CONTRACT_ADDRESS=0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb

# Your MetaMask wallet private key
# ⚠️ WARNING: Keep this secret! Never share or commit to Git!
PRIVATE_KEY=your_private_key_here_without_0x_prefix

# API base URL
API_BASE_URL=http://localhost:8000
```

3. **Get Your Private Key from MetaMask**
   - Open MetaMask
   - Click three dots → Account Details
   - Click "Export Private Key"
   - Enter password
   - Copy private key (remove `0x` prefix if present)
   - **⚠️ NEVER share this key!**

---

## 🚀 Step 4: Start the Application

### Terminal 1: Start Backend API

```bash
cd backend
python app.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### Terminal 2: Start Frontend

```bash
streamlit run frontend/streamlit_app.py
```

Browser will open at `http://localhost:8501`

---

## ✅ Step 5: Verify Deployment

### Test API Health

```bash
curl http://localhost:8000/
```

Expected response:
```json
{
  "message": "Oilseed Hedging Platform API",
  "status": "operational",
  "blockchain_configured": true
}
```

### Test Blockchain Connection

```bash
curl http://localhost:8000/blockchain/status
```

Expected response:
```json
{
  "success": true,
  "configured": true,
  "connected": true,
  "total_contracts": 0
}
```

---

## 📊 Step 6: Test the Platform

### 1. Test Price Prediction

**Via API:**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"commodity": "Soybean", "days": 7}'
```

**Via Frontend:**
1. Open `http://localhost:8501`
2. Go to "Price Prediction" tab
3. Click "Get Prediction"
4. View 7-day forecast chart

### 2. Test Contract Creation

**Via API:**
```bash
curl -X POST http://localhost:8000/create_contract \
  -H "Content-Type: application/json" \
  -d '{
    "commodity": "Soybean",
    "quantity": 100,
    "price_per_unit": 500000,
    "delivery_date": "2025-12-31",
    "farmer_address": "YOUR_METAMASK_ADDRESS"
  }'
```

**Via Frontend:**
1. Go to "Create Contract" tab
2. Fill in contract details
3. Enter your MetaMask address
4. Click "Create Contract"
5. Wait for blockchain confirmation

### 3. Test Contract Signing

**Via API:**
```bash
curl -X POST http://localhost:8000/sign_contract \
  -H "Content-Type: application/json" \
  -d '{
    "contract_id": 1,
    "buyer_address": "BUYER_METAMASK_ADDRESS"
  }'
```

### 4. View Contract Details

**Via API:**
```bash
curl http://localhost:8000/get_contract/1
```

**Via Frontend:**
1. Go to "View Contracts" tab
2. Enter Contract ID: 1
3. Click "Get Contract Details"

---

## 🔍 Verify on Blockchain Explorer

1. Go to [Mumbai PolygonScan](https://mumbai.polygonscan.com/)
2. Search for your contract address
3. View all transactions and events
4. Check ContractCreated, Signed, and Settled events

---

## 🐛 Troubleshooting

### Issue: "Blockchain not configured"

**Solution:**
- Verify `.env` file exists in project root
- Check `CONTRACT_ADDRESS` is correct
- Ensure `PRIVATE_KEY` is set (without 0x prefix)

### Issue: "Cannot connect to RPC"

**Solution:**
- Check internet connection
- Try alternative RPC: `https://matic-mumbai.chainstacklabs.com`
- Verify Mumbai testnet is not down

### Issue: "Insufficient funds"

**Solution:**
- Get test MATIC from [Polygon Faucet](https://faucet.polygon.technology/)
- Wait 1-2 minutes for tokens to arrive
- Check balance in MetaMask

### Issue: "Transaction failed"

**Solution:**
- Ensure delivery date is in the future
- Check quantity and price are > 0
- Verify you have enough gas (test MATIC)

### Issue: "API connection error" in frontend

**Solution:**
- Verify backend is running on port 8000
- Check `API_BASE_URL` in `.env`
- Try `http://localhost:8000` instead of `0.0.0.0`

---

## 📱 Production Deployment

### For Production Use:

1. **Security Audit**
   - Get smart contract audited
   - Implement access controls
   - Add escrow mechanism

2. **Deploy to Polygon Mainnet**
   - Change RPC to Polygon mainnet
   - Use real MATIC for gas
   - Update Chain ID to 137

3. **Backend Hosting**
   - Deploy API to cloud (AWS, GCP, Azure)
   - Use environment secrets management
   - Enable HTTPS

4. **Frontend Hosting**
   - Deploy Streamlit to Streamlit Cloud
   - Or containerize with Docker
   - Set production API URL

5. **Database Integration**
   - Add PostgreSQL for user data
   - Implement caching layer
   - Store historical transactions

---

## 🎯 Demo Flow for Hackathon

### Presentation Steps:

1. **Show Problem Statement** (1 min)
   - Farmer price volatility issue
   - Need for hedging tools

2. **Demo AI Prediction** (2 min)
   - Open frontend
   - Get 7-day forecast
   - Show price trend analysis

3. **Demo Contract Creation** (2 min)
   - Create forward contract
   - Show transaction on blockchain
   - Display contract ID

4. **Demo Contract Signing** (2 min)
   - Buyer signs contract
   - Show automatic settlement
   - View on PolygonScan

5. **Technical Architecture** (2 min)
   - Show code structure
   - Explain ARIMA model
   - Show Solidity contract

6. **Business Impact** (1 min)
   - Price certainty for farmers
   - Supply guarantee for buyers
   - Transparent blockchain records

---

## 📚 Additional Resources

- [Polygon Documentation](https://docs.polygon.technology/)
- [Web3.py Documentation](https://web3py.readthedocs.io/)
- [Solidity Documentation](https://docs.soliditylang.org/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [ARIMA Model Guide](https://www.statsmodels.org/stable/generated/statsmodels.tsa.arima.model.ARIMA.html)

---

## ⚡ Quick Command Reference

```bash
# Start backend
cd backend && python app.py

# Start frontend
streamlit run frontend/streamlit_app.py

# Test API
curl http://localhost:8000/

# Check blockchain status
curl http://localhost:8000/blockchain/status

# Get prediction
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"commodity": "Soybean", "days": 7}'
```

---

## ✅ Deployment Checklist

- [ ] Python 3.12 installed
- [ ] Dependencies installed
- [ ] MetaMask configured with Mumbai
- [ ] Test MATIC obtained
- [ ] Smart contract deployed
- [ ] Contract address copied
- [ ] .env file configured
- [ ] Backend running on port 8000
- [ ] Frontend running on port 8501
- [ ] API health check passes
- [ ] Blockchain connection verified
- [ ] Price prediction tested
- [ ] Contract creation tested
- [ ] Contract verified on PolygonScan

---

**🎉 Congratulations! Your blockchain hedging platform is now live!**

For support, refer to README.md or check the troubleshooting section above.
