import arcade
from settings.constants import DOGE_DATA_HUB_CALLING_INTERVAL, SCREEN_TITLE
from doge_data_hub.shared_data import SharedData
from views.loading_view import LoadingView

def main() -> None:
    display_width, display_height = arcade.get_display_size()
    window = arcade.Window(display_width, display_height, SCREEN_TITLE, resizable=True)
    start_view = LoadingView()
    window.show_view(start_view)
    arcade.schedule(SharedData.get_doge_price, DOGE_DATA_HUB_CALLING_INTERVAL) 
    arcade.run()

if __name__ == "__main__":
    main()
