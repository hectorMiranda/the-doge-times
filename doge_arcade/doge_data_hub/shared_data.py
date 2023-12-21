
import requests
from settings.constants import DOGE_DATA_HUB_ONLINE

class SharedData:
    doge_price= "Loading..."    
    
    def get_doge_price(delta_time):
            try:
                if DOGE_DATA_HUB_ONLINE:
                    response = requests.get('http://localhost:5000/currentPrice')
                    response.raise_for_status()
                    SharedData.doge_price = response.json()['dogecoin']
                    print(f"Current Dogecoin price: {SharedData.doge_price}")
                else:
                    SharedData.doge_price = 'N/A (offline)'
            except Exception as e:
                SharedData.doge_price = 'N/A (offline)'
                print(f"Exception details: {e}")
  