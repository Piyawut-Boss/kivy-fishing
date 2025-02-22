import random
import math
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.clock import Clock
from kivy.graphics import Scale, PushMatrix, PopMatrix
from kivy.core.window import Window  # ใช้ขนาดหน้าจอ
from kivy.uix.floatlayout import FloatLayout

class Hook(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = "assets/hook.png"  # Add a hook.png to your assets folder
        self.size_hint = (None, None)
        self.size = (50, 50)
        Window.bind(mouse_pos=self.on_mouse_move)

    def on_mouse_move(self, window, pos):
        self.pos = pos

class Fish(Image):
    def __init__(self, fish_type, **kwargs):
        # Set attributes before super().__init__
        self._direction = random.choice([-1, 1])
        self._flipped = False
        
        super().__init__(**kwargs)
        
        fish_data = {
            "puffer-fish": {
                "image": "assets/puffer-fish.png",
                "speed": random.randint(2, 3),
                "spawn_rate": 5,
                "points": 10,
                "movement": "zigzag"
            },
            "summer": {
                "image": "assets/summer.png",
                "speed": random.randint(6, 8),
                "spawn_rate": 1,
                "points": 30,
                "movement": "straight"
            },
            "clown-fish": {
                "image": "assets/clown-fish.png",
                "speed": random.randint(3, 4),
                "spawn_rate": 5,
                "points": 20,
                "movement": "wave"
            }
        }
        
        self.source = fish_data[fish_type]["image"]
        self.speed = fish_data[fish_type]["speed"]
        self.spawn_rate = fish_data[fish_type]["spawn_rate"]
        self.points = fish_data[fish_type]["points"]
        self.movement_type = fish_data[fish_type]["movement"]
        self.size_hint = (None, None)
        self.size = (150, 75)
        
        # Movement variables
        self.original_y = random.randint(100, Window.height - 100)
        self.y = self.original_y
        self.time = random.random() * 10
        self.amplitude = random.randint(30, 70)
        self.frequency = random.random() * 0.1
        
        # Add new movement variables
        self.current_speed = 0
        self.target_speed = self.speed
        self.acceleration = random.uniform(0.1, 0.2)
        self.turn_cooldown = 0
        self.direction_change_chance = 0.005  # 0.5% chance per frame
        self.vertical_speed = 0
        self.max_vertical_speed = 3
        self.vertical_acceleration = 0.1
        
        # Customize movement parameters based on fish type
        if fish_type == "puffer-fish":
            self.direction_change_chance = 0.01  # More erratic movement
            self.max_vertical_speed = 2  # Slower vertical movement
        elif fish_type == "summer":
            self.direction_change_chance = 0.002  # More direct movement
            self.acceleration = random.uniform(0.2, 0.3)  # Faster acceleration
        elif fish_type == "clown-fish":
            self.amplitude *= 1.5  # Larger wave pattern
            self.frequency *= 1.2  # Faster oscillation
        
        # Starting position
        if self._direction == 1:
            self.x = -self.width
        else:
            self.x = Window.width
            with self.canvas.before:
                PushMatrix()
                Scale(x=-1, y=1, origin=self.center)
                PopMatrix()

    def move(self):
        # Smooth acceleration
        speed_diff = self.target_speed - self.current_speed
        self.current_speed += speed_diff * self.acceleration
        
        # Basic movement
        self.x += self.current_speed * self._direction
        
        # Movement patterns
        if self.movement_type == "zigzag":
            if self.turn_cooldown <= 0:
                if random.random() < self.direction_change_chance:
                    self.vertical_speed = random.choice([-1, 1]) * self.max_vertical_speed
                    self.turn_cooldown = random.randint(30, 60)  # Frames until next turn
            else:
                self.turn_cooldown -= 1
            
            # Smooth vertical movement
            self.y += self.vertical_speed
            
            # Gradually return to center
            if abs(self.y - self.original_y) > 100:
                self.vertical_speed += (self.original_y - self.y) * 0.01
                
        elif self.movement_type == "wave":
            self.time += self.frequency
            target_y = self.original_y + math.sin(self.time) * self.amplitude
            self.y += (target_y - self.y) * 0.1  # Smooth transition
            
        elif self.movement_type == "straight":
            if random.random() < self.direction_change_chance * 0.5:  # Less frequent changes
                self.vertical_speed = random.uniform(-1, 1)
            self.y += self.vertical_speed
            self.vertical_speed *= 0.95  # Dampen vertical movement
        
        # Keep fish within bounds with smooth correction
        if self.y < 50:
            self.vertical_speed = abs(self.vertical_speed)
        elif self.y > Window.height - 50:
            self.vertical_speed = -abs(self.vertical_speed)
        
        # Screen bounds check
        if self.x > Window.width + self.width or self.x < -self.width:
            return True
        return False

class FishingGame(FloatLayout):  # Changed from RelativeLayout to FloatLayout
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Fix background for full screen
        self.background = Image(
            source="assets/background.png",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={'center_x': .5, 'center_y': .5}
        )
        
        # Add background first
        self.add_widget(self.background)
        
        # Bind size to update background
        self.bind(size=self._update_background)
        
        # Add hook
        self.hook = Hook()
        self.add_widget(self.hook)
        
        # Add score
        self.score = 0
        self.score_label = Label(
            text=f"Score: {self.score}",
            pos_hint={'right': 0.95, 'top': 0.95},
            size_hint=(None, None)
        )
        self.add_widget(self.score_label)
        
        # Create fish
        self.fishes = []
        self.spawn_initial_fish()
        
        # Bind click event
        self.bind(on_touch_down=self.on_click)

    def spawn_initial_fish(self):
        fish_types = ["puffer-fish", "summer", "clown-fish"]
        weights = [5, 1, 5]  # Spawn rates as weights
        for _ in range(10):
            fish_type = random.choices(fish_types, weights=weights)[0]
            fish = Fish(fish_type)
            self.fishes.append(fish)
            self.add_widget(fish)

    def on_click(self, instance, touch):
        for fish in self.fishes[:]:  # Use copy of list to avoid modification during iteration
            if self.check_collision(self.hook, fish):
                self.catch_fish(fish)

    def check_collision(self, hook, fish):
        return (hook.x < fish.x + fish.width and
                hook.x + hook.width > fish.x and
                hook.y < fish.y + fish.height and
                hook.y + hook.height > fish.y)

    def catch_fish(self, fish):
        self.score += fish.points
        self.score_label.text = f"Score: {self.score}"
        self.remove_widget(fish)
        self.fishes.remove(fish)
        
        # Spawn new fish
        fish_types = ["puffer-fish", "summer", "clown-fish"]
        new_fish = Fish(random.choice(fish_types))
        self.add_widget(new_fish)
        self.fishes.append(new_fish)

    def update(self, dt):
        for fish in self.fishes[:]:  
            if fish.move():
                self.remove_widget(fish)  
                self.fishes.remove(fish)  
                
                # Weighted random spawn of new fish
                fish_types = ["puffer-fish", "summer", "clown-fish"]
                weights = [5, 1, 5]
                fish_type = random.choices(fish_types, weights=weights)[0]
                new_fish = Fish(fish_type)
                self.add_widget(new_fish)
                self.fishes.append(new_fish)

    def _update_background(self, *args):
        """Update background size to match window"""
        if hasattr(self, 'background'):
            self.background.size = self.size
            self.background.pos = self.pos

class FishingApp(App):
    def build(self):
        Window.clearcolor = (0, 0, 0, 1)  # Set black background color
        game = FishingGame()
        Clock.schedule_interval(game.update, 1.0 / 60.0)  
        return game

if __name__ == "__main__":
    FishingApp().run()