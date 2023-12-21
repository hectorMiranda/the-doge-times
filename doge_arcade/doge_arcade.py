import requests
import arcade
import arcade.gui
import pathlib
import constants
import random
import time
import math


ASSETS_PATH = pathlib.Path(__file__).resolve().parent.parent / "assets"            
class StatusBar:
    def __init__(self, screen_width, bar_height=50):
        self.screen_width = screen_width
        self.bar_height = bar_height
        self.stat_boxes = []
        self.box_width = constants.STATUS_BAR_ITEM_BOX_WIDTH      
        self.box_height = constants.STATUS_BAR_ITEM_BOX_HEIGHT
        self.menu_open = False
        self.menu_width = constants.STATUS_BAR_MENU_ITEM_WIDTH
        self.menu_item_height = constants.STATUS_BAR_MENU_ITEM_HEIGHT
        self.menu_items_per_box = {}        
        self.current_stat_box_index = None  
        
    def toggle_menu(self, stat_box_index):
        if self.current_stat_box_index != stat_box_index:
            self.menu_open = True  # Open the menu
            self.current_stat_box_index = stat_box_index
        else:
            self.menu_open = not self.menu_open
            self.current_stat_box_index = None if not self.menu_open else stat_box_index

        
    def dummy_action(self):
        print("Dummy action")
        pass
    
    def add_menu_option(self, stat_box_index, label, action, thumbnail_path):
        # Ensure there is a list for the specified stat box
        if stat_box_index not in self.menu_items_per_box:
            self.menu_items_per_box[stat_box_index] = []
        thumbnail = arcade.load_texture(thumbnail_path)
        self.menu_items_per_box[stat_box_index].append({'label': label, 'action': action, 'thumbnail': thumbnail})

    def add_stat_box(self, text, thumbnail_path=None):
        thumbnail = arcade.load_texture(thumbnail_path) if thumbnail_path else None
        self.stat_boxes.append({'text': text, 'thumbnail': thumbnail})
        self._layout_stat_boxes()

    def update_stat_box(self, index, new_text):
        if 0 <= index < len(self.stat_boxes):
            self.stat_boxes[index]['text'] = new_text
            
    def update_menu_item(self, stat_box_index, menu_item_index, new_label, new_action, new_thumbnail_path):
        if stat_box_index in self.menu_items_per_box and 0 <= menu_item_index < len(self.menu_items_per_box[stat_box_index]):
            new_thumbnail = arcade.load_texture(new_thumbnail_path)

            self.menu_items_per_box[stat_box_index][menu_item_index] = {
                'label': new_label, 
                'action': new_action, 
                'thumbnail': new_thumbnail
            }


    def _layout_stat_boxes(self):
        num_boxes = len(self.stat_boxes)
        total_box_width = num_boxes * self.box_width
        start_x = (self.screen_width - total_box_width) / 2 + self.box_width / 2

        for i, stat_box in enumerate(self.stat_boxes):
            stat_box['x'] = start_x + i * self.box_width
            stat_box['y'] = self.bar_height / 2

    def on_mouse_press(self, x, y, button, modifiers):
        for index, stat_box in enumerate(self.stat_boxes):
        # Calculate the bounds of the stat box
            left = stat_box['x'] - self.box_width / 2
            right = stat_box['x'] + self.box_width / 2
            bottom = stat_box['y'] - self.box_height / 2
            top = stat_box['y'] + self.box_height / 2

            # Check if the click is within the stat box
            if left <= x <= right and bottom <= y <= top:
                self.toggle_menu(index)
                break

    def toggle_menu(self, stat_box_index):
    # Check if the clicked stat box is different from the current one
        if self.current_stat_box_index != stat_box_index:
            self.menu_open = True  # Open the menu
            self.current_stat_box_index = stat_box_index  # Update the current stat box index
        else:
            # Toggle the menu state if the same stat box is clicked again
            self.menu_open = not self.menu_open
            self.current_stat_box_index = None if not self.menu_open else stat_box_index

    def _get_stat_box_position(self, index):
        # Calculate the starting x position
        spacing = 1  
        total_spacing = (len(self.stat_boxes) - 1) * spacing
        total_box_width = len(self.stat_boxes) * self.box_width + total_spacing
        start_x = (self.screen_width - total_box_width) / 2 + self.box_width / 2

        # Calculate the x position of each box
        x = (start_x + index * (self.box_width + spacing)) - self.box_width/2 
        y = self.bar_height / 2  # Centered vertically in the status bar
        print ("_get_stat_box_position", x, y, self.box_width, self.box_height)
        return (x, y, self.box_width, self.box_height)



    def on_draw(self):
        for stat_box in self.stat_boxes:
            # Draw the box
            arcade.draw_rectangle_filled(center_x=stat_box['x'], center_y=stat_box['y'],
                                        width=self.box_width, height=self.box_height,
                                        color=constants.TRANSLUCENT_BACKGROUND_COLOR)
            arcade.draw_rectangle_outline(center_x=stat_box['x'], center_y=stat_box['y'],
                                        width=self.box_width, height=self.box_height,
                                        color=arcade.color.GRAY, border_width=2)
            
             # Draw the thumbnail if it exists
            if stat_box['thumbnail']:
                thumbnail_x = stat_box['x'] - self.box_width / 2 + 30
                thumbnail_y = stat_box['y']
                arcade.draw_texture_rectangle(thumbnail_x, thumbnail_y, width=35, height=35, texture=stat_box['thumbnail'])

            # Adjust text position to accommodate thumbnail
            text_x = stat_box['x'] - self.box_width / 2 + 60  # Adjust this position based on thumbnail size
            text_y = stat_box['y'] - self.box_height / 2 + 15
            arcade.draw_text(stat_box['text'], start_x=text_x, start_y=text_y, 
                             color=arcade.color.WHITE, font_size=19, font_name="Kenney Future")


        # Draw the menu if it is open and a stat box is selected
        if self.menu_open and self.current_stat_box_index is not None:
            menu_items = self.menu_items_per_box.get(self.current_stat_box_index, [])

            # Calculate position for the menu
            box_x, box_y, box_width, box_height = self._get_stat_box_position(self.current_stat_box_index)
            menu_x = box_x - self.menu_width / 2 + box_width / 2
            menu_y = box_y + box_height / 2  # Adjust this to position the menu correctly

            # Ensure the menu does not go off-screen
            menu_y = max(menu_y, self.menu_item_height * len(menu_items))


            # Draw the menu background
            menu_height = len(menu_items) * self.menu_item_height -self.menu_item_height if len(menu_items) > 1 else len(menu_items) * self.menu_item_height

            print("menu_x and menu_y", menu_x, menu_y)
            print("menu draw:", menu_x + (menu_x + self.menu_width / 2), (menu_y + menu_height / 2),self.menu_width, menu_height)
            
            arcade.draw_rectangle_filled(center_x=menu_x + self.menu_width / 2, 
                                        center_y=menu_y + menu_height / 2,
                                        width=self.menu_width, 
                                        height=menu_height, 
                                        color=constants.TRANSLUCENT_BACKGROUND_COLOR)

            # Draw each menu item
            for i, item in enumerate(menu_items):
                item_height = self.menu_item_height
                # Adjust item_y to start from the top of the menu and go downwards
                item_y = menu_y + menu_height - (i + 1) * item_height

                # Draw item background
                arcade.draw_rectangle_filled(center_x=menu_x + self.menu_width / 2,
                                            center_y=item_y + item_height / 2,
                                            width=self.menu_width,
                                            height=item_height,
                                            color=constants.TRANSLUCENT_BACKGROUND_COLOR)

                # Draw the label, positioned within the item
                label_x = menu_x + 80  # Padding from the left
                label_y = item_y + (item_height - 20) / 2  # Vertically center the text
                arcade.draw_text(item['label'], start_x=label_x, start_y=label_y,
                                color=arcade.color.WHITE, font_size=12)

                # Draw the thumbnail, positioned within the item
                thumbnail_x = menu_x + 25  
                thumbnail_y = item_y + item_height / 2
                arcade.draw_texture_rectangle(center_x=thumbnail_x,
                                            center_y=thumbnail_y,
                                            width=40, height=40,
                                            texture=item['thumbnail'])


