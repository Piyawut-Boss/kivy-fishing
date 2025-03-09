from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.app import App

class GameOverScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=20, padding=50)
        
        # Game Over text
        game_over_label = Label(
            text='GAME OVER!',
            font_size=80,
            color=(1, 0, 0, 1),  # Red color
            size_hint_y=0.4
        )
        
        # Final score display
        self.score_label = Label(
            text='Final Score: 0',
            font_size=60,
            color=(1, 0.8, 0, 1),  # Gold color
            size_hint_y=0.3
        )
        
        # Play Again button
        retry_btn = Button(
            text='Play Again',
            size_hint=(None, None),
            size=(300, 80),
            pos_hint={'center_x': 0.5},
            font_size=40
        )
        retry_btn.bind(on_release=self.play_again)
        
        # Menu button
        menu_btn = Button(
            text='Main Menu',
            size_hint=(None, None),
            size=(300, 80),
            pos_hint={'center_x': 0.5},
            font_size=40
        )
        menu_btn.bind(on_release=self.go_to_menu)
        
        # Add Quit button
        quit_btn = Button(
            text='Quit Game',
            size_hint=(None, None),
            size=(300, 80),
            pos_hint={'center_x': 0.5},
            font_size=40,
            background_color=(1, 0.3, 0.3, 1)  # Red color
        )
        quit_btn.bind(on_release=self.quit_game)
        
        layout.add_widget(game_over_label)
        layout.add_widget(self.score_label)
        layout.add_widget(retry_btn)
        layout.add_widget(menu_btn)
        layout.add_widget(quit_btn)  # Add quit button at the end
        
        self.add_widget(layout)
    
    def update_score(self, score):
        self.score_label.text = f'Final Score: {score}'
    
    def play_again(self, *args):
        self.manager.current = 'game'
    
    def go_to_menu(self, *args):
        self.manager.current = 'menu'
    
    def quit_game(self, *args):
        """Close the entire application"""
        App.get_running_app().stop()
