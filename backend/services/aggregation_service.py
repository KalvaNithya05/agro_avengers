from config.supabase_client import supabase
from datetime import datetime, timedelta
import pandas as pd

class AggregationService:
    def get_30_day_average(self, device_id='pi_01'):
        """
        Fetches last 30 days of data for the device from Supabase and calculates stats.
        Returns dictionary with keys mapping to model features: N, P, K, temperature, humidity, ph, rainfall.
        """
        if not supabase:
            # Fallback for offline/local mode without Supabase connection
            return self._mock_aggregation()

        try:
            thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat()
            
            # Fetch data
            response = supabase.table('sensor_readings')\
                .select('*')\
                .eq('device_id', device_id)\
                .gte('timestamp', thirty_days_ago)\
                .execute()
            
            data = response.data
            if not data:
                print("No data found for aggregation, using mock.")
                return self._mock_aggregation()
                
            df = pd.DataFrame(data)
            
            # Map column names if they differ from model expectation
            # DB: nitrogen, phosphorus, potassium
            # Model: N, P, K
            
            agg = {
                'temperature': round(df['temperature'].mean(), 2),
                'humidity': round(df['humidity'].mean(), 2),
                'ph': round(df['ph'].mean(), 2),
                'N': round(df['nitrogen'].mean(), 2),
                'P': round(df['phosphorus'].mean(), 2),
                'K': round(df['potassium'].mean(), 2),
                # If rainfall is not in DB (fetched from weather API usually), default to 0
                'rainfall': round(df['rainfall'].sum(), 2) if 'rainfall' in df.columns else 100.0 
            }
            return agg
            
        except Exception as e:
            print(f"Aggregation Service Error: {e}")
            return self._mock_aggregation()

    def _mock_aggregation(self):
        """
        Provides dummy aggregated data for testing/demo.
        """
        return {
            'temperature': 28.5,
            'humidity': 62.0,
            'ph': 6.5,
            'N': 90.0,
            'P': 42.0,
            'K': 110.0,
            'rainfall': 120.0
        }
