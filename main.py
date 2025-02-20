import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.clock import Clock
from kivy.graphics import Scale
from kivy.core.window import Window  # ใช้ขนาดหน้าจอ

class Fish(Image):
    def __init__(self, fish_type, **kwargs):
        super().__init__(**kwargs)
        
        # เลือกรูปภาพปลาและกำหนดค่าความเร็วและอัตราการเกิดตามประเภทปลา
        fish_data = {
            "puffer-fish": {"image": "assets/puffer-fish.png", "speed": random.randint(3, 4), "spawn_rate": 5},
            "summer": {"image": "assets/summer.png", "speed": random.randint(8, 9), "spawn_rate": 1},
            "clown-fish": {"image": "assets/clown-fish.png", "speed": random.randint(3, 4), "spawn_rate": 5}
        }
        
        self.source = fish_data[fish_type]["image"]
        self.speed = fish_data[fish_type]["speed"]  # ความเร็ว
        self.spawn_rate = fish_data[fish_type]["spawn_rate"]  # อัตราการเกิด
        self.size_hint = (None, None)
        self.size = (100, 50)
        
        # กำหนดตำแหน่งเริ่มต้นแบบสุ่ม
        self.y = random.randint(100, 400)
        self.direction = random.choice([-1, 1])  # เลือกไปซ้าย (-1) หรือไปขวา (1)

        # กำหนดค่าเริ่มต้นสำหรับการพลิกภาพ
        self.flip_horizontal = False  # กำหนดให้เป็น False เริ่มต้น (ไม่พลิก)
        
        if self.direction == 1:
            self.x = -self.width  # เริ่มต้นที่ขอบซ้ายของหน้าจอ (ปลาจะว่ายเข้ามาจากซ้าย)
        else:
            self.x = Window.width  # เริ่มต้นที่ขอบขวาที่สุด (ใช้ Window.width)
            self.flip_image()  # พลิกภาพหากเริ่มจากขวา

    def move(self):
        self.x += self.speed * self.direction  

        # เมื่อปลาออกจากขอบหน้าจอด้านขวา
        if self.x > Window.width:  # ขอบขวาของหน้าจอ
            self.direction = -1
            self.flip_image()
            return True  

        # เมื่อปลาออกจากขอบหน้าจอด้านซ้าย
        if self.x < -self.width:  # ขอบซ้ายของหน้าจอ
            self.direction = 1
            self.flip_image()
            return True  

        return False  

    def flip_image(self):
        self.flip_horizontal = not self.flip_horizontal  # พลิกภาพ

        # ลบการแปลงการพลิกเดิมออก
        self.canvas.before.clear()

        # ถ้าพลิกภาพ
        if self.flip_horizontal:
            # เพิ่มการพลิกภาพตามแนวนอน (แกน X)
            scale = Scale(x=-1, y=1, origin=self.center)
            self.canvas.before.add(scale)

class FishingGame(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # ตั้งค่าพื้นหลัง
        self.background = Image(source="assets/background.png", allow_stretch=True, keep_ratio=False)
        self.add_widget(self.background)

        # สร้างปลา 5 ตัวเริ่มต้นจากชนิดสุ่ม
        fish_types = ["puffer-fish", "summer", "clown-fish"]
        self.fishes = [Fish(random.choice(fish_types)) for _ in range(10)]
        for fish in self.fishes:
            self.add_widget(fish)

    def update(self, dt):
        for fish in self.fishes[:]:  
            if fish.move():
                self.remove_widget(fish)  
                self.fishes.remove(fish)  
                
                # เพิ่มปลาตัวใหม่ที่ชนิดสุ่มตามอัตราการเกิด
                fish_types = ["puffer-fish", "summer", "clown-fish"]
                fish_type = random.choice(fish_types)
                new_fish = Fish(fish_type)
                self.add_widget(new_fish)
                self.fishes.append(new_fish)

class FishingApp(App):
    def build(self):
        game = FishingGame()
        Clock.schedule_interval(game.update, 1.0 / 60.0)  
        return game

if __name__ == "__main__":
    FishingApp().run()
