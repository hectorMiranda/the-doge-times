import time
import math
import random
import arcade
from arcade import View, color, key
from settings.constants import ASSETS_PATH 
from views.confirm_exit_view import ConfirmExitView
 
              
class LandingView(arcade.View):
    def __init__(self):
        super().__init__()
        self.loading_bar_width = 0
        self.total_loading_time = 1 
        self.start_time = time.time()
        self.loading_complete = False
        self.text_visible = True
        self.blink_timer = 0  
        self.display_width, self.display_height = arcade.get_display_size()
        self.cube_rotation_x = 0
        self.cube_rotation_y = 0
        self.cube_rotation_z = 0
        self.rotation_speed_x = random.uniform(-0.02, 0.02)
        self.rotation_speed_y = random.uniform(-0.02, 0.02)
        self.rotation_speed_z = random.uniform(-0.02, 0.02)

        
    def on_show(self):
        arcade.set_background_color(arcade.color.CORNFLOWER_BLUE)

    def on_draw(self):
        arcade.start_render()
        
        arcade.draw_text("Journey to the moon!", self.display_width / 2, self.display_height / 2, arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("python arcade edition!", self.display_width / 2 + 250, self.display_height / 2 -45, arcade.color.ORANGE, font_size=20, anchor_x="center")                         
        
        progress_bar_x = self.display_width / 2
        progress_bar_y = self.display_height / 3
        arcade.draw_texture_rectangle(self.display_width / 5, self.display_height / 2, 400, 400, arcade.load_texture(str(ASSETS_PATH / "UI" / "doge_mining.png")))
       
        if self.loading_complete:  
            self.draw_rotating_cube()
            if self.text_visible:
                message = arcade.draw_text("Press any key to continue", progress_bar_x, progress_bar_y - 10 , arcade.color.BLUE, font_size=20, font_name="Kenney Future", anchor_x="center")
        elif not self.loading_complete:
            arcade.draw_rectangle_filled(progress_bar_x, progress_bar_y, self.loading_bar_width, 30, arcade.color.BLUE)
            message = arcade.draw_text("Loading ...", progress_bar_x, progress_bar_y - 10 , arcade.color.WHITE, font_size=20, font_name="Kenney Future", anchor_x="center")
    def draw_rotating_cube(self):
        # Cube vertices
        size = 50
        vertices = [
            [-size, -size, -size],
            [size, -size, -size],
            [size, size, -size],
            [-size, size, -size],
            [-size, -size, size],
            [size, -size, size],
            [size, size, size],
            [-size, size, size]
        ]

        # Cube faces (each face is a quadrilateral)
        faces = [
            (0, 1, 2, 3),  # Front face
            (4, 5, 6, 7),  # Back face
            (0, 1, 5, 4),  # Bottom face
            (3, 2, 6, 7),  # Top face
            (0, 3, 7, 4),  # Left face
            (1, 2, 6, 5)   # Right face
        ]

        # Grayscale colors for each face
        grayscale_colors = [
            (50, 50, 50),  # Darker gray
            (100, 100, 100),
            (150, 150, 150),
            (200, 200, 200),
            (225, 225, 225),  # Lighter gray
            (255, 255, 255)   # White
        ]

        # Apply rotation
        rotated_vertices = []
        for vertex in vertices:
            x, y, z = self.rotate_vertex(vertex)
            rotated_vertices.append((x, y, z))

        # Draw each face with a different grayscale color
        for face, color in zip(faces, grayscale_colors):
            face_vertices = [rotated_vertices[index] for index in face]
            screen_face_vertices = [(vertex[0] + self.display_width // 2, vertex[1] + self.display_height // 2 - 100) for vertex in face_vertices]
            arcade.draw_polygon_filled(screen_face_vertices, color)

        # Update rotation
        self.update_rotation()

    def rotate_vertex(self, vertex):
        x, y, z = vertex
        # Rotation around X-axis
        temp_y = y * math.cos(self.cube_rotation_x) - z * math.sin(self.cube_rotation_x)
        temp_z = y * math.sin(self.cube_rotation_x) + z * math.cos(self.cube_rotation_x)
        y, z = temp_y, temp_z
        # Rotation around Y-axis
        temp_x = x * math.cos(self.cube_rotation_y) - z * math.sin(self.cube_rotation_y)
        temp_z = x * math.sin(self.cube_rotation_y) + z * math.cos(self.cube_rotation_y)
        x, z = temp_x, temp_z
        # Rotation around Z-axis
        temp_x = x * math.cos(self.cube_rotation_z) - y * math.sin(self.cube_rotation_z)
        temp_y = x * math.sin(self.cube_rotation_z) + y * math.cos(self.cube_rotation_z)
        x, y = temp_x, temp_y
        return x, y, z

    def update_rotation(self):
        self.cube_rotation_x += self.rotation_speed_x
        self.cube_rotation_y += self.rotation_speed_y
        self.cube_rotation_z += self.rotation_speed_z

   
    def on_update(self, delta_time):

        if not self.loading_complete:
            elapsed_time = time.time() - self.start_time
            self.loading_bar_width = (elapsed_time / self.total_loading_time) * self.display_width
            
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
            from .game_view import GameView
            game = GameView()
            game.setup()
            self.window.show_view(game)
   