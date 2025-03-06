import pygame
from widgets import Button, TextLabel

# สีที่ใช้ในเมนู
MENU_BLUE = (65, 105, 225)
MENU_WHITE = (255, 255, 255)
MENU_HOVER = (100, 149, 237)

# สีที่ใช้ใน AboutPopup
POPUP_BG = (50, 50, 50)
POPUP_WHITE = (255, 255, 255)
POPUP_HOVER = (100, 149, 237)

class AboutPopup:
    def __init__(self, screen_size):
        self.width, self.height = 400, 300
        self.x = (screen_size[0] - self.width) // 2
        self.y = (screen_size[1] - self.height) // 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.title = TextLabel(self.x + 20, self.y + 20, "About the Game", POPUP_WHITE, 36)
        self.description = TextLabel(self.x + 20, self.y + 100, "This game was created by  .... .", POPUP_WHITE, 24)
        self.close_button = Button(self.x + 120, self.y + 220, 160, 50, "Close", POPUP_BG, POPUP_HOVER)

    def draw(self, screen):
        pygame.draw.rect(screen, POPUP_BG, self.rect)  # draw background
        self.title.draw(screen)
        self.description.draw(screen)
        self.close_button.draw(screen)

    def handle_mouse(self, pos):
        self.close_button.is_hovered = self.close_button.rect.collidepoint(pos)

class GameMenu:
    def __init__(self, screen_size):
        self.screen_width, self.screen_height = screen_size
        self.background_image = pygame.image.load("images/background.png")  # โหลดภาพพื้นหลัง
        self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))  # ปรับขนาดภาพให้พอดีกับหน้าจอ
        self.title = TextLabel(self.screen_width // 2 - 100, 150, "Fisherman", MENU_WHITE, 74)
        self.start_button = Button(self.screen_width // 2 - 100, 300, 200, 50, "Start", MENU_BLUE, MENU_HOVER)
        self.about_button = Button(self.screen_width // 2 - 100, 400, 200, 50, "About Us", MENU_BLUE, MENU_HOVER)
        self.quit_button = Button(self.screen_width // 2 - 100, 500, 200, 50, "Quit", MENU_BLUE, MENU_HOVER)
    
    def draw(self, screen):
        screen.blit(self.background_image, (0, 0))  # แสดงภาพพื้นหลัง
        self.title.draw(screen)
        self.start_button.draw(screen)
        self.about_button.draw(screen)
        self.quit_button.draw(screen)

    def handle_mouse(self, pos):
        self.start_button.is_hovered = self.start_button.rect.collidepoint(pos)
        self.about_button.is_hovered = self.about_button.rect.collidepoint(pos)
        self.quit_button.is_hovered = self.quit_button.rect.collidepoint(pos)

# ฟังก์ชันแสดงเมนูหลัก
def show_menu(screen):
    menu = GameMenu(screen.get_size())
    menu_running = True
    about_popup = None  # กำหนดว่าไม่มี pop-up ในตอนเริ่มต้น

    while menu_running:
        mouse_pos = pygame.mouse.get_pos()
        menu.handle_mouse(mouse_pos)

        if about_popup:  # ถ้ามี Pop-up
            about_popup.handle_mouse(mouse_pos)
            about_popup.draw(screen)
        else:
            menu.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu.start_button.rect.collidepoint(event.pos):
                    return "start"
                if menu.about_button.rect.collidepoint(event.pos):
                    about_popup = AboutPopup(screen.get_size())  # เปิด pop-up
                if menu.quit_button.rect.collidepoint(event.pos):
                    return "quit"
                if about_popup and about_popup.close_button.rect.collidepoint(event.pos):  # ปิด pop-up
                    about_popup = None

        pygame.display.flip()
        pygame.time.Clock().tick(60)
