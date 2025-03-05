import pygame
from settings import *
import random

class GameObject:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = None
        
    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect)

class Boat(GameObject):
    def __init__(self):
        super().__init__(SIZE[0]//2, 50, 200, 100)
        self.image = pygame.image.load("images/boat_left.png")
        self.speed = BOAT_SPEED
        
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]: self.rect.x += self.speed
        self.rect.clamp_ip(pygame.display.get_surface().get_rect())

class Fish(GameObject):
    def __init__(self):
        x = random.randrange(100, SIZE[0]-100)
        y = random.randrange(300, SIZE[1]-100)
        super().__init__(x, y, 80, 50)
        self.speed = FISH_SPEED
        self.direction = 1
        self.load_images()
        
    def load_images(self):
        self.images = {
            'left': pygame.image.load("images/fish_1_left.png"),
            'right': pygame.image.load("images/fish_1_right.png")
        }
        self.image = self.images['right']
        
    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.left < 0 or self.rect.right > SIZE[0]:
            self.direction *= -1
            self.image = self.images['right' if self.direction > 0 else 'left']

class Hook(GameObject):
    def __init__(self, boat):
        super().__init__(boat.rect.centerx, boat.rect.bottom, 15, 30)
        self.image = pygame.image.load("images/hook.png")
        self.boat = boat
        self.is_fishing = False
        self.speed = HOOK_SPEED
        
    def start_fishing(self):
        self.is_fishing = True
        
    def update(self):
        if self.is_fishing:
            self.rect.y += self.speed
            if self.rect.bottom > SIZE[1]:
                self.speed = -self.speed
            elif self.rect.top < self.boat.rect.bottom:
                self.is_fishing = False
                self.speed = abs(self.speed)
