import pygame

class Widget:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = True
    
    def draw(self, screen):
        pass

class Button(Widget):
    def __init__(self, x, y, width, height, text, color, hover_color):
        super().__init__(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.Font(None, 36)
        self.is_hovered = False

    def draw(self, screen):
        if not self.visible:
            return
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class TextLabel(Widget):
    def __init__(self, x, y, text, color, font_size=30):
        super().__init__(x, y, 0, 0)
        self.text = text
        self.color = color
        self.font = pygame.font.Font(None, font_size)
        self.update_text(text)

    def update_text(self, new_text):
        self.text = new_text
        text_surface = self.font.render(self.text, True, self.color)
        self.rect.size = text_surface.get_size()

    def draw(self, screen):
        if not self.visible:
            return
        text_surface = self.font.render(self.text, True, self.color)
        screen.blit(text_surface, self.rect)

class BoatWidget(Widget):
    def __init__(self, x, y, boat):
        super().__init__(x, y, 200, 100)
        self.boat = boat
        self.left_image, self.right_image = boat.load_boat()
        self.current_image = self.left_image

    def draw(self, screen):
        screen.blit(self.current_image, (self.boat.x, self.boat.y))
        
    def face_left(self):
        self.current_image = self.left_image
        
    def face_right(self):
        self.current_image = self.right_image

class FishWidget(Widget):
    def __init__(self, fish, initial_direction='left'):
        super().__init__(fish.x_pos, fish.y_pos, 80, 50)
        self.fish = fish
        self.left_image, self.right_image = fish.load_pictures()
        self.current_image = self.left_image if initial_direction == 'left' else self.right_image
        
    def draw(self, screen):
        screen.blit(self.current_image, (self.fish.x_pos, self.fish.y_pos))
        
    def update_direction(self, direction):
        self.current_image = self.left_image if direction == 'left' else self.right_image

class FishingLineWidget(Widget):
    def __init__(self, fishing_line, color=(255, 0, 0)):
        super().__init__(0, 0, 1, 1)
        self.fishing_line = fishing_line
        self.color = color
        
    def draw(self, screen, start_y, end_y):
        pygame.draw.line(screen, self.color, 
                        (self.fishing_line.tip_of_the_rod, start_y),
                        (self.fishing_line.tip_of_the_rod, end_y))

class HookWidget(Widget):
    def __init__(self, hook):
        super().__init__(0, hook.y_pos, 15, 30)
        self.hook = hook
        self.image = hook.picture
        
    def draw(self, screen, x_pos):
        screen.blit(self.image, (x_pos, self.hook.y_pos))

class GameOverWidget(Widget):
    def __init__(self, screen_size):
        super().__init__(0, 0, screen_size[0], screen_size[1])
        self.overlay = pygame.Surface(screen_size)
        self.overlay.set_alpha(128)
        self.overlay.fill((0, 0, 0))
        self.text = TextLabel(screen_size[0]//2 - 150, screen_size[1]//2, 
                            "Game Over! You Win!", (255, 0, 0), 48)
        
    def draw(self, screen):
        screen.blit(self.overlay, (0, 0))
        self.text.draw(screen)

class GameHUD:
    def __init__(self):
        self.fish_counter = TextLabel(10, 10, "Fish: 0", (255, 255, 255))
        self.record_label = TextLabel(160, 10, "Record: 0", (255, 255, 255))
        self.time_label = TextLabel(310, 10, "Time: 0s", (255, 255, 255))
        
    def update(self, fish_count, record, time):
        self.fish_counter.update_text(f"Fish: {fish_count}")
        self.record_label.update_text(f"Record: {record}")
        self.time_label.update_text(f"Time: {time}s")
        
    def draw(self, screen):
        self.fish_counter.draw(screen)
        self.record_label.draw(screen)
        self.time_label.draw(screen)
