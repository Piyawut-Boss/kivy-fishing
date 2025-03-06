from boat import Boat

class FishLine:

    def __init__(self, boat: Boat):
        self.boat = boat  # เก็บอ้างอิงถึงเรือ
        self.update_tip_of_the_rod()  # ตั้งค่าปลายคันเบ็ดตามทิศทางเรือ
        self.advance_line = 150

    def update_tip_of_the_rod(self):
        """อัปเดตตำแหน่งปลายคันเบ็ดตามทิศทางเรือ"""
        if self.boat.direction == "right":
            self.tip_of_the_rod = self.boat.x + 210
        else:
            self.tip_of_the_rod = self.boat.x + 35

    def rotate_fisherman_right(self):
        self.boat.direction = "right"
        self.update_tip_of_the_rod()

    def rotate_fisherman_left(self):
        self.boat.direction = "left"
        self.update_tip_of_the_rod()
