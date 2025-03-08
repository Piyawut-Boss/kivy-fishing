from boat import Boat # นำเข้าโมดูล Boat จากไฟล์ boat.py

class FishLine: # สร้างคลาส FishLine สำหรับจัดการสายเบ็ดตกปลา

    def __init__(self, boat: Boat): # กำหนดพารามิเตอร์ boat เป็นอ็อบเจกต์ Boat
        self.boat = boat  # เก็บอ้างอิงถึงเรือ
        self.update_tip_of_the_rod()  # ตั้งค่าปลายคันเบ็ดตามทิศทางเรือ
        self.advance_line = 150 # ความยาวของสายเบ็ด

    def update_tip_of_the_rod(self): # สร้างเมธอด update_tip_of_the_rod สำหรับอัปเดตตำแหน่งปลายคันเบ็ด
        """อัปเดตตำแหน่งปลายคันเบ็ดตามทิศทางเรือ"""
        if self.boat.direction == "right": #ถ้าเรือไปทางขวา
            self.tip_of_the_rod = self.boat.x + 210 # ตำแหน่งปลายคันเบ็ดอยู่ทางขวาของเรือ
        else:
            self.tip_of_the_rod = self.boat.x + 35 # ตำแหน่งปลายคันเบ็ดอยู่ทางซ้ายของเรือ

    def rotate_fisherman_right(self): # สร้างเมธอด rotate_fisherman_right สำหรับหมุนตัวลูกเบ็ดไปทางขวา
        self.boat.direction = "right" # ตั้งค่าทิศทางของเรือเป็นขวา
        self.update_tip_of_the_rod() # อัปเดตตำแหน่งปลายคันเบ็ด

    def rotate_fisherman_left(self): # สร้างเมธอด rotate_fisherman_left สำหรับหมุนตัวลูกเบ็ดไปทางซ้าย
        self.boat.direction = "left" # ตั้งค่าทิศทางของเรือเป็นซ้าย
        self.update_tip_of_the_rod() # อัปเดตตำแหน่งปลายคันเบ็ด
