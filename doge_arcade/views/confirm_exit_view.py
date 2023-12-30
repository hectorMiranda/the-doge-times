import arcade
import arcade.gui
from UI.action_button import ActionButton 

class ConfirmExitView(arcade.View):
    def __init__(self, return_view):
        super().__init__()
        self.return_view = return_view
        self.ui_manager = arcade.gui.UIManager()
        
        display_width, display_height = arcade.get_display_size()

        # Exit button
        self.exit_button = ActionButton(
            action=lambda: arcade.close_window(),
            text="Exit",
            center_x=display_width / 2 - 100,
            center_y=display_height / 2 - 50,
            width=100,
            height=40
        )
        self.ui_manager.add(self.exit_button)

        # Cancel button
        self.cancel_button = ActionButton(
            action=lambda: self.window.show_view(self.return_view),
            text="Cancel",
            center_x=display_width / 2 + 100,
            center_y=display_height / 2 - 50,
            width=100,
            height=40
        )
        self.ui_manager.add(self.cancel_button)

    def on_show(self):
        arcade.set_background_color(arcade.color.GRAY)

    def on_draw(self):
        display_width, display_height = arcade.get_display_size()

        arcade.start_render()
        arcade.draw_text("Are you sure you want to exit?", display_width / 2, display_height / 2 + 50,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_hide_view(self):
        self.ui_manager.unregister_handlers()
