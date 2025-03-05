from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.graphics import Rectangle, Color

class DepthMeter(Widget):
    depth = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (30, 200)
        self.bind(pos=self.update_meter, size=self.update_meter)
        
    def update_meter(self, *args):
        self.canvas.clear()
        with self.canvas:
            # Background
            Color(0.4, 0.4, 0.4)
            Rectangle(pos=self.pos, size=self.size)
            
            # Depth indicator
            Color(0, 0.75, 1)
            height = (self.depth / 700) * self.height
            Rectangle(pos=self.pos, size=(self.width, height))