class SharedData:
    doge_price= "Loading..."    
    display_width, display_height = arcade.get_display_size() # will cause error if called before window is created

    def get_doge_price(delta_time):
            try:
                if constants.DOGE_DATA_HUB_ONLINE:
                    response = requests.get('http://localhost:5000/currentPrice')
                    response.raise_for_status()
                    SharedData.doge_price = response.json()['dogecoin']
                    print(f"Current Dogecoin price: {SharedData.doge_price}")
                else:
                    SharedData.doge_price = 'N/A (offline)'
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
                self.player_sprite.change_y = constants.PLAYER_JUMP_SPEED
                self.jump_sound.play()
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -constants.PLAYER_MOVEMENT_SPEED
            self.player_sprite.scale_x = -1  # Flip sprite to face left

        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = constants.PLAYER_MOVEMENT_SPEED
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
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", constants.SPRITE_SCALING_BOX)
            wall.center_x = x
            wall.center_y = 90
            self.wall_list.append(wall)

        coordinate_list = [[200, 300], [300, 300], [400, 400], [500, 400], [600, 400]]

        for coordinate in coordinate_list:
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", constants.TILE_SCALING)
            wall.position = coordinate
            self.wall_list.append(wall)
        
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, gravity_constant=constants.GRAVITY)

    def on_draw(self):
        arcade.start_render()
        self.draw_sky()
        self.draw_hills()
        self.draw_clouds()
        self.update_clouds(1/60)
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
        
