from kivy.uix.image import Image
from boat import Boat
from fishing_line import FishLine


class Hook:
    def __init__(self, boat: Boat):
        self.texture = Image(source="images/hook.png").texture
        self.size = (15, 30)
        self.y_pos = boat.y - 15  # Adjusted for smaller boat
        self.is_hook_moving = False
        self.going_down = True

    def start_fishing(self):
        self.is_hook_moving = True
        self.going_down = True

    def reset(self):
        self.is_hook_moving = False

    def update(self, boat: Boat):
        if not self.is_hook_moving:
            self.y_pos = boat.y - 15  # Adjusted for smaller boat
            return

        if self.going_down:
            self.y_pos -= 5  # Move down instead of up
            if self.y_pos < 50:  # Stop near bottom
                self.going_down = False
        else:
            self.y_pos += 5  # Move up for retrieval
            if self.y_pos > boat.y - 30:
                self.is_hook_moving = False
                self.going_down = True
