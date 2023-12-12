import arcade
import random

# Game window settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "SortQuest"

class Book(arcade.Sprite):
    """ Represents a book in the game """
    def __init__(self, value, position_x):
        super().__init__()
        self.value = value
        self.width = 40
        self.height = value * 5  # Height based on value
        self.center_x = position_x
        self.center_y = self.height / 2 + 100  # Offset from bottom of the screen
        self.color = arcade.color.BLUE

        # Target positions for animation
        self.target_x = position_x
        self.target_y = self.center_y

    def draw_book(self):
        # Draw the book as a rectangle
        arcade.draw_rectangle_filled(self.center_x, 
                                     self.center_y, 
                                     self.width, 
                                     self.height, 
                                     self.color)
        
         # Draw the value on the book
        text_x = self.center_x
        text_y = self.center_y - 7  # Adjust the Y position to center the text
        arcade.draw_text(str(self.value), text_x, text_y, arcade.color.WHITE, 12, 
                         width=self.width, align="center", anchor_x="center", anchor_y="center")

    def update_animation(self, delta_time: float = 1/60):
        if self.center_x != self.target_x:
            self.center_x = arcade.lerp(self.center_x, self.target_x, delta_time * 5)  # Adjust 5 for speed

        if self.center_y != self.target_y:
            self.center_y = arcade.lerp(self.center_y, self.target_y, delta_time * 5)  # Adjust 5 for speed

class SortQuestGame(arcade.Window):
    """
    Main game class for SortQuest.
    """
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.book_list = []
        self.selected_book = None
        self.move_count = 0
        self.is_sorted = False
        self.current_level = 1
        self.dragged_book_shadow = None  # Shadow of the book being dragged
        self.setup()

    def setup(self):
        # Reset game state for new level
        self.book_list = arcade.SpriteList()  # Use SpriteList instead of a regular list
        self.move_count = 0
        self.is_sorted = False
        # Create a list of books with random values
        for i in range(10 + self.current_level):
            book = Book(random.randint(1, 20), i * 50 + 50)
            self.book_list.append(book)

    def on_draw(self):
        """
        Render the screen.
        """
        arcade.start_render()
        # Draw the books
        for book in self.book_list:
            book.draw_book()
        # Display the move count and instructions
        arcade.draw_text(f"Moves: {self.move_count}", 10, SCREEN_HEIGHT - 20, arcade.color.WHITE, 14)
        if not self.is_sorted:
            arcade.draw_text(f"Level {self.current_level}: Sort the books!", 10, SCREEN_HEIGHT - 40, arcade.color.WHITE, 14)
        else:
            arcade.draw_text("Sorted! Click to proceed to the next level!", 10, SCREEN_HEIGHT - 40, arcade.color.GREEN, 14)
        if self.dragged_book_shadow:
            self.dragged_book_shadow.draw()

    def on_update(self, delta_time):
        """
        Contains the game logic.
        """
        if not self.is_sorted:
            self.check_sort()
        else:
            print("Books are sorted!")  # Placeholder action
            self.setup_next_level()

        for book in self.book_list:
            book.update_animation(delta_time)

    def check_sort(self):
        """
        Check if the books are sorted.
        """
        self.is_sorted = all(self.book_list[i].value <= self.book_list[i + 1].value for i in range(len(self.book_list) - 1))

    def setup_next_level(self):
        """
        Advance to the next level when the player clicks.
        """
        if arcade.check_for_mouse_press():
            self.current_level += 1
            self.setup()

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        books = arcade.get_sprites_at_point((x, y), self.book_list)
        if books:
            # Select the topmost book
            self.selected_book = books[0]
             # Create a shadow effect for the book being dragged
            self.dragged_book_shadow = arcade.SpriteSolidColor(self.selected_book.width, self.selected_book.height, arcade.color.GRAY)
    
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.selected_book:
            # Update the position of the shadow effect
            self.dragged_book_shadow.center_x = x
            self.dragged_book_shadow.center_y = y

    def on_mouse_release(self, x, y, button, key_modifiers):
        if self.selected_book:
            closest_book = min((book for book in self.book_list if book != self.selected_book),
                            key=lambda book: abs(book.center_x - x))

            # Set target positions for animation
            self.selected_book.target_x, closest_book.target_x = closest_book.center_x, self.selected_book.center_x
            
            self.move_count += 1
            self.selected_book = None
            self.dragged_book_shadow = None



def main():
    """ Main method """
    game = SortQuestGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()

if __name__ == "__main__":
    main()
