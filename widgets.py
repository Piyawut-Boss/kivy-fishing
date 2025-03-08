import pygame

class Widget: # สร้างคลาส Widget
    def __init__(self, x, y, width, height): # สร้างเมธอด __init__ สำหรับกำหนดค่าเริ่มต้นของคลาส
        self.rect = pygame.Rect(x, y, width, height) # สร้างสี่เหลี่ยมผืนผ้าของ Widget
        self.visible = True # กำหนดให้เป็นจริง
    
    def draw(self, screen): # สร้างเมธอด draw สำหรับวาด Widget ลงบนหน้าจอ
        pass # ไม่ต้องทำอะไรเพราะเป็นคลาสแม่

class Button(Widget): # สร้างคลาส Button สืบทอดจาก Widget
    def __init__(self, x, y, width, height, text, color, hover_color): # สร้างเมธอด __init__ สำหรับกำหนดค่าเริ่มต้นของคลาส
        super().__init__(x, y, width, height) # เรียกใช้เมธอด __init__ ของคลาสแม่
        self.text = text # กำหนดข้อความ
        self.color = color # กำหนดสี
        self.hover_color = hover_color # กำหนดสีเมื่อชี้
        self.font = pygame.font.Font(None, 36) # กำหนดฟอนต์
        self.is_hovered = False # กำหนดว่าชี้หรือไม่

    def draw(self, screen): # สร้างเมธอด draw สำหรับวาดปุ่มลงบนหน้าจอ
        if not self.visible: # ถ้าไม่แสดง
            return
        color = self.hover_color if self.is_hovered else self.color # กำหนดสีของปุ่ม
        pygame.draw.rect(screen, color, self.rect) # วาดสี่เหลี่ยมผืนผ้าของปุ่ม
        text_surface = self.font.render(self.text, True, (255, 255, 255)) # สร้างข้อความ
        text_rect = text_surface.get_rect(center=self.rect.center) # กำหนดตำแหน่งของข้อความ
        screen.blit(text_surface, text_rect) # วาดข้อความลงบนหน้าจอ

class TextLabel(Widget): # สร้างคลาส TextLabel สืบทอดจาก Widget
    def __init__(self, x, y, text, color, font_size=30): # สร้างเมธอด __init__ สำหรับกำหนดค่าเริ่มต้นของคลาส
        super().__init__(x, y, 0, 0) # เรียกใช้เมธอด __init__ ของคลาสแม่
        self.text = text # กำหนดข้อความ
        self.color = color # กำหนดสี
        self.font = pygame.font.Font(None, font_size) # กำหนดฟอนต์
        self.update_text(text) # สร้างฟังก์ชัน update_text

    def update_text(self, new_text): # สร้างเมธอด update_text สำหรับอัพเดทข้อความ
        self.text = new_text # กำหนดข้อความ
        text_surface = self.font.render(self.text, True, self.color) # สร้างข้อความ
        self.rect.size = text_surface.get_size() # กำหนดขนาดของข้อความ
 
    def draw(self, screen): # สร้างเมธอด draw สำหรับวาดข้อความลงบนหน้าจอ
        if not self.visible: # ถ้าไม่แสดง
            return
        text_surface = self.font.render(self.text, True, self.color) # สร้างข้อความ
        screen.blit(text_surface, self.rect) # วาดข้อความลงบนหน้าจอ

class SpriteWidget(Widget): # สร้างคลาส SpriteWidget สืบทอดจาก Widget
    """Base class for all game sprites""" # คำอธิบายคลาส
    def __init__(self, x, y, width, height): # สร้างเมธอด __init__ สำหรับกำหนดค่าเริ่มต้นของคลาส
        super().__init__(x, y, width, height) # เรียกใช้เมธอด __init__ ของคลาสแม่
        self.hitbox = pygame.Rect(x, y, width, height) # สร้าง hitbox

    def update_hitbox(self, x, y): # สร้างเมธอด update_hitbox สำหรับอัพเดท hitbox
        self.hitbox.x = x # กำหนดตำแหน่งแนวนอนของ hitbox
        self.hitbox.y = y # กำหนดตำแหน่งแนวตั้งของ hitbox

class BoatWidget(SpriteWidget): # สร้างคลาส BoatWidget สืบทอดจาก SpriteWidget
    def __init__(self, boat): # สร้างเมธอด __init__ สำหรับกำหนดค่าเริ่มต้นของคลาส
        super().__init__(boat.x, boat.y, 200, 100) # เรียกใช้เมธอด __init__ ของคลาสแม่
        self.boat = boat
        self.left_image, self.right_image = boat.load_boat() # โหลดภาพเรือ
        self.current_image = self.left_image # กำหนดภาพเริ่มต้น

    def draw(self, screen): # สร้างเมธอด draw สำหรับวาดเรือลงบนหน้าจอ 
        screen.blit(self.current_image, (self.boat.x, self.boat.y)) # วาดภาพเรือลงบนหน้าจอ
        
    def update(self, facing_left): # สร้างเมธอด update สำหรับอัพเดทตำแหน่งของเรือ
        self.current_image = self.left_image if facing_left else self.right_image # กำหนดภาพของเรือ
        self.update_hitbox(self.boat.x, self.boat.y) # อัพเดท hitbox

