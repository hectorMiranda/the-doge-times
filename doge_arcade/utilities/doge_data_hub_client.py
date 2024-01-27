
import requests
from settings.config import DOGE_DATA_HUB_ONLINE, DOGE_DATA_SERVICE_URL
from utilities.doge_logger import DogeLogger


class DogeDataHub:
    doge_price= "Loading..."   
    
    
    def get_doge_price(delta_time):
            logger = DogeLogger.get_instance()
            try:
                if DOGE_DATA_HUB_ONLINE:
                    response = requests.get(DOGE_DATA_SERVICE_URL)
                    response.raise_for_status()
                    DogeDataHub.doge_price = response.json()['dogecoin']
                    logger.debug(f"Current Dogecoin price: {DogeDataHub.doge_price}")
                else:
                    DogeDataHub.doge_price = 'N/A (offline)'
            except Exception as e:
                DogeDataHub.doge_price = 'N/A (offline)'
                logger.error(f"Exception details: {e}")
  