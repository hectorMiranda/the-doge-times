import arcade
from settings.config import ASSETS_PATH, LEFT_FACING, RIGHT_FACING, SPRITE_DEATH_FRAMES,SPRITE_CLIMB_FRAMES, SPRITE_IDLE_FRAMES, SPRITE_RUN_FRAMES, SPRITE_SPAWN_FRAMES, SPRITE_SIZE_WIDTH, SPRITE_SIZE_HEIGHT

    
class PlayerCharacter(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.facing_direction = LEFT_FACING
        self.idle_textures = []
        self.run_textures = []
        self.run_left_textures = []
        self.spawn_textures = []
        self.jump_textures = []
        self.jump_left_textures = []
        self.climb_textures = []
        self.death_textures = []
        self.grow_sound = arcade.load_sound(str(ASSETS_PATH / "sounds" / "appear.wav"))    
        self.isAlive = True
        
        self.is_being_dragged = False
        self.drag_start_x = 0
        self.drag_start_y = 0

        sprite_count = 0 
        for row in range(6):  
            for col in range(7):
                if sprite_count >= SPRITE_IDLE_FRAMES: 
                    break
                idle_texture = arcade.load_texture(str(ASSETS_PATH / "sprites" / "PlayerIdle.png"), x=col * SPRITE_SIZE_WIDTH, y=row * SPRITE_SIZE_HEIGHT, width=SPRITE_SIZE_WIDTH, height=SPRITE_SIZE_HEIGHT)
                self.idle_textures.append(idle_texture)
                sprite_count += 1
        
        sprite_count = 0      
        for row in range(5):  
            for col in range(6): 
                if sprite_count >= SPRITE_RUN_FRAMES: 
                    break
                run_texture = arcade.load_texture(str(ASSETS_PATH / "sprites" / "PlayerRun.png"), x=col * SPRITE_SIZE_WIDTH, y=row * SPRITE_SIZE_HEIGHT, width=SPRITE_SIZE_WIDTH, height=SPRITE_SIZE_HEIGHT)
                self.run_textures.append(run_texture)
                sprite_count += 1
        
        sprite_count = 0         
        for row in range(5):  
            for col in range(6): 
                if sprite_count >= SPRITE_RUN_FRAMES: 
                    break
                run_left_texture = arcade.load_texture(str(ASSETS_PATH / "sprites" / "PlayerRun.png"), x=col * SPRITE_SIZE_WIDTH, y=row * SPRITE_SIZE_HEIGHT, width=SPRITE_SIZE_WIDTH, height=SPRITE_SIZE_HEIGHT, flipped_horizontally=True)
                self.run_left_textures.append(run_left_texture)
                sprite_count += 1
        
        sprite_count = 0 
        for row in range(4): 
            for col in range(5):  
                if sprite_count >= SPRITE_SPAWN_FRAMES: 
                    break
                spawn_texture = arcade.load_texture(str(ASSETS_PATH / "sprites" / "PlayerSpawn.png"), x=col * SPRITE_SIZE_WIDTH, y=row * SPRITE_SIZE_HEIGHT, width=SPRITE_SIZE_WIDTH, height=SPRITE_SIZE_HEIGHT)
                self.spawn_textures.append(spawn_texture)
                sprite_count += 1
                
                
        sprite_count = 0 
        for row in range(7): 
            for col in range(7):  
                if sprite_count >= SPRITE_RUN_FRAMES: 
                    break
                jump_texture = arcade.load_texture(str(ASSETS_PATH / "sprites" / "PlayerJump.png"), x=col * SPRITE_SIZE_WIDTH, y=row * SPRITE_SIZE_HEIGHT, width=SPRITE_SIZE_WIDTH, height=SPRITE_SIZE_HEIGHT)
                self.jump_textures.append(jump_texture)
                sprite_count += 1
                
                
        sprite_count = 0 
        for row in range(7): 
            for col in range(7):  
                if sprite_count >= SPRITE_RUN_FRAMES: 
                    break
                jump_left_texture = arcade.load_texture(str(ASSETS_PATH / "sprites" / "PlayerJump.png"), x=col * SPRITE_SIZE_WIDTH, y=row * SPRITE_SIZE_HEIGHT, width=SPRITE_SIZE_WIDTH, height=SPRITE_SIZE_HEIGHT, flipped_horizontally=True)
                self.jump_left_textures.append(jump_left_texture)
                sprite_count += 1
                
        sprite_count = 0 
        for row in range(2): 
            for col in range(7):  
                if sprite_count >= SPRITE_CLIMB_FRAMES: 
                    break
                climb_texture = arcade.load_texture(str(ASSETS_PATH / "sprites" / "PlayerClimbing.png"), x=col * SPRITE_SIZE_WIDTH, y=row * SPRITE_SIZE_HEIGHT, width=SPRITE_SIZE_WIDTH, height=SPRITE_SIZE_HEIGHT)
                self.climb_textures.append(climb_texture)
                sprite_count += 1
                
        sprite_count = 0 
        for row in range(3): 
            for col in range(5):  
                if sprite_count >= SPRITE_DEATH_FRAMES: 
                    break
                death_texture = arcade.load_texture(str(ASSETS_PATH / "sprites" / "PlayerDeath.png"), x=col * SPRITE_SIZE_WIDTH, y=row * SPRITE_SIZE_HEIGHT, width=SPRITE_SIZE_WIDTH, height=SPRITE_SIZE_HEIGHT)
                self.death_textures.append(death_texture)
                sprite_count += 1
                        
        self.character_face_direction = LEFT_FACING
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
        self.cur_texture += 1
        
        if self.change_x == 0 and self.change_y == 0: # Standing still
            if self.cur_texture >= 3 * len(self.idle_textures):
                self.cur_texture = 0
            self.texture = self.idle_textures[self.cur_texture // 3]
        elif self.change_x < 0: #left
            if self.cur_texture >= 3 * len(self.run_left_textures):
                self.cur_texture = 0
            self.texture = self.run_left_textures[self.cur_texture // 3]
        elif self.change_x > 0: #right
            if self.cur_texture >= 3 * len(self.run_textures):
                self.cur_texture = 0
            self.texture = self.run_textures[self.cur_texture // 3]
        
        if self.change_y != 0: #jump
            if self.cur_texture >= 3 * len(self.climb_textures):
                self.cur_texture = 0
            self.texture = self.climb_textures[self.cur_texture // 3]
        if self.change_y != 0 and self.change_x < 0: #jump left
            if self.cur_texture >= 3 * len(self.jump_textures):
                self.cur_texture = 0
            self.texture = self.jump_left_textures[self.cur_texture // 3]
        if self.change_y != 0 and self.change_x > 0: #jump
            if self.cur_texture >= 3 * len(self.jump_textures):
                self.cur_texture = 0
            self.texture = self.jump_textures[self.cur_texture //3]
            
        if self.isAlive == False:
            if self.cur_texture >= 3 * len(self.death_textures):
                self.cur_texture = 0
            self.texture = self.death_textures[self.cur_texture // 3]

    def on_mouse_press(self, x, y, button, modifiers):
        print("mouse press")
        if self.collides_with_point((x, y)) and button == arcade.MOUSE_BUTTON_LEFT:
            print("player collides with mouse click")
            self.is_being_dragged = True
            self.drag_start_x = x - self.center_x
            self.drag_start_y = y - self.center_y

    def on_mouse_release(self, x, y, button, modifiers):
        print("mouse release")
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.is_being_dragged = False

    def on_mouse_motion(self, x, y, dx, dy):
        print("mouse motion")
        if self.is_being_dragged:
            print("being dragged")
            self.center_x = x - self.drag_start_x
            self.center_y = y - self.drag_start_y


