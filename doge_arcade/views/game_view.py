import arcade
from arcade import View
import random
from settings.config import ASSETS_PATH, PLAYER_JUMP_SPEED, TILE_SCALING, GRAVITY, PLAYER_MOVEMENT_SPEED, PLAY_MUSIC_ON_START, INITIAL_MUSIC_VOLUME, SOUND_ON, SOUND_ON_VOLUME, LAYER_NAME_PLATFORMS, LAYER_NAME_COINS, LAYER_NAME_DONT_TOUCH, GRID_PIXEL_SIZE, LAYER_NAME_BACKGROUND, LAYER_NAME_LADDERS, PLAYER_START_X, PLAYER_START_Y, LAYER_NAME_MOVING_PLATFORMS
from utilities.doge_data_hub_client import DogeDataHub  
from UI.status_bar import StatusBar  
from entities.player_character import PlayerCharacter
from views.confirm_exit_view import ConfirmExitView
from views.pause_view import PauseView
class GameView(View):
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
        self.reset_score = True
        self.end_of_map = 0
        self.level = 1
        self.display_width, self.display_height = arcade.get_display_size()
        self.sky_color = arcade.color.SKY_BLUE
        self.hill_colors = [arcade.color.GREEN_YELLOW, arcade.color.FOREST_GREEN, arcade.color.DARK_OLIVE_GREEN]
        self.clouds = self.create_clouds(10)        
        self.doge_price = "Loading..."
        self.status_bar = StatusBar(screen_width=self.display_width, bar_height=50)
        self.status_bar.add_stat_box("Doge stats", str(ASSETS_PATH / "UI" / "price.png"))
        self.status_bar.add_stat_box("Settings", str(ASSETS_PATH / "UI" / "settings.png"))
        self.status_bar.add_stat_box("Lives: NA", str(ASSETS_PATH / "UI" / "start.png"))
        self.status_bar.add_stat_box("Coins: NA", str(ASSETS_PATH / "UI" / "coin.png"))
        self.status_bar.add_menu_option(0, f"Price: {DogeDataHub.doge_price}", self.status_bar.dummy_action, str(ASSETS_PATH / "UI" / "start.png"))
        self.status_bar.add_menu_option(0, "Heal", self.status_bar.dummy_action, str(ASSETS_PATH / "UI" / "start.png"))
        #self.status_bar.add_menu_option(0, "Setup wallet", self.status_bar.dummy_action, str(ASSETS_PATH / "UI" / "wallet.png")) #TODO: fix 3rd item position bug
        self.background_music = arcade.load_sound(str(ASSETS_PATH / "sounds" / "main_theme.wav"))
        self.background_music_player = None
        self.status_bar.add_menu_option(1, "sound on", self.toggle_music(), str(ASSETS_PATH / "UI" / "start.png"))
        self.status_bar.add_menu_option(1, "Recharge", self.status_bar.dummy_action, str(ASSETS_PATH / "UI" / "start.png"))        
        self.status_bar.add_menu_option(3, "Recharge", self.status_bar.dummy_action, str(ASSETS_PATH / "UI" / "start.png"))
        self.jump_sound = arcade.load_sound(str(ASSETS_PATH / "sounds" / "bark.wav"))        
        self.background = arcade.load_texture(str(ASSETS_PATH / "backgrounds" / "hills.png"))
        self.game_over = arcade.load_sound(str(ASSETS_PATH / "sounds" / "hurt.wav"))
        self.collect_coin_sound = arcade.load_sound(str(ASSETS_PATH / "sounds" / "collectable.wav"))
        self.player_sprite = None
        self.physics_engine = None
        self.scene = None
        self.camera = None
        self.gui_camera = None
        self.tile_map = None
            
            
        arcade.draw_text("Loading ...", 0, 200 , arcade.color.YELLOW, font_size=50, font_name="Kenney Future", anchor_x="left")



    def setup(self):
        self.camera = arcade.Camera(self.display_width, self.display_height)
        self.gui_camera = arcade.Camera(self.display_width, self.display_height)
          
        map_name = f"{ASSETS_PATH}/maps/map_level_{self.level}.json"
        layer_options = {
        LAYER_NAME_PLATFORMS: {
            "use_spatial_hash": True,
        },
        LAYER_NAME_MOVING_PLATFORMS: {
                "use_spatial_hash": False,
        },
        LAYER_NAME_LADDERS: {
                "use_spatial_hash": True,
        },
        LAYER_NAME_COINS: {
            "use_spatial_hash": True,
        },
        LAYER_NAME_DONT_TOUCH: {
            "use_spatial_hash": True,
        }
        }
       

        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        
        self.player_sprite = PlayerCharacter()
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        
        self.scene.add_sprite_list_after("Player", LAYER_NAME_BACKGROUND)


        self.scene.add_sprite("Player", self.player_sprite)
        
        
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)
        
        if self.level <=2:
            self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.scene[LAYER_NAME_PLATFORMS], gravity_constant=GRAVITY)
        else:
            self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            platforms=self.scene[LAYER_NAME_MOVING_PLATFORMS],
            gravity_constant=GRAVITY,
            ladders=self.scene[LAYER_NAME_LADDERS],
            walls=self.scene[LAYER_NAME_PLATFORMS]
        )
                    
        if self.reset_score:
            self.score = 0
        self.reset_score = True
        
        self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE
        self.player_sprite.isAlive=True

        
    def toggle_music(self):
        if self.background_music_player is None:
            self.background_music_player = self.background_music.play(volume=INITIAL_MUSIC_VOLUME, loop=True)
            if PLAY_MUSIC_ON_START == False:
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
        trees_texture = arcade.load_texture(str(ASSETS_PATH / "environment" / "group_of_trees.png"))
        center_y = hill_bottom + hill_height / 2
        arcade.draw_texture_rectangle(center_x=self.display_width / 2, center_y=center_y, width=self.display_width, height=hill_height, texture=trees_texture)
        
    def draw_house(self):
        house_bottom = 0
        house_height = self.display_height /1
        house_texture = arcade.load_texture(str(ASSETS_PATH / "environment" / "doge_house.png"))
        center_y = house_bottom + house_height / 2
        arcade.draw_texture_rectangle(center_x=self.display_width / 2, 
                                    center_y=center_y, 
                                    width=self.display_width, 
                                    height=house_height, 
                                    texture=house_texture)
        
    def draw_tree(self):
        tree_bottom = 200
        tree_height = 600
        tree_texture = arcade.load_texture(str(ASSETS_PATH / "environment" / "tree_0.png"))
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
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                self.jump_sound.play(volume=0.2)
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
            self.player_sprite.isAlive = True
        elif key == arcade.key.Z:
            self.player_sprite.zoom_in()
        elif key == arcade.key.X:
            self.player_sprite.zoom_out()
        elif key == arcade.key.R:
            self.background_music_player.pause()
            self.restart_game()
        elif key == arcade.key.M:
            self.toggle_music()
        elif key == arcade.key.T:
            self.player_sprite.isAlive = False            
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

    def on_update(self, delta_time): 
        self.physics_engine.update()
        
    def restart_game(self):
        from .loading_view import LoadingView
        self.window.show_view(LoadingView())

    def on_draw(self):
        arcade.start_render()
        self.camera.use()
        #arcade.draw_texture_rectangle(center_x=self.display_width / 2, center_y=self.display_height / 2, width=self.display_width, height=self.display_height, texture=self.background)
        self.status_bar.update_stat_box(0,f"{DogeDataHub.doge_price}")
        self.status_bar.update_stat_box(1,f"Level {self.level}")
        self.status_bar.update_stat_box(3,f"{self.score}")
        self.status_bar.update_menu_item(0,0,f"Doge Price: {DogeDataHub.doge_price}", self.status_bar.dummy_action, str(ASSETS_PATH / "UI" / "wallet.png"))
        self.scene.draw()
        self.gui_camera.use()
        self.status_bar.draw()

        
    def on_update(self, delta_time):
        if self.physics_engine:
             self.physics_engine.update()
             self.player_sprite.update_animation(delta_time)
             
        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene[LAYER_NAME_COINS]
        )

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
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y

            arcade.play_sound(self.game_over)
            self.player_sprite.isAlive = False

        # Did the player touch something they should not?
        if self.level <=2:
            if arcade.check_for_collision_with_list(self.player_sprite, self.scene[LAYER_NAME_DONT_TOUCH]):
                self.player_sprite.change_x = 0
                self.player_sprite.change_y = 0
                self.player_sprite.center_x = PLAYER_START_X
                self.player_sprite.center_y = PLAYER_START_Y

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
        print("-->", x, y)
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
     