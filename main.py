from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics import Rectangle, Color, Line  # Add this import
from boat import Boat
from fish import Fish
from hook import Hook
from info_json import *
from score_display import ScoreDisplay
from menu import MenuScreen  # Only import MenuScreen

class FishingGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.size = (1600, 900)
        
        # Initialize game objects
        self.boat = Boat()
        self.hook = Hook(self.boat)
        self.json_data = read_json()
        
        # Create mixed fish population
        self.fishes = []
        # Add regular fish
        for _ in range(4):
            self.fishes.append(Fish(800, 200, 'regular'))
        # Add sharks
        for _ in range(2):
            self.fishes.append(Fish(800, 200, 'shark'))
        
        # Load background
        self.background_texture = Image(source='images/background.png').texture
        
        # Setup score display
        self.score_display = ScoreDisplay()
        self.score_display.update_score(0)
        self.score_display.update_fish_count(0)
        self.score_display.update_high_score(self.json_data["best_result"])
        self.add_widget(self.score_display)
        
        # Setup keyboard
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)
        self.pressed_keys = set()
        
        Clock.schedule_interval(self.update, 1.0/60.0)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard.unbind(on_key_up=self._on_key_up)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        self.pressed_keys.add(keycode[1])
        if keycode[1] == 'spacebar':
            self.hook.start_fishing()
        return True

    def _on_key_up(self, keyboard, keycode):
        if keycode[1] in self.pressed_keys:
            self.pressed_keys.remove(keycode[1])
        return True
            
    def update(self, dt):
        # Handle movement
        if ('left' in self.pressed_keys or 'a' in self.pressed_keys):
            self.boat.move_left()
        if ('right' in self.pressed_keys or 'd' in self.pressed_keys):
            self.boat.move_right(Window.width)
            
        # Update all fish
        for fish in self.fishes:
            fish.update(dt)
            # Check collision for each fish
            if self.hook.is_hook_moving:
                if (abs(self.boat.x + 115 - fish.x_pos) < 60 and
                    abs(self.hook.y_pos - fish.y_pos) < 40):
                    self.handle_catch(fish)
        
        # Update hook
        self.hook.update(self.boat)
                
        self.draw()

    def handle_catch(self, caught_fish):
        self.boat.caught_fish()
        # Update scores with points based on fish type
        self.score_display.update_score(
            self.boat.caught_fishes * caught_fish.points, 
            animate=True
        )
        self.score_display.update_fish_count(self.boat.caught_fishes)
        
        # Respawn caught fish
        caught_fish.respawn()
        self.hook.reset()
        
        # Update high score if needed
        if self.boat.caught_fishes > self.json_data["best_result"]:
            self.json_data["best_result"] = self.boat.caught_fishes
            self.score_display.update_high_score(self.json_data["best_result"])
            save_on_close(self.json_data, self.boat.caught_fishes)

    def draw(self):
        self.canvas.clear()
        with self.canvas:
            # Draw background first
            Rectangle(texture=self.background_texture, pos=(0, 0), 
                     size=(Window.width, Window.height))
            
            # Draw boat (bigger)
            Rectangle(texture=self.boat.current_texture, 
                     pos=(self.boat.x, self.boat.y), 
                     size=(180, 95))
            
            # Adjust fishing line for bigger boat
            Color(1, 0, 0)
            Line(points=[self.boat.x + 90, self.boat.y + 20,
                        self.boat.x + 90, self.hook.y_pos])
            
            # Reset color to white before drawing sprites
            Color(1, 1, 1, 1)  # White color, full opacity
            
            # Adjust hook position for bigger boat
            Rectangle(texture=self.hook.texture,
                     pos=(self.boat.x + 85, self.hook.y_pos),
                     size=self.hook.size)
            
            # Draw all fish with their proper sizes
            for fish in self.fishes:
                Rectangle(texture=fish.current_texture,
                         pos=(fish.x_pos, fish.y_pos),
                         size=fish.size)  # Use fish's individual size
            
            # Make sure score display is always visible
            self.score_display.pos = (0, 0)

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game = FishingGame()
        self.add_widget(self.game)

class FishermanApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(GameScreen(name='game'))
        return sm

if __name__ == '__main__':
    FishermanApp().run()
