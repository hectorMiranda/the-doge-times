import arcade
import psutil
import settings.config as cfg
from utilities.doge_logger import DogeLogger
import time

class GameWindow(arcade.Window):
    def __init__(self):
        display_width, display_height = arcade.get_display_size()
        super().__init__(display_width, display_height, cfg.SCREEN_TITLE, resizable=True)
        self.logger = DogeLogger.get_instance()
        self.logger.info(f"{type(self).__name__} initialized")
        self.logger.debug(f"Display width: {display_width}, Display height: {display_height}")
        self.fps_count = 0
        self.memory_usage = 0
        self.start_time = time.time()
        self.fps = 0 

    def on_update(self, delta_time):
        super().on_update(delta_time)
        
        if cfg.WINDOW_PERFORMANCE_METRICS:
            self.fps_count += 1
            current_time = time.time()
            if current_time - self.start_time >= 1:
                self.fps = self.fps_count / (current_time - self.start_time)
                self.fps_count = 0
                self.start_time = current_time
            self.memory_usage = psutil.Process().memory_info().rss / 1024 ** 2  # Memory in MB

    def on_draw(self):
        if cfg.WINDOW_PERFORMANCE_METRICS:
            arcade.draw_text(f"FPS: {self.fps:.2f}", 10, self.height - 20, arcade.color.WHITE, 12)
            arcade.draw_text(f"Memory: {self.memory_usage:.2f} MB", 10, self.height - 40, arcade.color.WHITE, 12)
            
            arcade.draw_text("Journey to the moon!", 10, 30 , arcade.color.WHITE, font_size=10, anchor_x="left", font_name="Kenney Future")
            arcade.draw_text("python arcade edition: V 0.0.1", 10,10, arcade.color.ORANGE, font_size=8, anchor_x="left", font_name="Kenney Future")                        
 
        
        super().on_draw()

        
