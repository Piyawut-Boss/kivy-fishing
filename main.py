import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.clock import Clock

class Fish(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # เลือกรูปภาพแบบสุ่ม
        fish_images = ["assets/puffer-fish.png", "assets/summer.png", "assets/clown-fish.png"]
        self.source = random.choice(fish_images)
        
        # เลือกความเร็วแบบสุ่ม
        self.speed = random.randint(2, 5)  # ความเร็วระหว่าง 2 ถึง 5
        self.size_hint = (None, None)
        self.size = (100, 50)
        self.x = random.randint(0, 700)  # สุ่มจุดเกิด X
        self.y = random.randint(100, 400)  # สุ่มระดับน้ำ
        self.direction = random.choice([-1, 1])  # สุ่มทิศทาง

        self.flip_horizontal = False  # ค่าเริ่มต้นไม่พลิก

        if self.direction == -1:
            self.x = 700  # ถ้าไปซ้ายให้เริ่มจากขอบขวา
            self.flip_image()

    def move(self):
        self.x += self.speed * self.direction  # ใช้ความเร็วที่สุ่มไว้ในการว่าย

        # เมื่อชนขอบขวา
        if self.x > 700:
            self.direction = -1  # เปลี่ยนทิศทางไปซ้าย
            self.flip_image()  # พลิกภาพ
            return True  # ส่งคืนค่าบอกว่าปลาออกจากจอแล้ว

        # เมื่อชนขอบซ้าย
        if self.x < 0:
            self.direction = 1  # เปลี่ยนทิศทางไปขวา
            self.flip_image()  # พลิกภาพ
            return True  # ส่งคืนค่าบอกว่าปลาออกจากจอแล้ว

        return False  # ถ้ายังไม่ชนขอบ

    def flip_image(self):
        self.flip_horizontal = not self.flip_horizontal  # พลิกภาพ

class FishingGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fishes = [Fish() for _ in range(5)]  # สร้างปลา 5 ตัว
        for fish in self.fishes:
            self.add_widget(fish)

    def update(self, dt):
        for fish in self.fishes[:]:  # ใช้ [:] เพื่อให้สามารถลบปลาได้ในระหว่างการวนลูป
            if fish.move():
                self.remove_widget(fish)  # ลบปลาออกจากหน้าจอเมื่อชนขอบ
                self.fishes.remove(fish)  # ลบปลาจากรายการ
                # สร้างปลาตัวใหม่และเพิ่มเข้าไปในเกม
                new_fish = Fish()
                self.add_widget(new_fish)
                self.fishes.append(new_fish)

class FishingApp(App):
    def build(self):
        game = FishingGame()
        Clock.schedule_interval(game.update, 1.0 / 60.0)  # อัปเดตทุกเฟรม
        return game

if __name__ == "__main__":
    FishingApp().run()
