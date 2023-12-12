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

    def draw_book(self):
        # Draw the book as a rectangle
        arcade.draw_rectangle_filled(self.center_x, 
                                     self.center_y, 
                                     self.width, 
                                     self.height, 
                                     self.color)

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

    def on_update(self, delta_time):
        """
        Contains the game logic.
        """
        if not self.is_sorted:
            self.check_sort()
        else:
            self.setup_next_level()

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

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when the user releases a mouse button.
        """
        if self.selected_book:
            # Find the closest book to swap positions with
            closest_book = min((book for book in self.book_list if book != self.selected_book),
                               key=lambda book: abs(book.center_x - x))

            # Swap positions of the books
            self.selected_book.center_x, closest_book.center_x = closest_book.center_x, self.selected_book.center_x
            
            self.move_count += 1

            self.selected_book = None


def main():
    """ Main method """
    game = SortQuestGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()

if __name__ == "__main__":
    main()
