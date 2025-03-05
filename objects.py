import pygame
import random
from config import GameConfig as cfg

class GameObject:
    def __init__(self, image_path, size):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Boat(GameObject):
    def __init__(self):
        super().__init__("images/boat_left.png", (200, 100))
        self.rect.centerx = cfg.WINDOW_SIZE[0] // 2
        self.rect.bottom = 150
        
    def update(self, keys):
        if keys[pygame.K_LEFT]: self.rect.x -= cfg.BOAT_SPEED
        if keys[pygame.K_RIGHT]: self.rect.x += cfg.BOAT_SPEED
        self.rect.clamp_ip(pygame.display.get_surface().get_rect())

class Fish(GameObject):
    def __init__(self):
        super().__init__("images/fish_1_left.png", (80, 50))
        self.speed = cfg.FISH_SPEED
        self.direction = 1
        self.respawn()
        
    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.right > cfg.WINDOW_SIZE[0] or self.rect.left < 0:
            self.direction *= -1
            self.image = pygame.transform.flip(self.image, True, False)
            
    def respawn(self):
        self.rect.x = random.randrange(cfg.WINDOW_SIZE[0] - self.rect.width)
        self.rect.y = random.randrange(300, cfg.WINDOW_SIZE[1] - 100)

class Hook(GameObject):
    def __init__(self, boat):
        super().__init__("images/hook.png", (15, 30))
        self.boat = boat
        self.is_fishing = False
        self.reset()
        
    def reset(self):
        self.rect.centerx = self.boat.rect.centerx
        self.rect.top = self.boat.rect.bottom
        
    def start_fishing(self):
        self.is_fishing = True
        
    def update(self, boat):
        if not self.is_fishing:
            self.rect.centerx = boat.rect.centerx
        else:
            self.rect.y += cfg.HOOK_SPEED
            if self.rect.bottom > cfg.MAX_DEPTH:
                self.is_fishing = False
                self.reset()
