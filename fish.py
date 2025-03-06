import pygame

class Fish:
    _SWIM_SPEED = 2
    _FISH_WIDTH = 80
    _FISH_HEIGHT = 50
    _FISH_FLOAT_SPEED = 1

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
            raise ValueError("You must enter an integer or a float value for the WIDTH.")

    @property
    def y_pos(self):
        return self.__y_pos

    @y_pos.setter
    def y_pos(self, value):
        if isinstance(value, (int, float)):
            self.__y_pos = value
        else:
            raise ValueError("You must enter an integer or a float value for the HEIGHT.")

    @staticmethod
    def load_pictures():
        left_direction = pygame.image.load("images/fish_1_left.png")
        right_direction = pygame.image.load("images/fish_1_right.png")

        scale_factor = 0.1  # ลดขนาดลง 50%
        new_size = (int(left_direction.get_width() * scale_factor), int(left_direction.get_height() * scale_factor))

        return (
            pygame.transform.scale(left_direction, new_size),
            pygame.transform.scale(right_direction, new_size)
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
        return self.x_pos < 0

    def check_right_wall(self, screen_width: int):
        return self.x_pos > screen_width - Fish._FISH_WIDTH

    @staticmethod
    def increase_speed_fish_after_caught():
        Fish._SWIM_SPEED += 1


class Shark(Fish):  # Shark สืบทอดจาก Fish
    _SHARK_SPEED = 4  # ฉลามว่ายเร็วกว่า

    def __init__(self, x_pos, y_pos):
        super().__init__(x_pos, y_pos)
        self.left_image, self.right_image = self.load_pictures()

    @staticmethod
    def load_pictures():
        left_direction = pygame.image.load("images/shark_left.png")
        right_direction = pygame.image.load("images/shark_right.png")

        scale_factor = 0.185  # ลดขนาดลง 50%
        new_size = (int(left_direction.get_width() * scale_factor), int(left_direction.get_height() * scale_factor))

        return (
            pygame.transform.scale(left_direction, new_size),
            pygame.transform.scale(right_direction, new_size)
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
