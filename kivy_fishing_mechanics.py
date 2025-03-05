import random
from kivy.event import EventDispatcher
from kivy.properties import NumericProperty, StringProperty

class KivyFishingMechanics(EventDispatcher):
    depth = NumericProperty(0)
    fish_type = StringProperty('common')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fish_types = {
            'common': 1,
            'rare': 3,
            'legendary': 5
        }
        
    def try_catch(self, depth):
        self.depth = depth
        if depth < 300:
            return self.surface_catch()
        elif depth < 500:
            return self.medium_catch()
        else:
            return self.deep_catch()
            
    def surface_catch(self):
        if random.random() > 0.95:
            self.fish_type = 'rare'
            return self.fish_types['rare']
        self.fish_type = 'common'
        return self.fish_types['common']
        
    def medium_catch(self):
        roll = random.random()
        if roll > 0.8:
            self.fish_type = 'legendary'
            return self.fish_types['legendary']
        elif roll > 0.4:
            self.fish_type = 'rare'
            return self.fish_types['rare']
        self.fish_type = 'common'
        return self.fish_types['common']
        
    def deep_catch(self):
        roll = random.random()
        if roll > 0.6:
            self.fish_type = 'legendary'
            return self.fish_types['legendary']
        elif roll > 0.3:
            self.fish_type = 'rare'
            return self.fish_types['rare']
        self.fish_type = 'common'
        return self.fish_types['common']
