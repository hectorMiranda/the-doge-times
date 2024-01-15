from arcade import View as ArcadeView
from utilities.doge_logger import DogeLogger
import inspect

class BaseView(ArcadeView):
    def __init__(self):
        super().__init__()
        self.logger = DogeLogger.get_instance()
        self.logger.info(f"{type(self).__name__} initialized")
        self.started = False
        self.ui_manager = None
        
    def log_debug(self, message: str):
        caller_method = inspect.currentframe().f_back.f_code.co_name
        self.logger.debug(f"{type(self).__name__}.{caller_method}: {message}")
    
    def log_info(self, message: str):
        caller_method = inspect.currentframe().f_back.f_code.co_name
        self.logger.info(f"{type(self).__name__}.{caller_method}: {message}")


    def setup(self):
        self.started = True

    def on_show(self):
        self.logger.debug(f"{type(self).__name__} is now visible")
        if not self.started:
            self.setup()

        if self.ui_manager:
            self.ui_manager.enable()

    def on_hide_view(self):
        if self.ui_manager:
            self.ui_manager.disable()
            
    def on_draw(self):
        self.logger.debug(f"Rendering {type(self).__name__}")
        super().on_draw()
