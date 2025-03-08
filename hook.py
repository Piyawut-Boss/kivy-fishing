import pygame # นำเข้าโมดูล pygame เพื่อใช้สำหรับสร้างเกม
from boat import Boat # นำเข้าคลาส Boat จากไฟล์ boat.py
from fishing_line import FishLine # นำเข้าคลาส FishLine จากไฟล์ fishing_line.py


class Hook: # สร้างคลาส Hook สำหรับใช้เป็นคลาสของเบ็ด
    __DROP_SPEED = 4 # กำหนดความเร็วในการตกของเบ็ด
    __GET_BACK_SPEED = 8 # กำหนดความเร็วในการดึงเบ็ดกลับ
    __CAUGHT_FISH_SPEED = 2 # กำหนดความเร็วในการดึงปลาขึ้นมา

    def __init__(self, boat: Boat): # สร้างเมธอด __init__ สำหรับกำหนดค่าเริ่มต้นของเบ็ด
        self.picture = pygame.image.load("images/hook.png") # โหลดภาพของเบ็ด
        self.picture = pygame.transform.scale(self.picture, (15, 30)) # ปรับขนาดของภาพเบ็ด
        self.y_pos = boat.y + 160 # กำหนดตำแหน่ง y ของเบ็ด
        self.is_hook_moving = False # กำหนดให้เบ็ดไม่ได้เคลื่อนที่
        self.bottom_reached = False # กำหนดให้เบ็ดไม่ได้ตกลงสุด
        self.is_caught = False # กำหนดให้เบ็ดไม่ได้ตกปลา

    def drop_hook(self): # สร้างเมธอด drop_hook สำหรับให้เบ็ดตกลง
        self.y_pos += Hook.__DROP_SPEED # กำหนดให้เบ็ดตกลง
        if self.y_pos >= 700: # ถ้าเบ็ดตกลงสมากกว่าหรือเท่ากับความลึก 700
            self.bottom_reached = True # กำหนดให้เบ็ดตกลงสุด
            self.is_caught = False # กำหนดให้เบ็ดไม่ได้ตกปลา

    def get_hook_back(self, fishing_line: FishLine): # สร้างเมธอด get_hook_back สำหรับดึงเบ็ดกลับ
        if self.y_pos >= fishing_line.advance_line + 60: # ถ้าตำแหน่ง y ของเบ็ดมากกว่าหรือเท่ากับตำแหน่ง y ของเส้นเบ็ด + 60
            self.y_pos -= Hook.__GET_BACK_SPEED # กำหนดให้เบ็ดดึงกลับ
        else:
            self.is_hook_moving = False # กำหนดให้เบ็ดไม่ได้เคลื่อนที่
            self.bottom_reached = False # กำหนดให้เบ็ดไม่ได้ตกลงสุด

    def caught_fish(self, fishing_line: FishLine): # สร้างเมธอด caught_fish สำหรับดึงปลาขึ้นมา
        if self.y_pos >= fishing_line.advance_line + 60: # ถ้าตำแหน่ง y ของเบ็ดมากกว่าหรือเท่ากับตำแหน่ง y ของเส้นเบ็ด + 60
            self.y_pos -= Hook.__CAUGHT_FISH_SPEED # กำหนดให้เบ็ดดึงปลาขึ้นมา
        else:
            self.is_hook_moving = False # กำหนดให้เบ็ดไม่ได้เคลื่อนที่
            self.bottom_reached = False # กำหนดให้เบ็ดไม่ได้ตกลงสุด
            self.is_caught = True # กำหนดให้เบ็ดตกปลา

    def fix_bug_fishing_every_second_time(self): # สร้างเมธอด fix_bug_fishing_every_second_time สำหรับแก้บัคการตกปลาทุกครั้งที่สอง
        if self.y_pos < 210: # ถ้าตำแหน่ง y ของเบ็ดน้อยกว่า 210
            self.is_caught = False # กำหนดให้เบ็ดไม่ได้ตกปลา
