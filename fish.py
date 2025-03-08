from kivy.uix.image import Image
from kivy.core.window import Window
import random

class Fish:
    def __init__(self, x, y):
        self.respawn()  # Start at random position
        self.texture_left = Image(source='images/fish_1_left.png').texture
        self.texture_right = Image(source='images/fish_1_right.png').texture
        self.current_texture = self.texture_left
        self.size = (60, 40)  # Add size property for smaller fish
        
    def update(self, dt):
        if self.moving_right:
            self.x_pos += self.speed
            self.current_texture = self.texture_right
            if self.x_pos > 1500:  # Fixed boundary check
                self.moving_right = False
        else:
            self.x_pos -= self.speed
            self.current_texture = self.texture_left
            if self.x_pos < 0:
                self.moving_right = True
                
    def respawn(self):
        self.x_pos = random.randint(100, 1400)
        self.y_pos = random.randint(100, 300)  # Keep fish in bottom third of screen
        self.speed = random.uniform(2, 4)  # Random speed for each fish
        self.moving_right = random.choice([True, False])  # Random direction
