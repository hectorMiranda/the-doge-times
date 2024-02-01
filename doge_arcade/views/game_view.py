import arcade
import random
import settings.config as cfg
from utilities.doge_data_hub_client import DogeDataHub  
from UI.status_bar import StatusBar  
from entities.player_character import PlayerCharacter
from views.confirm_exit_view import ConfirmExitView
from views.pause_view import PauseView
from views.base_view import BaseView
from utilities.doge_logger import DogeLogger
class GameView(BaseView):
    def __init__(self):
        super().__init__()
        self.logger = DogeLogger.get_instance()
        self.elapsed_time = 0.0
        self.time_display = "00:00"
        self.start_timer = False
        self.score = 0
        self.lives = 99
        self.coins = None
        self.background = None
        self.walls = None
        self.ladders = None
        self.goals = None
        self.enemies = None
        self.reset_score = True
        self.end_of_map = 0
        self.level = 0
        self.display_width, self.display_height = arcade.get_display_size()
        self.sky_color = arcade.color.SKY_BLUE
        self.hill_colors = [arcade.color.GREEN_YELLOW, arcade.color.FOREST_GREEN, arcade.color.DARK_OLIVE_GREEN]
        self.clouds = self.create_clouds(10)        
        self.doge_price = "Loading..."
        self.create_status_bar()
        self.setup_game_controller()
        self.game_over = arcade.load_sound(str(cfg.ASSETS_PATH / "sounds" / "hurt.wav"))
        self.collect_coin_sound = arcade.load_sound(str(cfg.ASSETS_PATH / "sounds" / "collectable.wav"))
        self.jump_sound = arcade.load_sound(str(cfg.ASSETS_PATH / "sounds" / "bark.wav"))
        self.background_music = arcade.load_sound(str(cfg.ASSETS_PATH / "sounds" / "main_theme.wav"))
        self.background_music_player = None
        self.IsPlayerBig = False
        self.player_sprite = None
        self.physics_engine = None
        self.scene = None
        self.camera = None
        self.gui_camera = None
        self.tile_map = None
        self.confetti_list = []
        self.raindrop_list = []
        self.Winner = False
        self.IsRaining = False



    def setup_game_controller(self):
        # Check for game controllers and set up the first one found
        joysticks = arcade.get_joysticks()
        if joysticks:
            self.game_controller = joysticks[0]
            self.logger.debug(self.game_controller.device.name)
            self.game_controller.open()
            self.game_controller.push_handlers(
                self.on_joybutton_press,
                self.on_joybutton_release,
                self.on_joyhat_motion,
                self.on_joyaxis_motion
            )

    def on_joybutton_press(self, joystick, button):
        if button == cfg.BUTTON_X:
            self.on_key_press(arcade.key.UP, 0)
    def on_joybutton_release(self, joystick, button):
        if button == cfg.BUTTON_X:
            self.on_key_release(arcade.key.UP, 0)

    def on_joyhat_motion(self, joystick, hat_x, hat_y):
        # Check for D-pad Up
        if hat_y == 1:
            self.on_key_press(arcade.key.UP, 0)
        elif hat_y == -1:
            self.on_key_press(arcade.key.DOWN, 0)

        # Check for D-pad Left/Right
        if hat_x == -1:
            self.on_key_press(arcade.key.LEFT, 0)
        elif hat_x == 1:
            self.on_key_press(arcade.key.RIGHT, 0)

        # Reset when D-pad is in the center position
        if hat_x == 0:
            self.on_key_release(arcade.key.LEFT, 0)
            self.on_key_release(arcade.key.RIGHT, 0)
        if hat_y == 0:
            self.on_key_release(arcade.key.UP, 0)
            self.on_key_release(arcade.key.DOWN, 0)


    def on_joyaxis_motion(self, joystick, axis, value):
        DEADZONE = 0.1  # Adjust this value as needed

        if axis == 'x':  # Left-right movement
            if value < -DEADZONE:
                self.on_key_press(arcade.key.LEFT, 0)
            elif value > DEADZONE:
                self.on_key_press(arcade.key.RIGHT, 0)
            else:
                # Release both keys when in the deadzone
                self.on_key_release(arcade.key.LEFT, 0)
                self.on_key_release(arcade.key.RIGHT, 0)

        elif axis == 'y':  # Up-down movement
            if value < -DEADZONE:
                self.on_key_press(arcade.key.UP, 0)  # Assuming UP is for climbing up
            elif value > DEADZONE:
                self.on_key_press(arcade.key.DOWN, 0)  # Assuming DOWN is for climbing down
            else:
                self.on_key_release(arcade.key.UP, 0)
                self.on_key_release(arcade.key.DOWN, 0)
        
        
    def create_status_bar(self):
        self.status_bar = StatusBar(screen_width=self.display_width, bar_height=50)
        
        # Adding status box items
        status_box_items = [
            ("Doge stats", "price.png"),
            ("Settings", "settings.png"),
            (f"Time: {self.time_display}", "start.png"),
            ("Coins: NA", "coin.png"),
        ]

        for label, icon in status_box_items:
            self.add_status_box_item(label, icon)

        # Adding menu options
        menu_options = [
            (0, f"Price: {DogeDataHub.doge_price}", self.status_bar.dummy_action, "start.png"),
            (0, "Heal", self.status_bar.dummy_action, "start.png"),
            # Uncomment the next line when the bug is fixed
            # (0, "Setup wallet", self.status_bar.dummy_action, "wallet.png"),
            (1, "sound on", self.toggle_music, "start.png"),
            (1, "Recharge", self.status_bar.dummy_action, "start.png"),
            (3, "Recharge", self.status_bar.dummy_action, "start.png")
        ]

        for group, label, action, icon in menu_options:
            self.add_menu_option(group, label, action, icon)

    def add_status_box_item(self, label, icon_name):
        icon_path = str(cfg.ASSETS_PATH / "UI" / icon_name)
        self.status_bar.add_stat_box(label, icon_path)

    def add_menu_option(self, group, label, action, icon_name):
        icon_path = str(cfg.ASSETS_PATH / "UI" / icon_name)
        self.status_bar.add_menu_option(group, label, action, icon_path)
        arcade.draw_text("Loading ...", 0, 200 , arcade.color.YELLOW, font_size=50, font_name="Kenney Future", anchor_x="left")



    def setup(self):
        self.camera = arcade.Camera(self.display_width, self.display_height)
        self.gui_camera = arcade.Camera(self.display_width, self.display_height)
        
        if cfg.LOAD_VERTICAL_MAPS == True:  
            map_name = f"{cfg.ASSETS_PATH}/maps/map_level_{self.level}_vertical.json"
        else:
            map_name = f"{cfg.ASSETS_PATH}/maps/map_level_{self.level}.json"
        
        layer_options = {
        cfg.LAYER_NAME_PLATFORMS: {
            "use_spatial_hash": True,
        },
        cfg.LAYER_NAME_MOVING_PLATFORMS: {
                "use_spatial_hash": False,
        },
        cfg.LAYER_NAME_LADDERS: {
                "use_spatial_hash": True,
        },
        cfg.LAYER_NAME_COINS: {
            "use_spatial_hash": True,
        },
        cfg.LAYER_NAME_DONT_TOUCH: {
            "use_spatial_hash": True,
        }
        }
       
        try:
            self.tile_map = arcade.load_tilemap(map_name, cfg.TILE_SCALING, layer_options)
        except Exception as e:
            self.logger.error(f"Error loading tile map: {e}")
    
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        
        self.player_sprite = PlayerCharacter()
        self.player_sprite.center_x = cfg.PLAYER_START_X
        self.player_sprite.center_y = cfg.PLAYER_START_Y
        
        self.scene.add_sprite_list_after("Player", cfg.LAYER_NAME_BACKGROUND)


        self.scene.add_sprite("Player", self.player_sprite)
        
        
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)
        
        self.physics_engine = arcade.PhysicsEnginePlatformer(
        self.player_sprite,
        platforms=self.scene[cfg.LAYER_NAME_MOVING_PLATFORMS],
        gravity_constant=cfg.GRAVITY,
        ladders=self.scene[cfg.LAYER_NAME_LADDERS],
        walls=self.scene[cfg.LAYER_NAME_PLATFORMS]
        )
                    
        if self.reset_score:
            self.score = 0
        self.reset_score = True
        
        self.end_of_map = self.tile_map.width * cfg.GRID_PIXEL_SIZE
        self.player_sprite.isAlive=True
        
        


        
    def toggle_music(self):
        if self.background_music_player is None:
            self.background_music_player = self.background_music.play(volume=cfg.INITIAL_MUSIC_VOLUME, loop=True)
            if cfg.PLAY_MUSIC_ON_START == False:
                self.background_music_player.pause()
        else:
            if self.background_music_player.playing:
                self.background_music_player.pause()
            else:
                self.background_music_player.play()
      
        
    def create_clouds(self, num_clouds=5):
        clouds = []
        for _ in range(num_clouds):  
            cloud_width = random.randrange(100, 200)
            cloud_height = random.randrange(50, 100)
            x = random.randrange(0, self.display_width)
            y = random.randrange(int(self.display_height / 2), self.display_height)
            speed = random.random() * 0.5  # Cloud speed (0.0 - 0.5)
            clouds.append({'x': x, 'y': y, 'width': cloud_width, 'height': cloud_height, 'speed': speed})
        return clouds    
        
    def draw_sky(self):
        arcade.draw_lrtb_rectangle_filled(0, self.display_width, self.display_height, self.display_height / 2, self.sky_color)
    
    def draw_trees(self):
        hill_bottom = 0
        hill_height = self.display_height /1.5
        trees_texture = arcade.load_texture(str(cfg.ASSETS_PATH / "environment" / "group_of_trees.png"))
        center_y = hill_bottom + hill_height / 2
        arcade.draw_texture_rectangle(center_x=self.display_width / 2, center_y=center_y, width=self.display_width, height=hill_height, texture=trees_texture)
        
    def draw_house(self):
        house_bottom = 0
        house_height = self.display_height /1
        house_texture = arcade.load_texture(str(cfg.ASSETS_PATH / "environment" / "doge_house.png"))
        center_y = house_bottom + house_height / 2
        arcade.draw_texture_rectangle(center_x=self.display_width / 2, 
                                    center_y=center_y, 
                                    width=self.display_width, 
                                    height=house_height, 
                                    texture=house_texture)
        
    def draw_tree(self):
        tree_bottom = 200
        tree_height = 600
        tree_texture = arcade.load_texture(str(cfg.ASSETS_PATH / "environment" / "tree_0.png"))
        center_y = tree_bottom + tree_height / 2
        arcade.draw_texture_rectangle(center_x=350, center_y=500, width=600, height=tree_height, texture=tree_texture)


    def draw_clouds(self):
        cloud_color = arcade.color.LIGHT_GRAY
        for cloud in self.clouds:
            for _ in range(3):
                offset_x = random.randrange(-cloud['width'] // 3, cloud['width'] // 3)
                offset_y = random.randrange(-cloud['height'] // 3, cloud['height'] // 3)
                arcade.draw_ellipse_filled(cloud['x'] + offset_x, cloud['y'] + offset_y, cloud['width'], cloud['height'], cloud_color)

    def update_clouds(self, delta_time):
        for cloud in self.clouds:
            cloud['x'] += cloud['speed']
            # If the cloud has moved past the right edge, wrap around to the left
            if cloud['x'] > self.display_width + cloud['width']:
                cloud['x'] = -cloud['width']


    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = cfg.PLAYER_REGULAR_JUMP_SPEED
                self.jump_sound.play(volume=0.2)
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -cfg.PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -cfg.PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = cfg.PLAYER_MOVEMENT_SPEED
            self.player_sprite.isAlive = True
            self.start_timer = True
        elif key == arcade.key.Z:
            if self.IsPlayerBig == False:
                self.IsPlayerBig = True
                self.player_sprite.zoom_in()
            self.player_sprite.zoom_in()
        elif key == arcade.key.X:
            self.player_sprite.zoom_out()
        elif key == arcade.key.R:
            if self.background_music_player is not None:
                self.background_music_player.pause()
            self.restart_game()
        elif key == arcade.key.M:
            self.toggle_music()
        elif key == arcade.key.L:
            if self.IsRaining == False:
                self.IsRaining = True
            else:  
                self.IsRaining = False
            self.logger.debug(self.IsRaining)
        elif key == arcade.key.T:
            self.player_sprite.isAlive = False
        elif key == arcade.key.C:
            if self.Winner == False:
                self.Winner = True
            else:
                self.Winner = False           
        elif key == arcade.key.ESCAPE:
            modal_view = ConfirmExitView(self)  
            self.window.show_view(modal_view)
        elif key == arcade.key.P:
            pause_view = PauseView()
            self.window.show_view(pause_view)
    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

        
    def restart_game(self):
        from .start_view import StartView
        self.window.show_view(StartView())

    def on_draw(self):
        arcade.start_render()
   
        minutes = int(self.elapsed_time) // 60
        seconds = int(self.elapsed_time) % 60
        self.time_display = f"{minutes:02d}:{seconds:02d}"
             

        self.camera.use()
        #arcade.draw_texture_rectangle(center_x=self.display_width / 2, center_y=self.display_height / 2, width=self.display_width, height=self.display_height, texture=self.background)
        self.status_bar.update_stat_box(0,f"{DogeDataHub.doge_price}")
        self.status_bar.update_stat_box(1,f"Level {self.level}")
        self.status_bar.update_stat_box(2,f"Time: {self.time_display}")
        self.status_bar.update_stat_box(3,f"{self.score}")
        self.status_bar.update_menu_item(0,0,f"Doge Price: {DogeDataHub.doge_price}", self.status_bar.dummy_action, str(cfg.ASSETS_PATH / "UI" / "wallet.png"))

        
        self.scene.draw()
        self.gui_camera.use()
        self.status_bar.draw()

        
        
        if self.Winner == True:
            self.confetti_list = []
            for i in range(cfg.CONFETTI_COUNT):
                x = random.randint(0, self.display_width)
                y = random.randint(0, self.display_height)
                color = random.choice(cfg.COLORS)
                self.confetti_list.append({"x": x, "y": y, "color": color})
            for confetti in self.confetti_list:
                arcade.draw_rectangle_filled(confetti["x"], confetti["y"], 10, 5, confetti["color"])
        
        if self.IsRaining == True:        
            self.raindrop_list = []
            for i in range(cfg.RAINDROP_COUNT):
                x = random.randint(0, self.display_width)
                y = random.randint(0, self.display_height)
                length = random.randint(10, 20)
                color = arcade.color.BLUE_GRAY  
                self.raindrop_list.append({"x": x, "y": y, "length": length, "color": color})
            for raindrop in self.raindrop_list:
                arcade.draw_line(raindrop["x"], raindrop["y"], 
                                raindrop["x"], raindrop["y"] + raindrop["length"], 
                                raindrop["color"], 2)
                    



        
    def on_update(self, delta_time):
        if self.start_timer:
            self.elapsed_time += delta_time

        if self.physics_engine:
             self.physics_engine.update()
             self.player_sprite.update_animation(delta_time)
             
        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene[cfg.LAYER_NAME_COINS]
        )
        if self.IsRaining == True:
            for raindrop in self.raindrop_list:
                raindrop["y"] -= 4  # Adjust the speed of the rain
                if raindrop["y"] < -20:  # Reset raindrop to the top once it falls out of the window
                    raindrop["y"] = self.display_width + 20


        # Loop through each coin we hit (if any) and remove it
        for coin in coin_hit_list:
            # Remove the coin
            coin.remove_from_sprite_lists()
            # Play a sound
            arcade.play_sound(self.collect_coin_sound)
            # Add one to the score
            self.score += 1
        
        self.center_camera_to_player()
        
               # Did the player fall off the map?
        if self.player_sprite.center_y < -100:
            self.player_sprite.center_x = cfg.PLAYER_START_X
            self.player_sprite.center_y = cfg.PLAYER_START_Y

            arcade.play_sound(self.game_over)
            self.player_sprite.isAlive = False

        # Did the player touch something they should not?
        if self.level <=2:
            if arcade.check_for_collision_with_list(self.player_sprite, self.scene[cfg.LAYER_NAME_DONT_TOUCH]):
                self.player_sprite.change_x = 0
                self.player_sprite.change_y = 0
                self.player_sprite.center_x = cfg.PLAYER_START_X
                self.player_sprite.center_y = cfg.PLAYER_START_Y

                arcade.play_sound(self.game_over)
                self.player_sprite.isAlive = False

        # See if the user got to the end of the level
        if self.player_sprite.center_x >= self.end_of_map:
            # Advance to the next level
            self.level += 1

            # Make sure to keep the score from this level when setting up the next level
            self.reset_score = False

            # Load the next level
            self.setup()

            
    def on_mouse_press(self, x, y, button, modifiers):
        self.logger.debug("--> {}, {}".format(x, y))
        self.status_bar.on_mouse_press(x, y, button, modifiers)
        self.player_sprite.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        self.player_sprite.on_mouse_release(x, y, button, modifiers)
        
    def on_mouse_motion(self, x, y, dx, dy):
        self.player_sprite.on_mouse_motion(x, y, dx, dy)

        
    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )

        # Don't let camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)
     