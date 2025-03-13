from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
from kivy.animation import Animation
from kivy.uix.image import Image

class VolumeControlButton(Button):
    def __init__(self, sound_manager, **kwargs):
        super().__init__(**kwargs)
        self.sound_manager = sound_manager
        self.is_muted = False  # สถานะเสียงเริ่มต้นเปิดอยู่

        # กำหนดไอคอนเริ่มต้นเป็น "เปิดเสียง"
        self.icon = Image(source="images/", size=(50, 50))
        self.add_widget(self.icon)

        self.size_hint = (None, None)
        self.size = (80, 80)
        self.pos_hint = {"right": 1, "top": 1}  # วางที่มุมขวาบนของจอ
        self.background_normal = ""  # ลบพื้นหลังปุ่ม
        self.background_color = (0, 0, 0, 0)  # ทำให้ปุ่มโปร่งใส

        self.bind(on_release=self.toggle_sound)

    def toggle_sound(self, instance):
        self.is_muted = not self.is_muted
        if self.is_muted:
            self.sound_manager.stop_music()
            self.icon.source = "images/"  # เปลี่ยนเป็นไอคอนปิดเสียง
        else:
            self.sound_manager.play_music()
            self.icon.source = "images/"  # เปลี่ยนเป็นไอคอนเปิดเสียง
        
        # ทำอนิเมชันตอนกด
        anim = Animation(size=(70, 70), duration=0.1) + Animation(size=(80, 80), duration=0.1)
        anim.start(self)