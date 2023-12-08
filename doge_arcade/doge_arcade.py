import arcade

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Doge 2D Platformer"

# Player constants
PLAYER_SCALING = 0.5
GRAVITY = 1
PLAYER_MOVEMENT_SPEED = 5
PLAYER_JUMP_SPEED = 20

# Sprite constants - adjust the numbers based on your sprite sheet
SPRITE_NATIVE_SIZE = 128
SPRITE_SCALING = 0.5
SPRITE_SIZE_WIDTH = 128 #int(SPRITE_NATIVE_SIZE * SPRITE_SCALING)
SPRITE_SIZE_HEIGHT = 126 #int(SPRITE_NATIVE_SIZE * SPRITE_SCALING)


# Assuming the idle and run sprites are on a grid in the image file,
# provide the correct rows and columns
SPRITE_IDLE_FRAMES = 2
SPRITE_RUN_FRAMES = 8

# Constants to determine sprite facing direction
LEFT_FACING = 0
RIGHT_FACING = 1


class PlayerCharacter(arcade.Sprite):
    def __init__(self):
        # Set up parent class
        super().__init__()

        # Load textures for idle
        self.idle_textures = []
        for i in range(SPRITE_IDLE_FRAMES):
            texture = arcade.load_texture("../artwork/sprites//PlayerIdle.png", x=i*SPRITE_SIZE_WIDTH, y=0, width=SPRITE_SIZE_WIDTH, height=SPRITE_SIZE_HEIGHT)
            self.idle_textures.append(texture)

        # Load textures for running
        self.run_textures = []
        for i in range(SPRITE_RUN_FRAMES):
            self.run_textures.append(texture)

        # By default, face right
        self.character_face_direction = 1 #arcade.Sprite.RIGHT_FACING

        # Set the initial texture
        self.texture = self.idle_textures[0]

        # Track our state
        self.jumping = False
        self.is_running = False
        self.cur_texture = 0

    def update_animation(self, delta_time: float = 1/60):
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
            self.texture = self.run_textures[self.cur_texture // 3]


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

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
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.player_list.append(self.player_sprite)

        # Create the ground
        # This should be replaced with your own logic to place platforms
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE_WIDTH):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", SPRITE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        # Set up the physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list,
                                                             gravity_constant=GRAVITY)

    def on_draw(self):
        arcade.start_render()
        self.wall_list.draw()
        self.player_list.draw()

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
