import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os



st.set_page_config(
    page_title="Oilseed Hedging Platform",
    page_icon="🌾",
    layout="wide"
)

st.title("🌾 Oilseed Hedging Platform")
st.markdown("### AI-Powered Price Prediction & Blockchain Forward Contracts")

tab1, tab2, tab3, tab4 = st.tabs(["📊 Price Prediction", "📝 Create Contract", "✅ Sign Contract", "🔍 View Contracts"])

with tab1:
    st.header("AI Price Prediction")
    st.markdown("Get 7-day price forecasts using advanced ARIMA modeling")
    
    col1, col2 = st.columns([2, 1])
    
    with col2:
        commodity = st.selectbox("Select Commodity", ["Soybean", "Mustard", "Groundnut"], key="pred_commodity")
        days = st.slider("Forecast Days", 1, 30, 7)
        
        if st.button("🔮 Get Prediction", type="primary"):
            with st.spinner("Analyzing market data..."):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/predict",
                        json={"commodity": commodity, "days": days}
                    )
                    
                    if response.status_code == 200:
                        data = response.json()["data"]
                        
                        st.success("✅ Prediction Generated Successfully!")
                        
                        st.metric(
                            label="Current Price",
                            value=f"₹{data['current_price']:,.2f}/quintal"
                        )
                        
                        col_a, col_b, col_c = st.columns(3)
                        
                        with col_a:
                            st.metric(
                                "Avg Forecast Price",
                                f"₹{data['average_forecast_price']:,.2f}",
                                f"{data['expected_price_change']:+.2f}"
                            )
                        
                        with col_b:
                            st.metric(
                                "Price Change",
                                f"{data['expected_price_change_percent']:+.2f}%"
                            )
                        
                        with col_c:
                            sentiment = "🟢" if data['expected_price_change_percent'] > 0 else "🔴"
                            st.metric("Trend", sentiment)
                        
                        st.info(f"**Recommendation:** {data['recommendation']}")
                        
                        with col1:
                            predictions_df = pd.DataFrame(data['predictions'])
                            
                            fig = go.Figure()
                            
                            fig.add_trace(go.Scatter(
                                x=predictions_df['date'],
                                y=predictions_df['predicted_price'],
                                mode='lines+markers',
                                name='Predicted Price',
                                line=dict(color='#1f77b4', width=3),
                                marker=dict(size=8)
                            ))
                            
                            fig.update_layout(
                                title=f"{commodity} Price Forecast - Next {days} Days",
                                xaxis_title="Date",
                                yaxis_title="Price (₹/quintal)",
                                hovermode='x unified',
                                height=400
                            )
                            
                            st.plotly_chart(fig, use_container_width=True)
                            
                            st.dataframe(
                                predictions_df,
                                use_container_width=True,
                                hide_index=True
                            )
                    
                    else:
                        st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to backend API. Please ensure the server is running.")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

with tab2:
    st.header("Create Forward Contract")
    st.markdown("Create a blockchain-based forward contract for price hedging")
    
    col1, col2 = st.columns(2)
    
    with col1:
        contract_commodity = st.selectbox("Commodity", ["Soybean", "Mustard", "Groundnut"], key="contract_commodity")
        quantity = st.number_input("Quantity (quintals)", min_value=1, value=100)
        price_per_unit = st.number_input("Price per Quintal (₹)", min_value=1, value=5000)
    
    with col2:
        delivery_date = st.date_input(
            "Delivery Date",
            min_value=datetime.now().date() + timedelta(days=1),
            value=datetime.now().date() + timedelta(days=30)
        )
        farmer_address = st.text_input(
            "Farmer Wallet Address",
            placeholder="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
        )
    
    st.info("💡 **Note:** You need to configure blockchain settings in `.env` file to create contracts.")
    
    if st.button("📝 Create Contract", type="primary"):
        if not farmer_address:
            st.error("Please enter farmer wallet address")
        else:
            with st.spinner("Creating contract on blockchain..."):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/create_contract",
                        json={
                            "commodity": contract_commodity,
                            "quantity": quantity,
                            "price_per_unit": price_per_unit,
                            "delivery_date": delivery_date.strftime('%Y-%m-%d'),
                            "farmer_address": farmer_address
                        }
                    )
                    
                    if response.status_code == 200:
                        result = response.json()["data"]
                        st.success("✅ Contract Created Successfully!")
                        st.json(result)
                        st.balloons()
                    else:
                        error_detail = response.json().get('detail', 'Unknown error')
                        if "not configured" in error_detail:
                            st.warning("⚠️ Blockchain not configured. See deployment documentation to set up Polygon Mumbai testnet.")
                        else:
                            st.error(f"Error: {error_detail}")
                
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to backend API")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

