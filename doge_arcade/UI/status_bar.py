import arcade
import arcade.gui
from settings.config import STATUS_BAR_ITEM_BOX_WIDTH, STATUS_BAR_ITEM_BOX_HEIGHT, STATUS_BAR_MENU_ITEM_WIDTH, STATUS_BAR_MENU_ITEM_HEIGHT, TRANSLUCENT_BACKGROUND_COLOR   
import math
import time

class StatusBar:
    def __init__(self, screen_width, bar_height=50):
        self.screen_width = screen_width
        self.bar_height = bar_height
        self.stat_boxes = []
        self.box_width = STATUS_BAR_ITEM_BOX_WIDTH      
        self.box_height = STATUS_BAR_ITEM_BOX_HEIGHT
        self.menu_open = False
        self.menu_width = STATUS_BAR_MENU_ITEM_WIDTH
        self.menu_item_height = STATUS_BAR_MENU_ITEM_HEIGHT
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

    def draw(self):
        for stat_box in self.stat_boxes:
            # Draw the box
            arcade.draw_rectangle_filled(center_x=stat_box['x'], center_y=stat_box['y'],
                                        width=self.box_width, height=self.box_height,
                                        color=TRANSLUCENT_BACKGROUND_COLOR)
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
                                        color=TRANSLUCENT_BACKGROUND_COLOR)

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
                                            color=TRANSLUCENT_BACKGROUND_COLOR)

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
