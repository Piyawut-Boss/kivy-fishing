import pygame

class Fish:
    _SWIM_SPEED = 2
    _FISH_WIDTH = 80
    _FISH_HEIGHT = 50
    _FISH_FLOAT_SPEED = 1  # เปลี่ยนจาก __FISH_FLOAT_SPEED เป็น _FISH_FLOAT_SPEED

    def __init__(self, x_pos: int or float, y_pos: int or float):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.left_image, self.right_image = self.load_pictures()

    @property
    def x_pos(self):
        return self.__x_pos

    @x_pos.setter
    def x_pos(self, value):
        if isinstance(value, (int, float)):
            self.__x_pos = value
        else:
            raise ValueError("You must enter integer or a float value for the WIDTH.")

    @property
    def y_pos(self):
        return self.__y_pos

    @y_pos.setter
    def y_pos(self, value):
        if isinstance(value, (int, float)):
            self.__y_pos = value
        else:
            raise ValueError("You must enter integer or a float value for the HEIGHT")

    @staticmethod
    def load_pictures():
        left_direction = pygame.image.load("images/fish_1_left.png")
        right_direction = pygame.image.load("images/fish_1_right.png")
        return (
            pygame.transform.scale(left_direction, (Fish._FISH_WIDTH, Fish._FISH_HEIGHT)),
            pygame.transform.scale(right_direction, (Fish._FISH_WIDTH, Fish._FISH_HEIGHT))
        )

    def swim_left(self, seconds_passed: int, fish_rect):
        self.x_pos -= Fish._SWIM_SPEED
        fish_rect.x -= Fish._SWIM_SPEED
        if seconds_passed % 2 == 0:
            self.y_pos -= Fish._FISH_FLOAT_SPEED
            fish_rect.y -= Fish._FISH_FLOAT_SPEED
        else:
            self.y_pos += Fish._FISH_FLOAT_SPEED
            fish_rect.y += Fish._FISH_FLOAT_SPEED

    def swim_right(self, seconds_passed: int, fish_rect):
        self.x_pos += Fish._SWIM_SPEED
        fish_rect.x += Fish._SWIM_SPEED
        if seconds_passed % 2 == 0:
            self.y_pos -= Fish._FISH_FLOAT_SPEED
            fish_rect.y -= Fish._FISH_FLOAT_SPEED
        else:
            self.y_pos += Fish._FISH_FLOAT_SPEED
            fish_rect.y += Fish._FISH_FLOAT_SPEED

    def check_left_wall(self):
        return True if self.x_pos < 0 else False

    def check_right_wall(self, screen_width: int):
        return True if self.x_pos > screen_width - Fish._FISH_WIDTH else False

    @staticmethod
    def increase_speed_fish_after_caught():
        Fish._SWIM_SPEED += 1

class Shark(Fish):  # Shark inherits from Fish
    _SHARK_SPEED = 4  # Sharks swim faster

    def __init__(self, x_pos, y_pos):
        super().__init__(x_pos, y_pos)
        self.left_image, self.right_image = self.load_pictures()

    @staticmethod
    def load_pictures():
        left_direction = pygame.image.load("images/shark_left.png")
        right_direction = pygame.image.load("images/shark_right.png")
        return (
            pygame.transform.scale(left_direction, (Fish._FISH_WIDTH, Fish._FISH_HEIGHT)),
            pygame.transform.scale(right_direction, (Fish._FISH_WIDTH, Fish._FISH_HEIGHT))
        )

    def swim_left(self, seconds_passed: int, fish_rect):
        self.x_pos -= Shark._SHARK_SPEED
        fish_rect.x -= Shark._SHARK_SPEED
        if seconds_passed % 2 == 0:
            self.y_pos -= Fish._FISH_FLOAT_SPEED
            fish_rect.y -= Fish._FISH_FLOAT_SPEED
        else:
            self.y_pos += Fish._FISH_FLOAT_SPEED
            fish_rect.y += Fish._FISH_FLOAT_SPEED

    def swim_right(self, seconds_passed: int, fish_rect):
        self.x_pos += Shark._SHARK_SPEED
        fish_rect.x += Shark._SHARK_SPEED
        if seconds_passed % 2 == 0:
            self.y_pos -= Fish._FISH_FLOAT_SPEED
            fish_rect.y -= Fish._FISH_FLOAT_SPEED
        else:
            self.y_pos += Fish._FISH_FLOAT_SPEED
            fish_rect.y += Fish._FISH_FLOAT_SPEED