import requests
import arcade
import arcade.gui
import pathlib
import constants
import random
import time

ASSETS_PATH = pathlib.Path(__file__).resolve().parent.parent / "assets"

            
class StatusBar:
    def __init__(self, screen_width, bar_height=80):
        self.screen_width = screen_width
        self.bar_height = bar_height
        self.stat_boxes = []
        self.box_width = constants.BOX_WIDTH      
        self.box_height = constants.BOX_HEIGHT
        
        

    def add_stat_box(self, text):
        self.stat_boxes.append({'text': text})
        self._layout_stat_boxes()

    def update_stat_box(self, index, new_text):
        if 0 <= index < len(self.stat_boxes):
            self.stat_boxes[index]['text'] = new_text

    def _layout_stat_boxes(self):
        num_boxes = len(self.stat_boxes)
        total_box_width = num_boxes * self.box_width
        start_x = (self.screen_width - total_box_width) / 2 + self.box_width / 2

        for i, stat_box in enumerate(self.stat_boxes):
            stat_box['x'] = start_x + i * self.box_width
            stat_box['y'] = self.bar_height / 2

    def draw(self):
        # Draw the main status bar
        arcade.draw_rectangle_filled(center_x=self.screen_width / 2, 
                                     center_y=self.bar_height / 2, 
                                     width=self.screen_width, 
                                     height=self.bar_height, 
                                     color=arcade.color.BLACK)

        # Draw each stat box
        for stat_box in self.stat_boxes:
            # Draw the box
            arcade.draw_rectangle_filled(center_x=stat_box['x'], center_y=stat_box['y'],
                                         width=self.box_width, height=self.box_height,
                                         color=arcade.color.GRAY)
            arcade.draw_rectangle_outline(center_x=stat_box['x'], center_y=stat_box['y'],
                                          width=self.box_width, height=self.box_height,
                                          color=arcade.color.WHITE, border_width=2)

            # Draw the text
            text_x = stat_box['x'] - self.box_width / 2 + 10
            text_y = stat_box['y'] - 10
            arcade.draw_text(stat_box['text'], start_x=text_x, start_y=text_y, 
                             color=arcade.color.WHITE, font_size=17, font_name="Kenney Future")



class SharedData:
    doge_price= "Loading..."
    
    display_width, display_height = arcade.get_display_size() # will cause error if called before window is created


    def get_doge_price(delta_time):
            try:
                response = requests.get('http://localhost:5000/currentPrice')
                response.raise_for_status()
                SharedData.doge_price = response.json()['dogecoin']
                print(f"Current Dogecoin price: {SharedData.doge_price}")
            except Exception as e:
                SharedData.doge_price = 'N/A (offline)'
                print(f"Exception details: {e}")
                
    



