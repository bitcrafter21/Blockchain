import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')


class PricePredictionModel:
    def __init__(self, csv_path='data/prices.csv'):
        self.csv_path = csv_path
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Load price data from CSV"""
        try:
            self.df = pd.read_csv(self.csv_path)
            self.df['date'] = pd.to_datetime(self.df['date'])
            self.df = self.df.sort_values('date')
        except Exception as e:
            raise Exception(f"Error loading price data: {str(e)}")
    
    def predict_prices(self, commodity='Soybean', days=7):
        """
        Predict future prices using ARIMA model
        
        Args:
            commodity: Name of the commodity (default: Soybean)
            days: Number of days to forecast (default: 7)
        
        Returns:
            Dictionary with predictions and metadata
        """
        try:
            commodity_data = self.df[self.df['commodity'] == commodity].copy()
            
            if len(commodity_data) == 0:
                raise ValueError(f"No data found for commodity: {commodity}")
            
            prices = commodity_data['price_per_quintal'].values
            
            model = ARIMA(prices, order=(2, 1, 2))
            fitted_model = model.fit()
            
            forecast = fitted_model.forecast(steps=days)
            
            last_date = commodity_data['date'].max()
            forecast_dates = [
                (last_date + timedelta(days=i+1)).strftime('%Y-%m-%d') 
                for i in range(days)
            ]
            
            current_price = float(prices[-1])
            avg_forecast_price = float(np.mean(forecast))
            price_change = avg_forecast_price - current_price
            price_change_pct = (price_change / current_price) * 100
            
            predictions = [
                {
                    'date': forecast_dates[i],
                    'predicted_price': float(forecast[i]),
                    'day': i + 1
                }
                for i in range(days)
            ]
            
            return {
                'commodity': commodity,
                'current_price': current_price,
                'forecast_period_days': days,
                'predictions': predictions,
                'average_forecast_price': avg_forecast_price,
                'expected_price_change': round(price_change, 2),
                'expected_price_change_percent': round(price_change_pct, 2),
                'recommendation': self._get_recommendation(price_change_pct),
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            raise Exception(f"Error in price prediction: {str(e)}")
    
    def _get_recommendation(self, price_change_pct):
        """Generate recommendation based on price change"""
        if price_change_pct > 5:
            return "BULLISH - Prices expected to rise. Good time for farmers to create forward contracts."
        elif price_change_pct < -5:
            return "BEARISH - Prices expected to fall. Good time for buyers to lock in contracts."
        else:
            return "NEUTRAL - Stable prices expected. Consider waiting or hedging moderately."
    
    def get_historical_data(self, commodity='Soybean', days=30):
        """Get recent historical price data"""
        commodity_data = self.df[self.df['commodity'] == commodity].copy()
        recent_data = commodity_data.tail(days)
        
        return {
            'commodity': commodity,
            'data': recent_data[['date', 'price_per_quintal']].to_dict('records')
        }
