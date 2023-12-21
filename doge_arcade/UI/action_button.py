    
import arcade.gui


class ActionButton(arcade.gui.UIFlatButton):
    def __init__(self, action, text, center_x, center_y, width, height):
        super().__init__(text, center_x=center_x, center_y=center_y, width=width, height=height)
        self.action = action

    def on_click(self):
        self.action()
