from kivy.uix.image import Image
from kivy.core.window import Window
import random

class Bomb:
    def __init__(self, x, y):
        self.texture = Image(source='images/bomb.png').texture
        self.size = (40, 40)
        self.x_pos = x
        self.y_pos = y
        self.speed = random.uniform(2, 4)
        self.moving_right = random.choice([True, False])
        self.points = -5  # Negative points for bombs
        self.respawn()

    def update(self, dt):
        if self.moving_right:
            self.x_pos += self.speed
            if self.x_pos > Window.width - self.size[0]:
                self.moving_right = False
        else:
            self.x_pos -= self.speed
            if self.x_pos < 0:
                self.moving_right = True

    def respawn(self):
        self.x_pos = random.randint(100, Window.width - 100)
        self.y_pos = random.randint(100, 300)
        self.speed = random.uniform(2, 4)
        self.moving_right = random.choice([True, False])
