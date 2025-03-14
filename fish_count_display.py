from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window

class FishCountDisplay(Widget):
    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self.label = Label(text=f"Fish caught: {self.game.caught_fish_count}",
                           font_size=30,
                           size_hint=(None, None),
                           size=(200, 50),
                           pos=(Window.width / 1 - 100, Window.height - 1))
        self.add_widget(self.label)
        Clock.schedule_interval(self.update_count, 1 / 30)
    
    def update_count(self, dt):
        self.label.text = f"Fish caught: {self.game.caught_fish_count}"
