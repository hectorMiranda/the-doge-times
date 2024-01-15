import arcade
import settings.config as cfg
from utilities.doge_data_hub_client import DogeDataHub
from views.start_view import StartView
from utilities.doge_logger import DogeLogger
from windows.game_window import GameWindow

def main() -> None:
    try:
        logger = DogeLogger.get_instance()
        window = GameWindow()
        start_view = StartView()
        window.show_view(start_view)
        arcade.schedule(DogeDataHub.get_doge_price, cfg.DOGE_DATA_HUB_CALLING_INTERVAL) 
        arcade.run()
        
    except Exception as e:
        logger.error(f"Exception occurred: {e}", exc_info=True)

if __name__ == "__main__":
    main()