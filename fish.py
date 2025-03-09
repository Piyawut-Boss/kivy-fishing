from kivy.uix.image import Image
from kivy.core.window import Window
import random

class Fish(Image):
    FISH_TYPES = {
        'regular': {
            'left': 'images/fish_1_left.png',
            'right': 'images/fish_1_right.png',
            'size': (60, 40),
            'speed_range': (2, 4),
            'points': 1
        },
        'shark': {
            'left': 'images/shark_left.png',
            'right': 'images/shark_right.png',
            'size': (180, 120),  # Increased from (120, 80)
            'speed_range': (3, 5),  # Increased from (1, 3)
            'points': 5  # Increased points for catching harder shark
        },
        'tropical': {  # New tropical fish type
            'left': 'images/tropical_left.png',
            'right': 'images/tropical_right.png',
            'size': (70, 45),
            'speed_range': (4, 6),  # Faster than regular fish
            'points': 3  # Worth more than regular fish but less than shark
        }
    }

    def __init__(self, x, y, fish_type='regular'):
        super().__init__()
        self.fish_type = fish_type
        self.texture_left = Image(source=self.FISH_TYPES[fish_type]['left']).texture
        self.texture_right = Image(source=self.FISH_TYPES[fish_type]['right']).texture
        self.current_texture = self.texture_left
        self.size = self.FISH_TYPES[fish_type]['size']
        self.points = self.FISH_TYPES[fish_type]['points']
        self.respawn(fish_type)  # Ensure we call respawn with fish_type

    def update(self, dt):
        if self.moving_right:
            self.x_pos += self.speed
            self.current_texture = self.texture_right
            if self.x_pos > Window.width - self.size[0]:
                self.moving_right = False
        else:
            self.x_pos -= self.speed
            self.current_texture = self.texture_left
            if self.x_pos < 0:
                self.moving_right = True
                
    def respawn(self, fish_type=None):
        if fish_type:
            self.fish_type = fish_type  # Update fish type if passed

        speed_min, speed_max = self.FISH_TYPES[self.fish_type]['speed_range']
        self.x_pos = random.randint(100, Window.width - 100)
        self.y_pos = random.randint(100, 300)
        self.speed = random.uniform(speed_min, speed_max)
        self.moving_right = random.choice([True, False])
        
        # Update texture and size after respawning
        self.texture_left = Image(source=self.FISH_TYPES[self.fish_type]['left']).texture
        self.texture_right = Image(source=self.FISH_TYPES[self.fish_type]['right']).texture
        self.size = self.FISH_TYPES[self.fish_type]['size']
        self.points = self.FISH_TYPES[self.fish_type]['points']
        self.current_texture = self.texture_left
