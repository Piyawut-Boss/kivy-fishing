import pygame # ใช้งาน pygame ในการโหลดภาพ

class Fish: # สร้างคราสปลา
    _SWIM_SPEED = 2 # ความเร็วในการว่าย
    _FISH_WIDTH = 80 # กำหนดความกว้างของปลา
    _FISH_HEIGHT = 50 # กำหนดความสูงของปลา 
    _FISH_FLOAT_SPEED = 1 # ความเร็วในการลอยขึ้นลงของปลา

    def __init__(self, x_pos: int or float, y_pos: int or float): # กำหนดเมธอด __init__ โดยรับพารามิเตอร์ x_pos และ y_pos เพื่อกำหนดตำแหน่งปลา
        self.x_pos = x_pos # กำหนดตำแหน่ง x ของปลา
        self.y_pos = y_pos # กำหนดตำแหน่ง y ของปลา
        self.left_image, self.right_image = self.load_pictures() # โหลดภาพของปลาที่ว่ายไปทางซ้ายและขวา

    @property # กำหนดเมธอด getter สำหรับ x_pos
    def x_pos(self): # กำหนดเมธอด x_pos สำหรับคืนค่าตำแหน่ง x ของปลา
        return self.__x_pos

    @x_pos.setter # กำหนดเมธอด setter สำหรับ x_pos
    def x_pos(self, value): # กำหนดเมธอด x_pos สำหรับกำหนดค่าตำแหน่ง x ของปลา
        if isinstance(value, (int, float)): # ถ้าค่าที่รับเข้ามาเป็น int หรือ float
            self.__x_pos = value # กำหนดค่าตำแหน่ง x ของปลา
        else:
            raise ValueError("You must enter an integer or a float value for the WIDTH.") # แสดงข้อความว่า คุณต้องใส่ค่าเป็นจำนวนเต็มหรือทศนิยมสำหรับความกว้าง

    @property # กำหนดเมธอด getter สำหรับ y_pos
    def y_pos(self): # กำหนดเมธอด y_pos สำหรับคืนค่าตำแหน่ง y ของปลา
        return self.__y_pos 

    @y_pos.setter # กำหนดเมธอด setter สำหรับ y_pos
    def y_pos(self, value): # กำหนดเมธอด y_pos สำหรับกำหนดค่าตำแหน่ง y ของปลา
        if isinstance(value, (int, float)): # ถ้าค่าที่รับเข้ามาเป็น int หรือ float
            self.__y_pos = value # กำหนดค่าตำแหน่ง y ของปลา
        else:
            raise ValueError("You must enter an integer or a float value for the HEIGHT.") # แสดงข้อความว่า คุณต้องใส่ค่าเป็นจำนวนเต็มหรือทศนิยมสำหรับความสูง

    @staticmethod # กำหนดเมธอดเป็นเมธอดสถิต
    def load_pictures(): # กำหนดเมธอด load_pictures สำหรับโหลดภาพของปลา
        left_direction = pygame.image.load("images/fish_1_left.png") # โหลดภาพของปลาที่ว่ายไปทางซ้าย
        right_direction = pygame.image.load("images/fish_1_right.png") # โหลดภาพของปลาที่ว่ายไปทางขวา

        scale_factor = 0.1  # ลดขนาดลง 50%
        new_size = (int(left_direction.get_width() * scale_factor), int(left_direction.get_height() * scale_factor)) # กำหนดขนาดใหม่ของภาพ

        return ( # คืนค่าภาพของปลาที่ว่ายไปทางซ้ายและขวา
            pygame.transform.scale(left_direction, new_size),
            pygame.transform.scale(right_direction, new_size)
        )

    def swim_left(self, seconds_passed: int, fish_rect): # กำหนดเมธอด swim_left สำหรับให้ปลาว่ายไปทางซ้าย
        self.x_pos -= Fish._SWIM_SPEED # ปรับตำแหน่ง x ของปลาให้ลดลง
        fish_rect.x -= Fish._SWIM_SPEED # ปรับตำแหน่ง x ของสี่เหลี่ยมของปลาให้ลดลง
        if seconds_passed % 2 == 0: # ถ้าเวลาที่ผ่านมาหารด้วย 2 ลงตัว
            self.y_pos -= Fish._FISH_FLOAT_SPEED # ปรับตำแหน่ง y ของปลาให้ลดลง
            fish_rect.y -= Fish._FISH_FLOAT_SPEED # ปรับตำแหน่ง y ของสี่เหลี่ยมของปลาให้ลดลง
        else:
            self.y_pos += Fish._FISH_FLOAT_SPEED # ปรับตำแหน่ง y ของปลาให้เพิ่มขึ้น
            fish_rect.y += Fish._FISH_FLOAT_SPEED # ปรับตำแหน่ง y ของสี่เหลี่ยมของปลาให้เพิ่มขึ้น

    def swim_right(self, seconds_passed: int, fish_rect): # กำหนดเมธอด swim_right สำหรับให้ปลาว่ายไปทางขวา
        self.x_pos += Fish._SWIM_SPEED # ปรับตำแหน่ง x ของปลาให้เพิ่มขึ้น
        fish_rect.x += Fish._SWIM_SPEED # ปรับตำแหน่ง x ของสี่เหลี่ยมของปลาให้เพิ่มขึ้น
        if seconds_passed % 2 == 0: # ถ้าเวลาที่ผ่านมาหารด้วย 2 ลงตัว
            self.y_pos -= Fish._FISH_FLOAT_SPEED # ปรับตำแหน่ง y ของปลาให้ลดลง
            fish_rect.y -= Fish._FISH_FLOAT_SPEED # ปรับตำแหน่ง y ของสี่เหลี่ยมของปลาให้ลดลง
        else:
            self.y_pos += Fish._FISH_FLOAT_SPEED # ปรับตำแหน่ง y ของปลาให้เพิ่มขึ้น
            fish_rect.y += Fish._FISH_FLOAT_SPEED # ปรับตำแหน่ง y ของสี่เหลี่ยมของปลาให้เพิ่มขึ้น

    def check_left_wall(self): # กำหนดเมธอด check_left_wall สำหรับตรวจสอบว่าปลาชนขอบซ้ายหรือไม่
        return self.x_pos < 0 # คืนค่าว่าตำแหน่ง x ของปลาน้อยกว่า 0 หรือไม่

    def check_right_wall(self, screen_width: int): # กำหนดเมธอด check_right_wall สำหรับตรวจสอบว่าปลาชนขอบขวาหรือไม่
        return self.x_pos > screen_width - Fish._FISH_WIDTH # คืนค่าว่าตำแหน่ง x ของปลามากกว่าความกว้างของหน้าจอลบด้วยความกว้างของปลาหรือไม่

    @staticmethod # กำหนดเมธอดเป็นเมธอดสถิต
    def increase_speed_fish_after_caught(): # กำหนดเมธอด increase_speed_fish_after_caught สำหรับเพิ่มความเร็วในการว่ายของปลาหลังจากตกปลา
        Fish._SWIM_SPEED += 1 # เพิ่มความเร็วในการว่ายของปลาขึ้น 1


