from kivy.uix.image import Image
from kivy.properties import BooleanProperty, NumericProperty
from boat import Boat

class Hook(Image):
    is_fishing = BooleanProperty(False)
    speed = NumericProperty(4)
    
    def __init__(self, boat, **kwargs):
        super().__init__(**kwargs)
        self.source = 'images/hook.png'
        self.size_hint = (None, None)
        self.size = (15, 30)
        self.boat = boat
        self.reset()
        
    def reset(self):
        self.pos = (self.boat.x + 85, self.boat.y - 30)
        self.is_fishing = False
        
    def start_fishing(self):
        if not self.is_fishing:
            self.is_fishing = True
            
    def update(self):
        if not self.is_fishing:
            self.x = self.boat.x + 85
            self.y = self.boat.y - 30
        else:
            self.y -= self.speed
            if self.y < 50:
                self.is_fishing = False

    def check_collision(self, fish):
        """ ตรวจจับการชนกันของเบ็ดและปลา ให้ง่ายขึ้น """
        return (abs(self.x - fish.x_pos) < fish.size[0] * 0.8 and 
                abs(self.y - fish.y_pos) < fish.size[1] * 0.8)
