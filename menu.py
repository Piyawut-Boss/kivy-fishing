import pygame # นำเข้าโมดูล pygame เพื่อใช้สำหรับพัฒนาเกม
from widgets import Button, TextLabel # นำเข้าคลาส Button และ TextLabel จากโมดูล widgets

# สีที่ใช้ในเมนู
MENU_BLUE = (65, 105, 225) 
MENU_WHITE = (255, 255, 255)
MENU_HOVER = (100, 149, 237)

# สีที่ใช้ใน AboutPopup
POPUP_BG = (50, 50, 50)
POPUP_WHITE = (255, 255, 255)
POPUP_HOVER = (100, 149, 237)

class AboutPopup: # คลาสสำหรับแสดง pop-up ข้อมูลเกม
    def __init__(self, screen_size): # สร้างเมธอด __init__ สำหรับกำหนดค่าเริ่มต้นของคลาส
        self.width, self.height = 400, 300 # กำหนดขนาดของ pop-up
        self.x = (screen_size[0] - self.width) // 2 # กำหนดตำแหน่ง x ของ pop-up
        self.y = (screen_size[1] - self.height) // 2 # กำหนดตำแหน่ง y ของ pop-up
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height) # กำหนดพื้นที่ของ pop-up
        self.title = TextLabel(self.x + 20, self.y + 20, "About the Game", POPUP_WHITE, 36) # กำหนดข้อความหัวของ pop-up
        self.description = TextLabel(self.x + 20, self.y + 100, "This game was created by  .... .", POPUP_WHITE, 24) # กำหนดข้อความรายละเอียดของ pop-up
        self.close_button = Button(self.x + 120, self.y + 220, 160, 50, "Close", POPUP_BG, POPUP_HOVER) # กำหนดปุ่มปิด pop-up

    def draw(self, screen): # สร้างเมธอด draw สำหรับวาด pop-up ลงบนหน้าจอ
        pygame.draw.rect(screen, POPUP_BG, self.rect)  # draw background
        self.title.draw(screen) # วาดข้อความหัว
        self.description.draw(screen) # วาดข้อความรายละเอียด
        self.close_button.draw(screen) # วาดปุ่มปิด

    def handle_mouse(self, pos): # สร้างเมธอด handle_mouse สำหรับจัดการเมื่อเมาส์คลิก
        self.close_button.is_hovered = self.close_button.rect.collidepoint(pos) # ตรวจสอบว่าเมาส์ชี้ที่ปุ่มปิดหรือไม่

class GameMenu:
    def __init__(self, screen_size): # สร้างเมธอด __init__ สำหรับกำหนดค่าเริ่มต้นของคลาส
        self.screen_width, self.screen_height = screen_size # กำหนดความกว้างและความสูงของหน้าจอ
        self.background_image = pygame.image.load("images/background.png")  # โหลดภาพพื้นหลัง
        self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))  # ปรับขนาดภาพให้พอดีกับหน้าจอ
        self.title = TextLabel(self.screen_width // 2 - 100, 150, "Fisherman", MENU_WHITE, 74) # กำหนดข้อความหัวเรื่อง
        self.start_button = Button(self.screen_width // 2 - 100, 300, 200, 50, "Start", MENU_BLUE, MENU_HOVER) # กำหนดปุ่มเริ่มเกม
        self.about_button = Button(self.screen_width // 2 - 100, 400, 200, 50, "About Us", MENU_BLUE, MENU_HOVER) # กำหนดปุ่มเกี่ยวกับเรา
        self.quit_button = Button(self.screen_width // 2 - 100, 500, 200, 50, "Quit", MENU_BLUE, MENU_HOVER) # กำหนดปุ่มออกจากเกม
    
    def draw(self, screen): # สร้างเมธอด draw สำหรับวาดเมนูลงบน
        screen.blit(self.background_image, (0, 0))  # แสดงภาพพื้นหลัง
        self.title.draw(screen) # แสดงข้อความหัวเรื่อง
        self.start_button.draw(screen) # แสดงปุ่มเริ่มเกม
        self.about_button.draw(screen)  # แสดงปุ่มเกี่ยวกับเรา
        self.quit_button.draw(screen) # แสดงปุ่มออกจากเกม

    def handle_mouse(self, pos): # สร้างเมธอด handle_mouse สำหรับจัดการเมื่อเมาส์คลิก
        self.start_button.is_hovered = self.start_button.rect.collidepoint(pos) # ตรวจสอบว่าเมาส์ชี้ที่ปุ่มเริ่มเกมหรือไม่
        self.about_button.is_hovered = self.about_button.rect.collidepoint(pos) # ตรวจสอบว่าเมาส์ชี้ที่ปุ่มเกี่ยวกับเราหรือไม่
        self.quit_button.is_hovered = self.quit_button.rect.collidepoint(pos) # ตรวจสอบว่าเมาส์ชี้ที่ปุ่มออกจากเกมหรือไม่

# ฟังก์ชันแสดงเมนูหลัก
def show_menu(screen): # สร้างฟังก์ชัน show_menu สำหรับแสดงเมนูหลัก
    menu = GameMenu(screen.get_size()) # สร้างเมนู
    menu_running = True # กำหนดว่าเมนูกำลังทำงาน
    about_popup = None  # กำหนดว่าไม่มี pop-up ในตอนเริ่มต้น

    while menu_running: # วนลูปเมนู
        mouse_pos = pygame.mouse.get_pos() # รับตำแหน่งของเมาส์
        menu.handle_mouse(mouse_pos) # จัดการเมื่อเมาส์คลิก

        if about_popup:  # ถ้ามี Pop-up
            about_popup.handle_mouse(mouse_pos) # จัดการเมื่อเมาส์คลิก
            about_popup.draw(screen) # วาด pop-up
        else:
            menu.draw(screen) # วาดเมนู

        for event in pygame.event.get(): # ตรวจสอบเหตุการณ์ที่เกิดขึ้น
            if event.type == pygame.QUIT: # ถ้าเกิดเหตุการณ์การออกจากเกม
                return "quit" # ออกจากเกม
            if event.type == pygame.MOUSEBUTTONDOWN: # ถ้าเกิดเหตุการณ์คลิกเมาส์
                if menu.start_button.rect.collidepoint(event.pos): # ถ้าคลิกที่ปุ่มเริ่มเกม
                    return "start" # เริ่มเกม
                if menu.about_button.rect.collidepoint(event.pos): # ถ้าคลิกที่ปุ่มเกี่ยวกับเรา
                    about_popup = AboutPopup(screen.get_size())  # เปิด pop-up
                if menu.quit_button.rect.collidepoint(event.pos): # ถ้าคลิกที่ปุ่มออกจากเกม
                    return "quit" # ออกจากเกม
                if about_popup and about_popup.close_button.rect.collidepoint(event.pos):  # ปิด pop-up
                    about_popup = None

        pygame.display.flip() # อัพเดทหน้าจอ
        pygame.time.Clock().tick(60) # จำกัด FPS ที่ 60
