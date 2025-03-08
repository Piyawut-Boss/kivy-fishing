import pygame # นำเข้าโมดูล pygame
import random # นำเข้าโมดูล random
from config import GameConfig as cfg # นำเข้าค่าคงที่จากไฟล์ config.py

class GameObject: # สร้างคลาส GameObject
    def __init__(self, image_path, size): # สร้างเมธอด __init__ สำหรับกำหนดค่าเริ่มต้นของคลาส
        self.image = pygame.image.load(image_path) # โหลดภาพ
        self.image = pygame.transform.scale(self.image, size) # ปรับขนาดภาพ
        self.rect = self.image.get_rect() # สร้างสี่เหลี่ยมผืนผ้าของภาพ
        
    def draw(self, screen): # สร้างเมธอด draw สำหรับวาดภาพลงบนหน้าจอ
        screen.blit(self.image, self.rect) # วาดภาพลงบนหน้าจอ

class Boat(GameObject): # สร้างคลาส Boat สืบทอดจาก GameObject
    def __init__(self): # สร้างเมธอด __init__ สำหรับกำหนดค่าเริ่มต้นของคลาส
        super().__init__("images/boat_left.png", (200, 100)) # เรียกใช้เมธอด __init__ ของคลาสแม่
        self.rect.centerx = cfg.WINDOW_SIZE[0] // 2 # กำหนดตำแหน่งแนวนอนของเรือ
        self.rect.bottom = 150 # กำหนดตำแหน่งแนวตั้งของเรือ
        
    def update(self, keys): # สร้างเมธอด update สำหรับอัพเดทตำแหน่งของเรือ
        if keys[pygame.K_LEFT]: self.rect.x -= cfg.BOAT_SPEED # ถ้ากดปุ่มลูกศรซ้าย
        if keys[pygame.K_RIGHT]: self.rect.x += cfg.BOAT_SPEED # ถ้ากดปุ่มลูกศรขวา
        self.rect.clamp_ip(pygame.display.get_surface().get_rect()) # กำหนดให้เรืออยู่ในขอบเขตของหน้าจอ

class Fish(GameObject): # สร้างคลาส Fish สืบทอดจาก GameObject
    def __init__(self): # สร้างเมธอด __init__ สำหรับกำหนดค่าเริ่มต้นของคลาส
        super().__init__("images/fish_1_left.png", (80, 50)) # เรียกใช้เมธอด __init__ ของคลาสแม่
        self.speed = cfg.FISH_SPEED # กำหนดความเร็วของปลา
        self.direction = 1 # กำหนดทิศทางของปลา
        self.respawn() # สร้างฟังก์ชัน respawn
        
    def update(self): # สร้างเมธอด update สำหรับอัพเดทตำแหน่งของปลา
        self.rect.x += self.speed * self.direction # กำหนดตำแหน่งแนวนอนของปลา
        if self.rect.right > cfg.WINDOW_SIZE[0] or self.rect.left < 0: # ถ้าปลาชนขอบหน้าจอ
            self.direction *= -1 # กลับทิศทาง
            self.image = pygame.transform.flip(self.image, True, False) # กลับทิศทางของภาพ
            
    def respawn(self): # สร้างเมธอด respawn สำหรับกำหนดตำแหน่งเริ่มต้นของปลา
        self.rect.x = random.randrange(cfg.WINDOW_SIZE[0] - self.rect.width) # กำหนดตำแหน่งแนวนอนของปลา
        self.rect.y = random.randrange(300, cfg.WINDOW_SIZE[1] - 100) # กำหนดตำแหน่งแนวตั้งของปลา

class Hook(GameObject): # สร้างคลาส Hook สืบทอดจาก GameObject
    def __init__(self, boat): # สร้างเมธอด __init__ สำหรับกำหนดค่าเริ่มต้นของคลาส
        super().__init__("images/hook.png", (15, 30)) # เรียกใช้เมธอด __init__ ของคลาสแม่
        self.boat = boat # กำหนดเรือ
        self.is_fishing = False # กำหนดว่ากำลังจะตกปลาหรือไม่
        self.reset() # สร้างฟังก์ชัน reset
        
    def reset(self): # สร้างเมธอด reset สำหรับกำหนดตำแหน่งเริ่มต้นของเบ็ด
        self.rect.centerx = self.boat.rect.centerx # กำหนดตำแหน่งแนวนอนของเบ็ด
        self.rect.top = self.boat.rect.bottom # กำหนดตำแหน่งแนวตั้งของเบ็ด
        
    def start_fishing(self): # สร้างเมธอด start_fishing สำหรับเริ่มตกปลา
        self.is_fishing = True # กำหนดว่ากำลังตกปลา
        
    def update(self, boat): # สร้างเมธอด update สำหรับอัพเดทตำแหน่งของเบ็ด
        if not self.is_fishing: # ถ้าไม่ได้ตกปลา
            self.rect.centerx = boat.rect.centerx # กำหนดตำแหน่งแนวนอนของเบ็ด
        else: # ถ้าตกปลา
            self.rect.y += cfg.HOOK_SPEED # กำหนดตำแหน่งแนวตั้งของเบ็ด
            if self.rect.bottom > cfg.MAX_DEPTH: # ถ้าเบ็ดตกลงไปเกินลึกสุด
                self.is_fishing = False # หยุดตกปลา
                self.reset() # กลับไปตำแหน่งเริ่มต้น
