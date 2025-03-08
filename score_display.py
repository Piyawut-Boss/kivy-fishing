from kivy.uix.widget import Widget  # Changed from FloatLayout to Widget
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

class ScoreDisplay(Widget):  # Changed to Widget
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Main score (top left)
        self.score_label = Label(
            text='SCORE: 0',
            pos=(20, Window.height - 50),
            font_size=40,
            bold=True,
            color=(1, 1, 0, 1)  # Bright yellow
        )
        
        # Fish count (top center)
        self.fish_count = Label(
            text='FISH: 0',
            pos=(Window.width//2 - 50, Window.height - 50),
            font_size=40,
            bold=True,
            color=(0, 1, 1, 1)  # Cyan
        )
        
        # High score (top right)
        self.high_score = Label(
            text='BEST: 0',
            pos=(Window.width - 200, Window.height - 50),
            font_size=40,
            bold=True,
            color=(1, 0.5, 0, 1)  # Orange
        )
        
        # Add labels
        self.add_widget(self.score_label)
        self.add_widget(self.fish_count)
        self.add_widget(self.high_score)

    def update_score(self, score, animate=False):
        self.score_label.text = f'SCORE: {score}'

    def update_fish_count(self, count):
        self.fish_count.text = f'FISH: {count}'

    def update_high_score(self, score):
        self.high_score.text = f'BEST: {score}'
