import arcade
from arcade import View, color, key, SpriteList, PhysicsEnginePlatformer
import random
from settings.constants import ASSETS_PATH, PLAYER_JUMP_SPEED, SPRITE_SCALING_BOX, TILE_SCALING, GRAVITY, PLAYER_MOVEMENT_SPEED
from doge_data_hub.shared_data import SharedData  
from UI.status_bar import StatusBar  
from entities.player_character import PlayerCharacter
from views.confirm_exit_view import ConfirmExitView

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

        self.status_bar.add_menu_option(0, f"Price: {SharedData.doge_price}", self.status_bar.dummy_action, str(ASSETS_PATH / "UI" / "start.png"))
        self.status_bar.add_menu_option(0, "Heal", self.status_bar.dummy_action, str(ASSETS_PATH / "UI" / "start.png"))
        #self.status_bar.add_menu_option(0, "Setup wallet", self.status_bar.dummy_action, str(ASSETS_PATH / "UI" / "wallet.png")) #TODO: fix 3rd item position bug


        self.status_bar.add_menu_option(1, "Mana Potion", self.status_bar.dummy_action, str(ASSETS_PATH / "UI" / "start.png"))
        self.status_bar.add_menu_option(1, "Recharge", self.status_bar.dummy_action, str(ASSETS_PATH / "UI" / "start.png"))        
        self.status_bar.add_menu_option(3, "Recharge", self.status_bar.dummy_action, str(ASSETS_PATH / "UI" / "start.png"))

        self.coin_sound = arcade.load_sound(str(ASSETS_PATH / "sounds" / "collectable.wav"))
        self.jump_sound = arcade.load_sound(str(ASSETS_PATH / "sounds" / "bark.wav"))        
        self.background = arcade.load_texture(str(ASSETS_PATH / "backgrounds" / "hills.png"))
     
        self.player_list = None
        self.wall_list = None
        self.player_sprite = None
        self.physics_engine = None
        
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
    
    def draw_hills(self):
        # Draw the hills
        hill_bottom = 0
        hill_top = self.display_height / 3
        for color in self.hill_colors:
            # Points for the hill polygons
            hill_points = [
                (0, hill_bottom),
                (self.display_width / 4, hill_top),
                (self.display_width / 2, hill_bottom),
                (3 * self.display_width / 4, hill_top),
                (self.display_width, hill_bottom),
                (self.display_width, 0),
                (0, 0)
            ]
            arcade.draw_polygon_filled(hill_points, color)
            # Move the hill range up for the next hill
            hill_bottom += self.display_height / 12
            hill_top += self.display_height / 12

    def draw_clouds(self):
        cloud_color = arcade.color.LIGHT_GRAY
        for cloud in self.clouds:
            # Draw each cloud with 3 ellipses
            for _ in range(3):
                offset_x = random.randrange(-cloud['width'] // 3, cloud['width'] // 3)
                offset_y = random.randrange(-cloud['height'] // 3, cloud['height'] // 3)
                arcade.draw_ellipse_filled(cloud['x'] + offset_x, cloud['y'] + offset_y, cloud['width'], cloud['height'], cloud_color)

    def update_clouds(self, delta_time):
        for cloud in self.clouds:
            # Move the cloud to the right slowly
            cloud['x'] += cloud['speed']
            # If the cloud has moved past the right edge, wrap around to the left
            if cloud['x'] > self.display_width + cloud['width']:
                cloud['x'] = -cloud['width']


    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                self.jump_sound.play()
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
            self.player_sprite.scale_x = -1  # Flip sprite to face left

        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
            self.player_sprite.scale_x = 1   # Flip sprite to face right

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
        
        for x in range(0, 800, 128):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", SPRITE_SCALING_BOX)
            wall.center_x = x
            wall.center_y = 90
            self.wall_list.append(wall)

        coordinate_list = [[200, 300], [300, 300], [400, 400], [500, 400], [600, 400]]

        for coordinate in coordinate_list:
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", TILE_SCALING)
            wall.position = coordinate
            self.wall_list.append(wall)
        
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, gravity_constant=GRAVITY)

    def on_draw(self):
        arcade.start_render()
        self.draw_sky()
        # self.draw_hills()
        # self.draw_clouds()
        # self.update_clouds(1/60)
        #arcade.draw_texture_rectangle(center_x=self.display_width / 2, center_y=self.display_height / 2, width=self.display_width, height=self.display_height, texture=self.background)
        self.status_bar.update_stat_box(0,f"{SharedData.doge_price}")
        self.status_bar.update_menu_item(0,0,f"Doge Price: {SharedData.doge_price}", self.status_bar.dummy_action, str(ASSETS_PATH / "UI" / "wallet.png"))
        self.player_sprite.draw()
        self.wall_list.draw()
        self.player_list.draw()        
        self.status_bar.on_draw()
        
        
    def on_update(self, delta_time):
        if self.physics_engine:
            self.physics_engine.update()
            self.player_sprite.update_animation(delta_time)
            
    def on_mouse_press(self, x, y, button, modifiers):
        # Forward the mouse press event to the status bar
        print("-->", x, y)
        self.status_bar.on_mouse_press(x, y, button, modifiers)
     