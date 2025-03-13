from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.animation import Animation

class VolumeControlButton(ButtonBehavior, Image):
    def __init__(self, sound_manager, **kwargs):
        super().__init__(**kwargs)
        self.sound_manager = sound_manager
        self.is_muted = False  # เริ่มต้นเปิดเสียง

        # ตั้งค่าไอคอนเริ่มต้น
        self.source = "images/icons8-voice-100.png"
        self.size_hint = (None, None)
        self.size = (80, 80)
        self.pos_hint = {"left": 0, "bottom": 0}  # ตำแหน่งมุมขวาบน
        self.allow_stretch = True  # ให้รูปยืดได้
        self.keep_ratio = False  # ป้องกันการผิดสัดส่วน

    def on_touch_down(self, touch):
        """ ตรวจสอบว่าคลิกอยู่บนปุ่มหรือไม่ """
        if self.collide_point(*touch.pos):  # ถ้าคลิกอยู่บนปุ่ม
            self.toggle_sound()
            return True
        return super().on_touch_down(touch)

    def toggle_sound(self):
        self.is_muted = not self.is_muted
        if self.is_muted:
            self.sound_manager.stop_music()
            self.source = "images/icons8-mute-100.png"  # เปลี่ยนเป็นไอคอนปิดเสียง
        else:
            self.sound_manager.play_music()
            self.source = "images/icons8-voice-100.png"  # เปลี่ยนเป็นไอคอนเปิดเสียง
        
        # ทำอนิเมชันตอนกด
        anim = Animation(size=(70, 70), duration=0.1) + Animation(size=(80, 80), duration=0.1)
        anim.start(self)