class LandingView(arcade.View):
    def __init__(self):
        super().__init__()
        self.loading_bar_width = 0
        self.total_loading_time = 1 
        self.start_time = time.time()
        self.loading_complete = False
        self.text_visible = True
        self.blink_timer = 0  
        
    def on_show(self):
        arcade.set_background_color(arcade.color.CORNFLOWER_BLUE)

    def on_draw(self):
        display_width, display_height = arcade.get_display_size()

        arcade.start_render()
        
        arcade.draw_text("Journey to the moon!", display_width / 2, display_height / 2, arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("python arcade edition!", display_width / 2, display_height / 2 -35, arcade.color.ORANGE, font_size=20, anchor_x="center")                         
        
        progress_bar_x = display_width / 2
        progress_bar_y = display_height / 3
        arcade.draw_texture_rectangle(display_width / 5, display_height / 2, 400, 400, arcade.load_texture(str(ASSETS_PATH / "UI" / "doge_mining.png")))
        arcade.draw_rectangle_filled(progress_bar_x, progress_bar_y, self.loading_bar_width, 30, arcade.color.BLUE)
 
        if self.loading_complete and self.text_visible:
            message = arcade.draw_text("Press any key to continue", progress_bar_x, progress_bar_y - 10 , arcade.color.WHITE, font_size=20, font_name="Kenney Future", anchor_x="center")
        elif not self.loading_complete:
            message = arcade.draw_text("Loading ...", progress_bar_x, progress_bar_y - 10 , arcade.color.WHITE, font_size=20, font_name="Kenney Future", anchor_x="center")
   
    def on_update(self, delta_time):
        display_width, display_height = arcade.get_display_size()

        if not self.loading_complete:
            elapsed_time = time.time() - self.start_time
            arcade.get_display_size()
            self.loading_bar_width = (elapsed_time / self.total_loading_time) * display_width
            
            if elapsed_time >= self.total_loading_time:
                self.loading_complete = True

        if self.loading_complete:
            self.blink_timer += delta_time
            if self.blink_timer > 0.5:  # Toggle visibility every 0.5 seconds
                self.text_visible = not self.text_visible
                self.blink_timer = 0

    def on_key_press(self, key, modifiers):
        print(key)
        if key == arcade.key.ESCAPE:  # Check for ESC key
            modal_view = ConfirmExitView(self)  
            self.window.show_view(modal_view)
        elif self.loading_complete:
            game = GameView()
            game.setup()
            self.window.show_view(game)
        
class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.lives = 99
        self.coins = None
        self.background = None
        self.walls = None
        self.ladders = None
        self.goals = None
        self.enemies = None
        self.score = 0
        self.level = 1
        self.display_width, self.display_height = arcade.get_display_size()
        self.doge_price = "Loading..."
        self.background = arcade.load_texture("../assets/backgrounds/launchpad.png")
        
        self.status_bar = StatusBar(screen_width=self.display_width)        
        self.status_bar.add_stat_box(f"Doge Price: {SharedData.doge_price}")
        self.status_bar.add_stat_box("Lives: NA")
        self.status_bar.add_stat_box("Coins: NA")

        
        self.coin_sound = arcade.load_sound(
            str(ASSETS_PATH / "sounds" / "collectable.wav")
        )
        self.jump_sound = arcade.load_sound(
            str(ASSETS_PATH / "sounds" / "bark.wav")
        )
        
        self.player_list = None
        self.wall_list = None
        self.player_sprite = None
        self.physics_engine = None

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = constants.PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -constants.PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = constants.PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.Z:
            self.player_sprite.zoom_in()
        elif key == arcade.key.X:
            self.player_sprite.zoom_out()
        elif key == arcade.key.R:
            self.restart_game()
        elif key == arcade.key.ESCAPE:
            pause_view = ConfirmExitView(self.window.current_view)
            self.show_view(pause_view)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        self.player_sprite.update()
        self.player_sprite.update_animation(delta_time)  
        
    def restart_game(self):
        self.window.show_view(LandingView())
    
    def setup(self):
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)

        self.player_sprite = PlayerCharacter()
        self.player_sprite.center_x = 128
        self.player_sprite.center_y = 126
        self.player_list.append(self.player_sprite)
        
        for x in range(0, 600, 128):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", constants.SPRITE_SCALING_BOX)
            wall.center_x = x
            wall.center_y = 90
            self.wall_list.append(wall)

        coordinate_list = [[200, 180], [300, 300], [400, 400], [500, 400], [600, 400]]

        for coordinate in coordinate_list:
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", constants.TILE_SCALING)
            wall.position = coordinate
            self.wall_list.append(wall)
        
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, gravity_constant=constants.GRAVITY)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(center_x=self.display_width / 2, center_y=self.display_height / 2, width=self.display_width, height=self.display_height, texture=self.background)
        self.status_bar.update_stat_box(0,f"Doge Price: {SharedData.doge_price}")
        self.player_sprite.draw()
        self.wall_list.draw()
        self.player_list.draw()        
        self.status_bar.draw()
        
    def on_update(self, delta_time):
        if self.physics_engine:
            self.physics_engine.update()
            self.player_sprite.update_animation(delta_time)
        
