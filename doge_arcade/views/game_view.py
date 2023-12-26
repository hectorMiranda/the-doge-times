import arcade
from arcade import View, color, key, SpriteList, PhysicsEnginePlatformer
import random
from settings.config import ASSETS_PATH, PLAYER_JUMP_SPEED, SPRITE_SCALING_BOX, TILE_SCALING, GRAVITY, PLAYER_MOVEMENT_SPEED
from utilities.doge_data_hub_client import DogeDataHub  
from UI.status_bar import StatusBar  
from entities.player_character import PlayerCharacter
from views.confirm_exit_view import ConfirmExitView
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
        self.coin_sound = arcade.load_sound(str(ASSETS_PATH / "sounds" / "collectable.wav"))
        self.jump_sound = arcade.load_sound(str(ASSETS_PATH / "sounds" / "bark.wav"))        
        self.background = arcade.load_texture(str(ASSETS_PATH / "backgrounds" / "hills.png"))
        # self.player_list = None
        # self.wall_list = None
        self.player_sprite = None
        self.physics_engine = None
        self.scene = None
        self.camera = None
        
    def toggle_music(self):
        if self.background_music_player is None:
            # If music is not playing, start playing and store the player object
            self.background_music_player = self.background_music.play(volume=0.3, loop=True)
        else:
            # If music is playing, toggle between pause and resume
            if self.background_music_player.playing:
                self.background_music_player.pause()
            else:
                self.background_music_player.play()
      
    def on_show(self):  
        arcade.set_background_color(arcade.color.CORNFLOWER_BLUE)
        
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
                self.jump_sound.play()
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
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
            pause_view = ConfirmExitView(self.window.current_view)
            self.show_view(pause_view)

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
    
    def setup(self):
        self.camera = arcade.Camera(self.display_width, self.display_height)

        self.scene = arcade.Scene()
        
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)
        
        self.player_sprite = PlayerCharacter()
        self.player_sprite.center_x = 500
        self.player_sprite.center_y = 500
        
        self.scene.add_sprite("Player", self.player_sprite)
        
        for x in range(0, self.display_width, 128):
            wall = arcade.Sprite(str(ASSETS_PATH / "environment" / "grass_3.png"), .2)
            wall.center_x = x
            wall.center_y = 0
            self.scene.add_sprite("Walls", wall)
        
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.scene["Walls"], gravity_constant=GRAVITY)

        
        self.player_sprite.zoom_in() 

    def on_draw(self):
        arcade.start_render()
        self.camera.use()
        #arcade.draw_texture_rectangle(center_x=self.display_width / 2, center_y=self.display_height / 2, width=self.display_width, height=self.display_height, texture=self.background)
        self.status_bar.update_stat_box(0,f"{DogeDataHub.doge_price}")
        self.status_bar.update_menu_item(0,0,f"Doge Price: {DogeDataHub.doge_price}", self.status_bar.dummy_action, str(ASSETS_PATH / "UI" / "wallet.png"))
     
        self.scene.draw()
        self.status_bar.on_draw()


        
        
    def on_update(self, delta_time):
        if self.physics_engine:
             self.physics_engine.update()
             self.player_sprite.update_animation(delta_time)
        
        self.center_camera_to_player()

            
    def on_mouse_press(self, x, y, button, modifiers):
        # Forward the mouse press event to the status bar
        print("-->", x, y)
        self.status_bar.on_mouse_press(x, y, button, modifiers)
        
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
     