import arcade

# Constants for the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Doge 2D Platformer"
PLAYER_SCALING = 1
GRAVITY = 1
PLAYER_MOVEMENT_SPEED = 5
PLAYER_JUMP_SPEED = 14

# Path to the player's texture files
PLAYER_IDLE_TEXTURE = '../artwork/sprites/PlayerIdle.png'
PLAYER_RUN_TEXTURE = '../artwork/sprites/PlayerRun.png'

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()

        # Load textures for idle standing
        self.idle_texture = arcade.load_texture(PLAYER_IDLE_TEXTURE)
        self.texture = self.idle_texture

        # Load textures for running
        self.run_textures = [arcade.load_texture(PLAYER_RUN_TEXTURE, x=i*32, y=0, width=32, height=32) for i in range(8)]

        # Track our state
        self.cur_texture = 0
        self.scale = PLAYER_SCALING

    def update_animation(self, delta_time: float = 1/60):
        # Running animation
        if self.change_x != 0:
            self.cur_texture += 1
            if self.cur_texture >= 8:
                self.cur_texture = 0
            self.texture = self.run_textures[self.cur_texture]
        else:
            self.texture = self.idle_texture

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.player_sprite = None
        self.physics_engine = None

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        self.player_sprite = Player()
        self.player_sprite.center_x = SCREEN_WIDTH // 2
        self.player_sprite.center_y = 128

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, platforms=None, gravity_constant=GRAVITY)

    def on_draw(self):
        arcade.start_render()
        self.player_sprite.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        self.physics_engine.update()
        self.player_sprite.update_animation(delta_time)

def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
