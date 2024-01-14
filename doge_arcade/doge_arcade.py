import arcade
import settings.config as cfg
from utilities.doge_data_hub_client import DogeDataHub
from views.start_view import StartView
from utilities.doge_logger import DogeLogger

def main() -> None:
    display_width, display_height = arcade.get_display_size()
    logger = DogeLogger.get_instance()
    logger.debug(f"Display width: {display_width}, Display height: {display_height}")
    window = arcade.Window(display_width, display_height, cfg.SCREEN_TITLE, resizable=True)
    start_view = StartView()
    window.show_view(start_view)
    arcade.schedule(DogeDataHub.get_doge_price, cfg.DOGE_DATA_HUB_CALLING_INTERVAL) 
    arcade.run()

if __name__ == "__main__":
    main()