with tab3:
    st.header("Sign Contract (Buyer)")
    st.markdown("Accept and sign an existing forward contract")
    
    col1, col2 = st.columns(2)
    
    with col1:
        contract_id = st.number_input("Contract ID", min_value=1, value=1)
    
    with col2:
        buyer_address = st.text_input(
            "Buyer Wallet Address",
            placeholder="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
        )
    
    if st.button("✅ Sign Contract", type="primary"):
        if not buyer_address:
            st.error("Please enter buyer wallet address")
        else:
            with st.spinner("Signing contract on blockchain..."):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/sign_contract",
                        json={
                            "contract_id": contract_id,
                            "buyer_address": buyer_address
                        }
                    )
                    
                    if response.status_code == 200:
                        result = response.json()["data"]
                        st.success("✅ Contract Signed Successfully!")
                        st.json(result)
                        st.balloons()
                    else:
                        error_detail = response.json().get('detail', 'Unknown error')
                        if "not configured" in error_detail:
                            st.warning("⚠️ Blockchain not configured")
                        else:
                            st.error(f"Error: {error_detail}")
                
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to backend API")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

with tab4:
    st.header("View Contract Details")
    
    view_contract_id = st.number_input("Enter Contract ID", min_value=1, value=1, key="view_contract")
    
    if st.button("🔍 Get Contract Details"):
        with st.spinner("Fetching contract from blockchain..."):
            try:
                response = requests.get(f"{API_BASE_URL}/get_contract/{view_contract_id}")
                
                if response.status_code == 200:
                    contract = response.json()["data"]
                    
                    st.success("✅ Contract Found!")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Contract ID", contract['contract_id'])
                        st.metric("Commodity", contract['commodity'])
                        st.metric("Quantity", f"{contract['quantity']} quintals")
                    
                    with col2:
                        st.metric("Price/Unit", f"₹{contract['price_per_unit']}")
                        st.metric("Total Value", f"₹{contract['total_value']:,}")
                        st.metric("Delivery Date", contract['delivery_date'])
                    
                    with col3:
                        st.metric("Status", contract['status'])
                        st.metric("Farmer Signed", "✅" if contract['farmer_signed'] else "❌")
                        st.metric("Buyer Signed", "✅" if contract['buyer_signed'] else "❌")
                    
                    with st.expander("📋 Full Contract Details"):
                        st.json(contract)
                
                else:
                    error_detail = response.json().get('detail', 'Unknown error')
                    if "not configured" in error_detail:
                        st.warning("⚠️ Blockchain not configured")
                    else:
                        st.error(f"Error: {error_detail}")
            
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend API")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

st.sidebar.header("ℹ️ System Status")

try:
    response = requests.get(f"{API_BASE_URL}/blockchain/status")
    if response.status_code == 200:
        status = response.json()
        
        if status.get('configured'):
            st.sidebar.success("✅ Blockchain Connected")
            st.sidebar.info(f"Total Contracts: {status.get('total_contracts', 0)}")
        else:
            st.sidebar.warning("⚠️ Blockchain Not Configured")
            st.sidebar.info("See DEPLOYMENT.md to configure")
except:
    st.sidebar.error("❌ API Offline")

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.markdown("""
This platform helps farmers hedge against price volatility using:
- 🤖 AI price predictions
- 🔗 Blockchain contracts
- 📊 Real-time analytics
""")
