from kivy.uix.image import Image


class Boat:
    __MOVE_SPEED = 3
    __BOAT_WIDTH = 180  # Increased from 125
    __BOAT_HEIGHT = 95  # Increased from 65

    def __init__(self, x=700, y=800):  # Changed y position from 750 to 800 for higher position
        self.x = x
        self.y = y
        self.caught_fishes = 0
        self.texture_left = Image(source='images/boat_left.png').texture
        self.texture_right = Image(source='images/boat_right.png').texture
        self.current_texture = self.texture_left

    def move_left(self):
        if self.x > 0:
            self.x -= self.__MOVE_SPEED
            self.current_texture = self.texture_left

    def move_right(self, screen_width: int):
        if self.x < screen_width - self.__BOAT_WIDTH:  # Using new width
            self.x += self.__MOVE_SPEED
            self.current_texture = self.texture_right

    def caught_fish(self):
        self.caught_fishes += 1