class FishWidget(SpriteWidget): # สร้างคลาส FishWidget สืบทอดจาก SpriteWidget
    def __init__(self, fish): # สร้างเมธอด __init__ สำหรับกำหนดค่าเริ่มต้นของคลาส
        super().__init__(fish.x_pos, fish.y_pos, 80, 50) # เรียกใช้เมธอด __init__ ของคลาสแม่
        self.fish = fish # กำหนดปลา
        self.left_image, self.right_image = fish.load_pictures() # โหลดภาพปลา
        self.current_image = self.left_image    # กำหนดภาพเริ่มต้น
        
    def draw(self, screen): # สร้างเมธอด draw สำหรับวาดปลาลงบนหน้าจอ
        screen.blit(self.current_image, (self.fish.x_pos, self.fish.y_pos)) # วาดภาพปลาลงบนหน้าจอ
        
    def update(self, direction): # สร้างเมธอด update สำหรับอัพเดทตำแหน่งของปลา
        self.current_image = self.left_image if direction == 'left' else self.right_image # กำหนดภาพของปลา
        self.update_hitbox(self.fish.x_pos, self.fish.y_pos + 27)  # Adjust hitbox position

class HookLineWidget(Widget): # สร้างคลาส HookLineWidget สืบทอดจาก Widget
    def __init__(self, fishing_line, hook): # สร้างเมธอด __init__ สำหรับกำหนดค่าเริ่มต้นของคลาส
        super().__init__(0, 0, 1, 1) # เรียกใช้เมธอด __init__ ของคลาสแม่
        self.fishing_line = fishing_line # กำหนดเส้นเบ็ด
        self.hook = hook # กำหนดเบ็ด
        self.color = (255, 0, 0) # กำหนดสี
        
    def draw(self, screen, boat_y): # สร้างเมธอด draw สำหรับวาดเส้นเบ็ดลงบนหน้าจอ
        start_pos = (self.fishing_line.tip_of_the_rod, boat_y + 17) # กำหนดจุดเริ่มต้น
        end_pos = (self.fishing_line.tip_of_the_rod, self.hook.y_pos)   # กำหนดจุดสิ้นสุด
        pygame.draw.line(screen, self.color, start_pos, end_pos) # วาดเส้นเบ็ด

class CaughtFishWidget(Widget): # สร้างคลาส CaughtFishWidget สืบทอดจาก Widget
    def __init__(self): # สร้างเมธอด __init__ สำหรับกำหนดค่าเริ่มต้นของคลาส
        super().__init__(0, 0, 80, 50) # เรียกใช้เมธอด __init__ ของคลาสแม่
        self.image = pygame.image.load("images/fish_1_left.png") # โหลดภาพปลา
        self.image = pygame.transform.scale(self.image, (80, 50)) # ปรับขนาดภาพ
        self.image = pygame.transform.rotate(self.image, -90) # หมุนภาพ
        
    def draw(self, screen, x, y): # สร้างเมธอด draw สำหรับวาดปลาที่ตกลงบนหน้าจอ
        screen.blit(self.image, (x - 23, y + 20)) # วาดภาพปลาลงบนหน้าจอ

class FishingLineWidget(Widget): # สร้างคลาส FishingLineWidget สืบทอดจาก Widget
    def __init__(self, fishing_line, color=(255, 0, 0)): # สร้างเมธอด __init__ สำหรับกำหนดค่าเริ่มต้นของคลาส
        super().__init__(0, 0, 1, 1) # เรียกใช้เมธอด __init__ ของคลาสแม่
        self.fishing_line = fishing_line # กำหนดเส้นเบ็ด
        self.color = color # กำหนดสี
        
    def draw(self, screen, start_y, end_y): # สร้างเมธอด draw สำหรับวาดเส้นเบ็ดลงบนหน้าจอ
        pygame.draw.line(screen, self.color,  # วาดเส้นเบ็ด
                        (self.fishing_line.tip_of_the_rod, start_y), # จุดเริ่มต้น
                        (self.fishing_line.tip_of_the_rod, end_y)) # จุดสิ้นสุด

class HookWidget(Widget): # สร้างคลาส HookWidget สืบทอดจาก Widget
    def __init__(self, hook): # สร้างเมธอด __init__ สำหรับกำหนดค่าเริ่มต้นของคลาส
        super().__init__(0, hook.y_pos, 15, 30) # เรียกใช้เมธอด __init__ ของคลาสแม่
        self.hook = hook # กำหนดเบ็ด
        self.image = hook.picture # กำหนดภาพเบ็ด
        
    def draw(self, screen, x_pos): # สร้างเมธอด draw สำหรับวาดเบ็ดลงบนหน้าจอ
        screen.blit(self.image, (x_pos, self.hook.y_pos)) # วาดภาพเบ็ดลงบนหน้าจอ

