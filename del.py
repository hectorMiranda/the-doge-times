import time
import arcade

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "FPS Test")
        self.fps_count = 0
        self.start_time = time.time()
        self.fps = 0  # Initialize fps here

    def on_update(self, delta_time):
        self.fps_count += 1
        current_time = time.time()
        if current_time - self.start_time >= 1:
            self.fps = self.fps_count / (current_time - self.start_time)
            self.fps_count = 0
            self.start_time = current_time

    def on_draw(self):
        arcade.start_render()
        fps_text = f"FPS: {self.fps:.2f}"
        arcade.draw_text(fps_text, 10, 20, arcade.color.WHITE, 14)

def main():
    game = MyGame()
    arcade.run()

if __name__ == "__main__":
    main()
