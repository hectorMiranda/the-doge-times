import arcade
import pyglet
from pyglet.gl import *
import random
import math

class MyGameView(arcade.View):
    def __init__(self):
        super().__init__()

        # Load a built-in Arcade texture
        self.texture = arcade.load_texture(":resources:images/tiles/brickTextureWhite.png")
        
        # OpenGL setup for 3D rendering
        glEnable(GL_DEPTH_TEST)  # Enable depth testing for 3D
     
        # Use the texture_id for OpenGL context
        self.texture_id = self.texture.texture_id
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        
        # Rotation speeds
        self.rotation_speed_x = random.uniform(-0.5, 0.5)
        self.rotation_speed_y = random.uniform(-0.5, 0.5)
        self.rotation_speed_z = random.uniform(-0.5, 0.5)

        # Initial rotation
        self.rotation_x = 0
        self.rotation_y = 0
        self.rotation_z = 0

    def on_draw(self):
        self.clear()
        self.draw_3d_cube()

    def draw_3d_cube(self):
        # Set up 3D projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, self.window.width / self.window.height, 0.1, 100)

        # Set up 3D view (modelview matrix)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0, 0, -5)
        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)
        glRotatef(self.rotation_z, 0, 0, 1)

        # Bind the texture
        glBindTexture(GL_TEXTURE_2D, self.texture_id)


        # Draw the cube with each face
        glBegin(GL_QUADS)
        # Front face
        glTexCoord2f(0, 0); glVertex3f(-1, -1, 1)
        glTexCoord2f(1, 0); glVertex3f(1, -1, 1)
        glTexCoord2f(1, 1); glVertex3f(1, 1, 1)
        glTexCoord2f(0, 1); glVertex3f(-1, 1, 1)
        # Other faces omitted for brevity...
        glEnd()

        # Update rotation
        self.rotation_x += self.rotation_speed_x
        self.rotation_y += self.rotation_speed_y
        self.rotation_z += self.rotation_speed_z

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(640, 480, "Arcade Window with 3D Cube")
        game_view = MyGameView()
        self.show_view(game_view)

def main():
    window = MyGame()
    arcade.run()

if __name__ == "__main__":
    main()