class GameOverWidget(Widget): # สร้างคลาส GameOverWidget สืบทอดจาก Widget
    def __init__(self, screen_size): # สร้างเมธอด __init__ สำหรับกำหนดค่าเริ่มต้นของคลาส
        super().__init__(0, 0, screen_size[0], screen_size[1]) # เรียกใช้เมธอด __init__ ของคลาสแม่
        self.overlay = pygame.Surface(screen_size) # สร้างพื้นที่สำหรับแสดงข้อความ
        self.overlay.set_alpha(128) # กำหนดความโปร่งแสง
        self.overlay.fill((0, 0, 0)) # กำหนดสีพื้นหลัง
        self.text = TextLabel(screen_size[0]//2 - 150, screen_size[1]//2,  # กำหนดข้อความ
                            "Game Over! You Win!", (255, 0, 0), 48) # กำหนดสีและขนาดฟอนต์
        
    def draw(self, screen): # สร้างเมธอด draw สำหรับวาดข้อความ Game Over
        screen.blit(self.overlay, (0, 0)) # วาดพื้นที่สำหรับข้อความ
        self.text.draw(screen) # วาดข้อความ

class GameHUD: # สร้างคลาส GameHUD
    def __init__(self): # สร้างเมธอด __init__ สำหรับกำหนดค่าเริ่มต้นของคลาส
        self.fish_counter = TextLabel(10, 10, "Fish: 0", (255, 255, 255)) # กำหนดข้อความจำนวนปลา
        self.record_label = TextLabel(160, 10, "Record: 0", (255, 255, 255)) # กำหนดข้อความคะแนนสูงสุด
        self.time_label = TextLabel(310, 10, "Time: 0s", (255, 255, 255)) # กำหนดข้อความเวลา
        
    def update(self, fish_count, record, time): # สร้างเมธอด update สำหรับอัพเดทข้อความ
        self.fish_counter.update_text(f"Fish: {fish_count}") # อัพเดทข้อความจำนวนปลา
        self.record_label.update_text(f"Record: {record}") # อัพเดทข้อความคะแนนสูงสุด
        self.time_label.update_text(f"Time: {time}s") # อัพเดทข้อความเวลา
        
    def draw(self, screen): # สร้างเมธอด draw สำหรับวาดข้อความลงบนหน้าจอ
        self.fish_counter.draw(screen) # วาดข้อความจำนวนปลา
        self.record_label.draw(screen) # วาดข้อความคะแนนสูงสุด
        self.time_label.draw(screen) # วาดข้อความเวลา

class DepthMeterWidget(Widget): # สร้างคลาส DepthMeterWidget สืบทอดจาก Widget
    def __init__(self, x, y, height): # สร้างเมธอด __init__ สำหรับกำหนดค่าเริ่มต้นของคลาส
        super().__init__(x, y, 30, height) # เรียกใช้เมธอด __init__ ของคลาสแม่
        self.max_depth = 700 # กำหนดความลึกสูงสุด
        self.current_depth = 0 # กำหนดความลึกปัจจุบัน
        self.color = (0, 191, 255) # กำหนดสี
        
    def update(self, hook_depth): # สร้างเมธอด update สำหรับอัพเดทความลึก
        self.current_depth = hook_depth # กำหนดความลึกปัจจุบัน
        
    def draw(self, screen): # สร้างเมธอด draw สำหรับวาด Depth Meter
        # Draw depth meter background
        pygame.draw.rect(screen, (100, 100, 100), self.rect) # วาดพื้นหลังของ Depth Meter
        # Draw current depth indicator 
        depth_height = (self.current_depth / self.max_depth) * self.rect.height # คำนวณความสูงของความลึก
        pygame.draw.rect(screen, self.color,  # วาดความลึก
                        (self.rect.x, self.rect.y + self.rect.height - depth_height, # ตำแหน่งแนวนอนและแนวตั้ง
                         self.rect.width, depth_height)) # ขนาดของความลึก

class FishingStatsWidget(Widget): # สร้างคลาส FishingStatsWidget สืบทอดจาก Widget
    def __init__(self, x, y): # สร้างเมธอด __init__ สำหรับกำหนดค่าเริ่มต้นของคลาส
        super().__init__(x, y, 200, 100) # เรียกใช้เมธอด __init__ ของคลาสแม่
        self.stats = { # กำหนดสถิติ
            'common': 0, # ปลาปกติ
            'rare': 0, # ปลาหายาก
            'legendary': 0 # ปลาตำนาน
        }
        
    def update_stats(self, fish_type): # สร้างเมธอด update_stats สำหรับอัพเดทสถิติ
        self.stats[fish_type] += 1 # อัพเดทสถิติ
        
    def draw(self, screen): # สร้างเมธอด draw สำหรับวาดสถิติลงบนหน้าจอ
        y_offset = 0  # กำหนดตำแหน่งแนวตั้ง
        for fish_type, count in self.stats.items(): # วนลูปสถิติ
            text = f"{fish_type.title()}: {count}" # กำหนดข้อความ
            TextLabel(self.rect.x, self.rect.y + y_offset, text, (255, 255, 255)).draw(screen) # วาดข้อความ
            y_offset += 30 # กำหนดตำแหน่งแนวตั้งของข้อความถัดไป
