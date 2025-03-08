import random # นำเข้าโมดูล random เพื่อใช้สำหรับสุ่มค่า

class FishingMechanics: # สร้างคลาส FishingMechanics เพื่อจัดการกับการตกปลา
    def __init__(self, event_manager): # กำหนดเมธอด __init__ โดยรับพารามิเตอร์ event_manager
        self.event_manager = event_manager # เก็บอ้างอิงถึง event_manager
        self.depth_multiplier = 1.0 # ตั้งค่าตัวคูณความลึกเป็น 1.0
        self.catch_chance = 0.8 # ตั้งค่าโอกาสในการตกปลาเป็น 80%
        self.fish_variety = ['common', 'rare', 'legendary'] # ตั้งค่าประเภทของปลา
        self.fish_points = { # ตั้งค่าคะแนนของปลาแต่ละประเภท
            'common': 1,    # Surface fish (0-300 depth)
            'rare': 3,      # Medium depth fish (301-500 depth)
            'legendary': 5  # Deep water fish (501+ depth)
        }
        
    def calculate_catch(self, hook_depth): # สร้างเมธอด calculate_catch สำหรับคำนวณประเภทของปลาที่จะตก
        # Deeper water has better fish
        self.depth_multiplier = min(2.0, hook_depth / 500) # คำนวณค่าตัวคูณความลึก
        
        # Calculate fish type based on depth
        if hook_depth < 300: # ถ้าความลึกน้อยกว่า 300
            chance = random.random() 
            if chance > 0.95:  # 5% chance for rare at surface
                return 'rare'
            return 'common'
        elif hook_depth < 500:
            chance = random.random()
            if chance > 0.8:   # 20% chance for legendary at medium depth
                return 'legendary'
            elif chance > 0.4:  # 40% chance for rare
                return 'rare'
            return 'common'
        else:  # Deep water
            chance = random.random()
            if chance > 0.6:   # 40% chance for legendary in deep water
                return 'legendary'
            elif chance > 0.3:  # 30% chance for rare
                return 'rare'
            return 'common'
    
    def attempt_catch(self, hook_depth): # สร้างเมธอด attempt_catch สำหรับลองตกปลา
        if random.random() < self.catch_chance: # ถ้าโอกาสในการตกปลาสูงกว่าค่าที่สุ่มได้
            fish_type = self.calculate_catch(hook_depth) # คำนวณประเภทของปลาที่จะตก
            points = self.fish_points[fish_type] # คำนวณคะแนนที่จะได้
            self.event_manager.trigger_event('fish_caught', fish_type, points) # ส่งอีเวนต์ fish_caught พร้อมกับประเภทของปลาและคะแนนที่ได้
            return True # ส่งค่า True กลับ
        return False
