import arcade

class SpriteManager:
    """
    A utility class for managing sprites in the arcade library.
    """

    def __init__(self, window_width, window_height):
        """
        Initialize the SpriteManager.
        """
        self.window_width = window_width
        self.window_height = window_height

    @staticmethod
    def load_texture_pair(filename):
        """
        Load a texture pair, with the second being a mirror image.

        :param filename: The path to the texture file.
        :return: A list of two arcade.Texture objects.
        """
        return [
            arcade.load_texture(filename),
            arcade.load_texture(filename, flipped_horizontally=True),
        ]
        
    def load_and_center_sprite(self, filename):
        """
        Load an image and center it in the middle of the screen.

        :param filename: The path to the image file.
        :return: An arcade.Sprite object centered on the screen.
        """
        sprite = arcade.Sprite(filename)
        sprite.center_x = self.window_width - sprite.width / 2
        sprite.center_y = self.window_height - sprite.height / 2
        return sprite


    @staticmethod
    def center_sprite(sprite):
        """
        Center the anchor point of a sprite.

        :param sprite: The sprite to center.
        """
        sprite.center_x = sprite.width / 2
        sprite.center_y = sprite.height / 2

    @staticmethod
    def scale_sprite(sprite, scale):
        """
        Scale a sprite.

        :param sprite: The sprite to scale.
        :param scale: The scaling factor.
        """
        sprite.scale = scale

    @staticmethod
    def flip_sprite(sprite, horizontal=True, vertical=False):
        """
        Flip a sprite horizontally or vertically.

        :param sprite: The sprite to flip.
        :param horizontal: Whether to flip horizontally.
        :param vertical: Whether to flip vertically.
        """
        if horizontal:
            sprite.texture = arcade.load_texture(sprite.texture.name, flipped_horizontally=True)
        if vertical:
            sprite.texture = arcade.load_texture(sprite.texture.name, flipped_vertically=True)

    @staticmethod
    def rotate_sprite(sprite, angle):
        """
        Rotate a sprite.

        :param sprite: The sprite to rotate.
        :param angle: The angle of rotation in degrees.
        """
        sprite.angle = angle

    @staticmethod
    def create_animated_sprite(file_path, scaling, columns, count, loop=True):
        """
        Create an animated sprite.

        :param file_path: Path to the spritesheet.
        :param scaling: Scale factor for the sprite.
        :param columns: Number of columns in the spritesheet.
        :param count: Number of images in the spritesheet.
        :param loop: Whether the animation should loop.
        :return: An instance of arcade.AnimatedTimeBasedSprite.
        """
        return arcade.AnimatedTimeBasedSprite(
            file_path, scaling, columns, count, loop=loop
        )