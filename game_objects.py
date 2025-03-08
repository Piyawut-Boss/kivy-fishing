import pygame # นำเข้าโมดูล pygame เพื่อใช้สำหรับการพัฒนาเกม
from settings import * # นำเข้าค่าคงที่ทั้งหมดจากไฟล์ settings.py
import random # นำเข้าโมดูล random เพื่อใช้สำหรับสุ่มตำแหน่งของปลา

class GameObject: # สร้างคลาส GameObject สำหรับใช้เป็นคลาสหลักของวัตถุในเกม
    def __init__(self, x, y, width, height): # สร้างเมธอด __init__ สำหรับกำหนดค่าเริ่มต้นของวัตถุ
        self.rect = pygame.Rect(x, y, width, height) # กำหนดพื้นที่ของวัตถุด้วยคลาส pygame.Rect
        self.image = None # กำหนดภาพของวัตถุเป็น None
        
    def draw(self, screen): # สร้างเมธอด draw สำหรับวาดวัตถุลงบนหน้าจอ
        if self.image: # ถ้ามีภาพของวัตถุ
            screen.blit(self.image, self.rect) # ให้วาดภาพของวัตถุลงบนหน้าจอ

class Boat(GameObject): # สร้างคลาส Boat สืบทอดคุณสมบัติจากคลาส GameObject
    def __init__(self): # สร้างเมธอด __init__ สำหรับกำหนดค่าเริ่มต้นของเรือ
        super().__init__(SIZE[0]//2, 50, 200, 100) # เรียกใช้เมธอด __init__ ของคลาสแม่และกำหนดตำแหน่งและขน
        self.image = pygame.image.load("images/boat_left.png") # กำหนดภาพของเรือ
        self.speed = BOAT_SPEED # กำหนดความเร็วของเรือ
        
    def update(self): # สร้างเมธอด update สำหรับอัพเดทตำแหน่งของเรือ
        keys = pygame.key.get_pressed() # รับค่าปุ่มที่กดจากคีย์บอร์ด
        if keys[pygame.K_LEFT]: self.rect.x -= self.speed # ถ้ากดปุ่มลูกศรซ้ายให้เรือเคลื่อนที่ไปทางซ้าย
        if keys[pygame.K_RIGHT]: self.rect.x += self.speed # ถ้ากดปุ่มลูกศรขวาให้เรือเคลื่อนที่ไปทางขวา
        self.rect.clamp_ip(pygame.display.get_surface().get_rect()) # กำหนดให้เรืออยู่ในขอบเขตของหน้าจอ

class Fish(GameObject): # สร้างคลาส Fish สืบทอดคุณสมบัติจากคลาส GameObject
    def __init__(self): # สร้างเมธอด __init__ สำหรับกำหนดค่าเริ่มต้นของปลา
        x = random.randrange(100, SIZE[0]-100) # สุ่มตำแหน่ง x ของปลา
        y = random.randrange(300, SIZE[1]-100) # สุ่มตำแหน่ง y ของปลา
        super().__init__(x, y, 80, 50) # เรียกใช้เมธอด __init__ ของคลาสแม่และกำหนดตำแหน่งและขน
        self.speed = FISH_SPEED # กำหนดความเร็วของปลา
        self.direction = 1 # กำหนดทิศทางของปลา
        self.load_images() # เรียกใช้เมธอด load_images เพื่อโหลดภาพของปลา
        
    def load_images(self): # สร้างเมธอด load_images สำหรับโหลดภาพของปลา
        self.images = { # สร้างดิกชันนารีเพื่อเก็บภาพของปลา
            'left': pygame.image.load("images/fish_1_left.png"), # กำหนดภาพของปลาเมื่อเคลื่อนที่ไปทางซ้าย
            'right': pygame.image.load("images/fish_1_right.png") # กำหนดภาพของปลาเมื่อเคลื่อนที่ไปทางขวา
        }
        self.image = self.images['right'] # กำหนดภาพเริ่มต้นของปลาเป็นภาพของปลาเมื่อเคลื่อนที่ไปทางขวา
        
    def update(self): # สร้างเมธอด update สำหรับอัพเดทตำแหน่งของปลา
        self.rect.x += self.speed * self.direction # กำหนดให้ปลาเคลื่อนที่ไปทางทิศทางที่กำหนด
        if self.rect.left < 0 or self.rect.right > SIZE[0]: # ถ้าปลาชนขอบของหน้าจอ
            self.direction *= -1 # กำหนดให้ปลาเปลี่ยนทิศทาง
            self.image = self.images['right' if self.direction > 0 else 'left'] # กำหนดให้ภาพของปลาเปลี่ยนตามทิศทางที่กำหนด

class Hook(GameObject): # สร้างคลาส Hook สืบทอดคุณสมบัติจากคลาส GameObject
    def __init__(self, boat): # สร้างเมธอด __init__ สำหรับกำหนดค่าเริ่มต้นของเบ็ด
        super().__init__(boat.rect.centerx, boat.rect.bottom, 15, 30) # เรียกใช้เมธอด __init__ ของคลาสแม่และกำหนดตำแหน่งและขน
        self.image = pygame.image.load("images/hook.png") # กำหนดภาพของเบ็ด
        self.boat = boat # กำหนดเรือที่เป็นเจ้าของของเบ็ด
        self.is_fishing = False # กำหนดให้เบ็ดไม่ได้ตกปลา
        self.speed = HOOK_SPEED # กำหนดความเร็วของเบ็ด
        
    def start_fishing(self): # สร้างเมธอด start_fishing สำหรับให้เบ็ดตกปลา
        self.is_fishing = True # กำหนดให้เบ็ดตกปลา
        
    def update(self): # สร้างเมธอด update สำหรับอัพเดทตำแหน่งของเบ็ด
        if self.is_fishing: # ถ้าเบ็ดตกปลา
            self.rect.y += self.speed # กำหนดให้เบ็ดตกลง
            if self.rect.bottom > SIZE[1]: # ถ้าเบ็ดชนขอบล่างของหน้าจอ
                self.speed = -self.speed # กำหนดให้เบ็ดเคลื่อนที่ขึ้น
            elif self.rect.top < self.boat.rect.bottom: # ถ้าเบ็ดชนกับเรือ
                self.is_fishing = False # กำหนดให้เบ็ดไม่ได้ตกปลา
                self.speed = abs(self.speed) # กำหนดให้ความเร็วเป็นบวก