class PlayerCharacter(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.facing_direction = constants.LEFT_FACING
        self.position = (200,200)

        self.idle_textures = []
        self.run_textures = []
        self.spawn_textures = []

        sprite_count = 0 

        for row in range(6):  
            for col in range(7):
                if sprite_count >= constants.SPRITE_IDLE_FRAMES: 
                    break
                idle_texture = arcade.load_texture(str(ASSETS_PATH / "sprites" / "PlayerIdle.png"), x=col * constants.SPRITE_SIZE_WIDTH, y=row * constants.SPRITE_SIZE_HEIGHT, width=constants.SPRITE_SIZE_WIDTH, height=constants.SPRITE_SIZE_HEIGHT)
                self.idle_textures.append(idle_texture)
                sprite_count += 1
        
        print(f"Idle textures: {len(self.idle_textures)}")

        sprite_count = 0 
        
        for row in range(5):  
            for col in range(6): 
                if sprite_count >= constants.SPRITE_RUN_FRAMES: 
                    break

                run_texture = arcade.load_texture(str(ASSETS_PATH / "sprites" / "PlayerRun.png"), x=col * constants.SPRITE_SIZE_WIDTH, y=row * constants.SPRITE_SIZE_HEIGHT, width=constants.SPRITE_SIZE_WIDTH, height=constants.SPRITE_SIZE_HEIGHT)
                self.run_textures.append(run_texture)
                sprite_count += 1
                
        print(f"run textures: {len(self.run_textures)}")
        
        
        sprite_count = 0 
        
        for row in range(4): 
            for col in range(5):  
                if sprite_count >= constants.SPRITE_SPAWN_FRAMES: 
                    break

                spawn_texture = arcade.load_texture(str(ASSETS_PATH / "sprites" / "PlayerSpawn.png"), x=col * constants.SPRITE_SIZE_WIDTH, y=row * constants.SPRITE_SIZE_HEIGHT, width=constants.SPRITE_SIZE_WIDTH, height=constants.SPRITE_SIZE_HEIGHT)
                self.spawn_textures.append(spawn_texture)
                sprite_count += 1
                
        print(f"spawn textures: {len(self.run_textures)}")
        
        
        
        self.character_face_direction = constants.RIGHT_FACING

        # Set the initial texture
        self.texture = self.idle_textures[0]

        # Track our state
        self.jumping = False
        self.is_running = False
        self.cur_texture = 0

    def zoom_in(self):
        self.scale *= 2

    def zoom_out(self):
        self.scale *= 0.5

    def update_animation(self, delta_time: float = 1/60):
        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.facing_direction == constants.RIGHT_FACING:
            self.facing_direction = constants.LEFT_FACING
        elif self.change_x > 0 and self.facing_direction == constants.LEFT_FACING:
            self.facing_direction = constants.RIGHT_FACING

        # Figure out if we're standing still, and set our texture appropriately
        if self.change_x == 0:
            self.cur_texture += 1
            if self.cur_texture > 3 * len(self.idle_textures):
                self.cur_texture = 0
            self.texture = self.idle_textures[(self.cur_texture // 3)-1]
        else:
            # We're moving
            self.cur_texture += 1
            if self.cur_texture > 3 * len(self.run_textures):
                self.cur_texture = 0
            self.texture = self.run_textures[(self.cur_texture // 3)-1]

class ActionButton(arcade.gui.UIFlatButton):
    def __init__(self, action, text, center_x, center_y, width, height):
        super().__init__(text, center_x=center_x, center_y=center_y, width=width, height=height)
        self.action = action

    def on_click(self):
        self.action()

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
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        display_width, display_height = arcade.get_display_size()

        arcade.start_render()
        arcade.draw_text("Are you sure you want to exit?", display_width / 2, display_height / 2 + 50,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_hide_view(self):
        self.ui_manager.unregister_handlers()

def main():
    display_width, display_height = arcade.get_display_size()
    window = arcade.Window(display_width, display_height, constants.SCREEN_TITLE, resizable=True)
    start_view = LandingView()
    window.show_view(start_view)
    
    arcade.schedule(SharedData.get_doge_price, 5.0)  # Call every 5 seconds

    
    arcade.run()

if __name__ == "__main__":
    main()

