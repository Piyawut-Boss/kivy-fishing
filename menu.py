import pygame
from widgets import Button, TextLabel

# สีที่ใช้ในเมนู
MENU_BLUE = (65, 105, 225)
MENU_WHITE = (255, 255, 255)
MENU_HOVER = (100, 149, 237)

class GameMenu:
    def __init__(self, screen_size):
        self.title = TextLabel(screen_size[0] // 2 - 100, 150, "Fisherman", MENU_WHITE, 74)
        self.start_button = Button(screen_size[0] // 2 - 100, 300, 200, 50, "Start", MENU_BLUE, MENU_HOVER)
        self.about_button = Button(screen_size[0] // 2 - 100, 400, 200, 50, "About", MENU_BLUE, MENU_HOVER)
        self.quit_button = Button(screen_size[0] // 2 - 100, 500, 200, 50, "Quit", MENU_BLUE, MENU_HOVER)
    
    def draw(self, screen):
        self.title.draw(screen)
        self.start_button.draw(screen)
        self.about_button.draw(screen)
        self.quit_button.draw(screen)

    def handle_mouse(self, pos):
        self.start_button.is_hovered = self.start_button.rect.collidepoint(pos)
        self.about_button.is_hovered = self.about_button.rect.collidepoint(pos)
        self.quit_button.is_hovered = self.quit_button.rect.collidepoint(pos)

def show_menu(screen):
    menu = GameMenu(screen.get_size())
    menu_running = True

    while menu_running:
        screen.fill((0, 0, 0))  # พื้นหลังสีดำ
        mouse_pos = pygame.mouse.get_pos()
        menu.handle_mouse(mouse_pos)
        menu.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu.start_button.rect.collidepoint(event.pos):
                    return "start"
                if menu.about_button.rect.collidepoint(event.pos):
                    return "about"
                if menu.quit_button.rect.collidepoint(event.pos):
                    return "quit"

        pygame.display.flip()
        pygame.time.Clock().tick(60)