class PlayerCharacter(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.facing_direction = constants.LEFT_FACING
        self.position = (400,400)
        self.idle_textures = []
        self.run_textures = []
        self.spawn_textures = []
        sprite_count = 0 
        self.grow_sound = arcade.load_sound(str(ASSETS_PATH / "sounds" / "appear.wav"))        

        for row in range(6):  
            for col in range(7):
                if sprite_count >= constants.SPRITE_IDLE_FRAMES: 
                    break
                idle_texture = arcade.load_texture(str(ASSETS_PATH / "sprites" / "PlayerIdle.png"), x=col * constants.SPRITE_SIZE_WIDTH, y=row * constants.SPRITE_SIZE_HEIGHT, width=constants.SPRITE_SIZE_WIDTH, height=constants.SPRITE_SIZE_HEIGHT)
                self.idle_textures.append(idle_texture)
                sprite_count += 1
        
        sprite_count = 0 
        
        for row in range(5):  
            for col in range(6): 
                if sprite_count >= constants.SPRITE_RUN_FRAMES: 
                    break
                run_texture = arcade.load_texture(str(ASSETS_PATH / "sprites" / "PlayerRun.png"), x=col * constants.SPRITE_SIZE_WIDTH, y=row * constants.SPRITE_SIZE_HEIGHT, width=constants.SPRITE_SIZE_WIDTH, height=constants.SPRITE_SIZE_HEIGHT)
                self.run_textures.append(run_texture)
                sprite_count += 1
        sprite_count = 0 
        
        for row in range(4): 
            for col in range(5):  
                if sprite_count >= constants.SPRITE_SPAWN_FRAMES: 
                    break
                spawn_texture = arcade.load_texture(str(ASSETS_PATH / "sprites" / "PlayerSpawn.png"), x=col * constants.SPRITE_SIZE_WIDTH, y=row * constants.SPRITE_SIZE_HEIGHT, width=constants.SPRITE_SIZE_WIDTH, height=constants.SPRITE_SIZE_HEIGHT)
                self.spawn_textures.append(spawn_texture)
                sprite_count += 1
                        
        self.character_face_direction = constants.LEFT_FACING
        self.texture = self.idle_textures[0]
        self.jumping = False
        self.is_running = False
        self.cur_texture = 0

    def zoom_in(self):
        self.scale *= 2
        self.grow_sound.play()
        

    def zoom_out(self):
        self.scale *= 0.5
        self.grow_sound.play()

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
    arcade.schedule(SharedData.get_doge_price, constants.DOGE_DATA_HUB_CALLING_INTERVAL) 
    arcade.run()

if __name__ == "__main__":
    main()

