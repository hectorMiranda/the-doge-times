import arcade
import pathlib
import constants
import random
import time

display_width, display_height = arcade.get_display_size()
SCREEN_WIDTH = int(display_width * 0.8)
SCREEN_HEIGHT = int(display_height * 0.8)
ASSETS_PATH = pathlib.Path(__file__).resolve().parent.parent / "assets"

class LandingView(arcade.View):
    
    def __init__(self):
        super().__init__()
        self.loading_bar_width = 0
        self.total_loading_time = 4 
        self.start_time = time.time()
        self.loading_complete = False
        self.text_visible = True
        self.blink_timer = 0  
        
    def on_show(self):
        arcade.set_background_color(arcade.color.CORNFLOWER_BLUE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Journey to the moon!", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("python arcade edition!", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 -35, arcade.color.ORANGE, font_size=20, anchor_x="center")                         
        
        progress_bar_x = SCREEN_WIDTH / 2
        progress_bar_y = SCREEN_HEIGHT / 3
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 5, SCREEN_HEIGHT / 2, 400, 400, arcade.load_texture(str(ASSETS_PATH / "UI" / "doge_mining.png")))
        arcade.draw_rectangle_filled(progress_bar_x, progress_bar_y, self.loading_bar_width, 30, arcade.color.BLUE)
 
        if self.loading_complete and self.text_visible:
            message = arcade.draw_text("Press any key to continue", progress_bar_x, progress_bar_y - 10 , arcade.color.WHITE, font_size=20, font_name="Kenney Future", anchor_x="center")
        elif not self.loading_complete:
            message = arcade.draw_text("Loading ...", progress_bar_x, progress_bar_y - 10 , arcade.color.WHITE, font_size=20, font_name="Kenney Future", anchor_x="center")
   
    def on_update(self, delta_time):
        # Update loading bar width
        if not self.loading_complete:
            elapsed_time = time.time() - self.start_time
            self.loading_bar_width = (elapsed_time / self.total_loading_time) * SCREEN_WIDTH

            if elapsed_time >= self.total_loading_time:
                self.loading_complete = True

        # Blinking effect for "Press any key" text
        if self.loading_complete:
            self.blink_timer += delta_time
            if self.blink_timer > 0.5:  # Toggle visibility every 0.5 seconds
                self.text_visible = not self.text_visible
                self.blink_timer = 0

    def on_key_press(self, key, modifiers):
        if self.loading_complete:
            self.window.show_view(GameView())
            
            
class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.lives = 3
        self.player_sprite = PlayerCharacter()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player_sprite.change_x = -constants.PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = constants.PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        self.player_sprite.update()
        self.player_sprite.update_animation(delta_time)

    def on_draw(self):
        arcade.start_render()
        self.player_sprite.draw()
        arcade.draw_text(f"Score: {self.score}", 10, SCREEN_HEIGHT - 20, arcade.color.WHITE, 14)
        arcade.draw_text(f"Lives: {self.lives}", SCREEN_WIDTH - 80, SCREEN_HEIGHT - 20, arcade.color.WHITE, 14)

class PlayerCharacter(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.facing_direction = constants.RIGHT_FACING


        self.position = (100,50)

        self.idle_textures = []
        for i in range(constants.SPRITE_IDLE_FRAMES):
            idle_texture = arcade.load_texture(str(ASSETS_PATH / "sprites" / "PlayerIdle.png"), x=i*constants.SPRITE_SIZE_WIDTH, y=0, width=constants.SPRITE_SIZE_WIDTH, height=constants.SPRITE_SIZE_HEIGHT)
            self.idle_textures.append(idle_texture)

        self.run_textures = []
        for i in range(constants.SPRITE_RUN_FRAMES):
            run_texture = arcade.load_texture(str(ASSETS_PATH / "sprites" / "PlayerRun.png"), x=i*constants.SPRITE_SIZE_WIDTH, y=0, width=constants.SPRITE_SIZE_WIDTH, height=constants.SPRITE_SIZE_HEIGHT)
            self.run_textures.append(run_texture)

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


class JourneyToTheMoon(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, resizable=True)

        self.coins = None
        self.background = None
        self.walls = None
        self.ladders = None
        self.goals = None
        self.enemies = None
        self.score = 0
        self.level = 1

        self.coin_sound = arcade.load_sound(
            str(ASSETS_PATH / "sounds" / "collectable.wav")
        )
        self.jump_sound = arcade.load_sound(
            str(ASSETS_PATH / "sounds" / "bark.wav")
        )
        

        # Sprite lists
        self.player_list = None
        self.wall_list = None

        # Set up the player
        self.player_sprite = None

        # Physics engine
        self.physics_engine = None



    def setup(self):
        # Set up the game
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)

        # Set up the player
        self.player_sprite = PlayerCharacter()
        self.player_sprite.center_x = 128
        self.player_sprite.center_y = 126
        self.player_list.append(self.player_sprite)

        for x in range(0, SCREEN_WIDTH, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", SPRITE_SCALING_BOX)
            wall.center_x = x
            wall.center_y = 350
            self.wall_list.append(wall)

        coordinate_list = [[512, 96], [256, 96], [768, 96]]

        for coordinate in coordinate_list:
            # Add a crate on the ground
            wall = arcade.Sprite(
                ":resources:images/tiles/boxCrate_double.png", TILE_SCALING
            )
            wall.position = coordinate
            self.wall_list.append(wall)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list,
                                                             gravity_constant=GRAVITY)

    def on_draw(self):
        arcade.clear()
        self.wall_list.draw()
        self.player_list.draw()


    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = constants.PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -constants.PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = constants.PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.Z:
            self.player.zoom_in()
        elif key == arcade.key.X:
            self.player.zoom_out()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        self.physics_engine.update()
        self.player_sprite.update_animation(delta_time)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, constants.SCREEN_TITLE)
    start_view = LandingView()
    window.show_view(start_view)
    arcade.run()

if __name__ == "__main__":
    main()

