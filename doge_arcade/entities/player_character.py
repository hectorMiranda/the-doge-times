import arcade
from settings.constants import ASSETS_PATH, LEFT_FACING, RIGHT_FACING, SPRITE_IDLE_FRAMES, SPRITE_RUN_FRAMES, SPRITE_SPAWN_FRAMES, SPRITE_SIZE_WIDTH, SPRITE_SIZE_HEIGHT

    
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
        self.grow_sound = arcade.load_sound(str(ASSETS_PATH / "sounds" / "appear.wav"))        

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
        if self.change_x == 0: # Standing still
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
        
        if self.change_y != 0 and self.change_x < 0: #jump left
            if self.cur_texture >= 3 * len(self.jump_textures):
                self.cur_texture = 0
            self.texture = self.jump_left_textures[self.cur_texture // 3]
        if self.change_y != 0 and self.change_x > 0: #jump
            if self.cur_texture >= 3 * len(self.jump_textures):
                self.cur_texture = 0
            self.texture = self.jump_textures[self.cur_texture // 3]


