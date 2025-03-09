import random  # เพิ่มการ import random
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
from bomb import Bomb

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
        
        # Add bombs
        self.bombs = [Bomb(800, 200) for _ in range(3)]
        
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

        # Add label to display caught fish count
        from kivy.uix.label import Label
        self.caught_fish_count = 0  # Initialize the fish count
        self.fish_count_label = Label(text=f"Fish caught: {self.caught_fish_count}", pos=(10, Window.height - 30), font_size=20)
        self.add_widget(self.fish_count_label)
        
        Clock.schedule_interval(self.update, 1.0/60.0)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard.unbind(on_key_up(self._on_key_up))
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
            
        # Update all fish and check collisions
        for fish in self.fishes:
            fish.update(dt)
            if self.hook.is_fishing and self.hook.check_collision(fish):
                self.handle_catch(fish)
        
        # Update bombs and check collisions
        for bomb in self.bombs:
            bomb.update(dt)
            if self.hook.is_fishing and self.hook.check_collision(bomb):
                self.handle_bomb_collision(bomb)
        
        # Update hook
        self.hook.update()
                
        self.draw()

    def handle_catch(self, caught_fish):
        self.boat.caught_fish()
        self.caught_fish_count += 1  # Increment the caught fish count
        
        # Update scores with points based on fish type
        self.score_display.update_score(
            self.boat.caught_fishes * caught_fish.points, 
            animate=True
        )
        self.score_display.update_fish_count(self.boat.caught_fishes)
        
        # Update the caught fish count label
        self.fish_count_label.text = f"Fish caught: {self.caught_fish_count}"
        
        # Respawn caught fish with random type
        new_fish_type = random.choice(['regular', 'shark'])  # Randomly choose between 'regular' and 'shark'
        caught_fish.respawn(fish_type=new_fish_type)  # Pass the random type to respawn
        self.hook.reset()
        
        # Update high score if needed
        if self.boat.caught_fishes > self.json_data["best_result"]:
            self.json_data["best_result"] = self.boat.caught_fishes
            self.score_display.update_high_score(self.json_data["best_result"])
            save_on_close(self.json_data, self.boat.caught_fishes)

    def handle_bomb_collision(self, bomb):
        # Reduce score when hitting a bomb
        current_score = max(0, self.boat.caught_fishes + bomb.points)
        self.boat.caught_fishes = current_score
        self.score_display.update_score(current_score)
        self.score_display.update_fish_count(current_score)
        bomb.respawn()
        self.hook.reset()

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
                        self.boat.x + 90, self.hook.y])
            
            # Reset color to white before drawing sprites
            Color(1, 1, 1, 1)  # White color, full opacity
            
            # Adjust hook position for bigger boat
            Rectangle(texture=self.hook.texture,
                     pos=(self.boat.x + 85, self.hook.y),
                     size=self.hook.size)
            
            # Draw all fish with their proper sizes
            for fish in self.fishes:
                Rectangle(texture=fish.current_texture,
                         pos=(fish.x_pos, fish.y_pos),
                         size=fish.size)  # Use fish's individual size
            
            # Draw bombs after fish
            for bomb in self.bombs:
                Rectangle(texture=bomb.texture,
                         pos=(bomb.x_pos, bomb.y_pos),
                         size=bomb.size)
            
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