class Shark(Fish):  # Shark สืบทอดจาก Fish
    _SHARK_SPEED = 4  # ฉลามว่ายเร็วกว่า

    def __init__(self, x_pos, y_pos): # กำหนดเมธอด __init__ โดยรับพารามิเตอร์ x_pos และ y_pos
        super().__init__(x_pos, y_pos) # เรียกใช้เมธอด __init__ ของคลาสแม่
        self.left_image, self.right_image = self.load_pictures() # โหลดภาพของฉลามที่ว่ายไปทางซ้ายและขวา

    @staticmethod # กำหนดเมธอดเป็นเมธอดสถิต
    def load_pictures(): # กำหนดเมธอด load_pictures สำหรับโหลดภาพของฉลาม
        left_direction = pygame.image.load("images/shark_left.png") # โหลดภาพของฉลามที่ว่ายไปทางซ้าย
        right_direction = pygame.image.load("images/shark_right.png") # โหลดภาพของฉลามที่ว่ายไปทางขวา
 
        scale_factor = 0.185  # ลดขนาดลง 50%
        new_size = (int(left_direction.get_width() * scale_factor), int(left_direction.get_height() * scale_factor)) # กำหนดขนาดใหม่ของภาพ

        return ( # คืนค่าภาพของฉลามที่ว่ายไปทางซ้ายและขวา
            pygame.transform.scale(left_direction, new_size), # ปรับขนาดของภาพฉลามที่ว่ายไปทางซ้าย
            pygame.transform.scale(right_direction, new_size) # ปรับขนาดของภาพฉลามที่ว่ายไปทางขวา
        )

    def swim_left(self, seconds_passed: int, fish_rect): # กำหนดเมธอด swim_left สำหรับให้ฉลามว่ายไปทางซ้าย
        self.x_pos -= Shark._SHARK_SPEED # ปรับตำแหน่ง x ของฉลามให้ลดลง
        fish_rect.x -= Shark._SHARK_SPEED # ปรับตำแหน่ง x ของสี่เหลี่ยมของฉลามให้ลดลง
        if seconds_passed % 2 == 0: # ถ้าเวลาที่ผ่านมาหารด้วย 2 ลงตัว
            self.y_pos -= Fish._FISH_FLOAT_SPEED  # ปรับตำแหน่ง y ของฉลามให้ลดลง
            fish_rect.y -= Fish._FISH_FLOAT_SPEED # ปรับตำแหน่ง y ของสี่เหลี่ยมของฉลามให้ลดลง
        else: # ถ้าไม่
            self.y_pos += Fish._FISH_FLOAT_SPEED # ปรับตำแหน่ง y ของฉลามให้เพิ่มขึ้น
            fish_rect.y += Fish._FISH_FLOAT_SPEED # ปรับตำแหน่ง y ของสี่เหลี่ยมของฉลามให้เพิ่มขึ้น

    def swim_right(self, seconds_passed: int, fish_rect): # กำหนดเมธอด swim_right สำหรับให้ฉลามว่ายไปทางขวา
        self.x_pos += Shark._SHARK_SPEED # ปรับตำแหน่ง x ของฉลามให้เพิ่มขึ้น
        fish_rect.x += Shark._SHARK_SPEED # ปรับตำแหน่ง x ของสี่เหลี่ยมของฉลามให้เพิ่มขึ้น
        if seconds_passed % 2 == 0: # ถ้าเวลาที่ผ่านมาหารด้วย 2 ลงตัว
            self.y_pos -= Fish._FISH_FLOAT_SPEED # ปรับตำแหน่ง y ของฉลามให้ลดลง
            fish_rect.y -= Fish._FISH_FLOAT_SPEED # ปรับตำแหน่ง y ของสี่เหลี่ยมของฉลามให้ลดลง
        else:
            self.y_pos += Fish._FISH_FLOAT_SPEED # ปรับตำแหน่ง y ของฉลามให้เพิ่มขึ้น
            fish_rect.y += Fish._FISH_FLOAT_SPEED # ปรับตำแหน่ง y ของสี่เหลี่ยมของฉลามให้เพิ่มขึ้น
