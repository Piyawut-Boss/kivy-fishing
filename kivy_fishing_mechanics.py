import random # นำเข้าโมดูล random เพื่อใช้สำหรับสุ่มตำแหน่งของปลา
from kivy.event import EventDispatcher # นำเข้าคลาส EventDispatcher จากโมดูล kivy.event
from kivy.properties import NumericProperty, StringProperty # นำเข้าคลาส NumericProperty และ StringProperty จากโมดูล kivy.properties

class KivyFishingMechanics(EventDispatcher): # สร้างคลาส KivyFishingMechanics สืบทอดคุณสมบัติจากคลาส EventDispatcher
    depth = NumericProperty(0) # กำหนดคุณสมบัติ depth เป็น NumericProperty ที่มีค่าเริ่มต้นเป็น 0
    fish_type = StringProperty('common') # กำหนดคุณสมบัติ fish_type เป็น StringProperty ที่มีค่าเริ่มต้นเป็น 'common'
    
    def __init__(self, **kwargs): # สร้างเมธอด __init__ สำหรับกำหนดค่าเริ่มต้นของคลาส
        super().__init__(**kwargs) # เรียกใช้เมธอด __init__ ของคลาสแม่
        self.fish_types = { # สร้างดิกชันนารีเพื่อเก็บประเภทของปลา
            'common': 1, # กำหนดค่าของปลาประเภท common
            'rare': 3, # กำหนดค่าของปลาประเภท rare
            'legendary': 5 # กำหนดค่าของปลาประเภท legendary
        }
        
    def try_catch(self, depth): # สร้างเมธอด try_catch สำหรับลองจับปลา
        self.depth = depth # กำหนดความลึกของน้ำ
        if depth < 300: # ถ้าความลึกน้อยกว่า 300
            return self.surface_catch() # เรียกใช้เมธอด surface_catch
        elif depth < 500: # ถ้าความลึกน้อยกว่า 500
            return self.medium_catch() # เรียกใช้เมธอด medium_catch
        else: # ถ้าความลึกมากกว่าหรือเท่ากับ 500
            return self.deep_catch() # เรียกใช้เมธอด deep_catch
            
    def surface_catch(self): # สร้างเมธอด surface_catch สำหรับจับปลาที่ผิวน้ำ
        if random.random() > 0.95: # ถ้าค่าสุ่มมากกว่า 0.95
            self.fish_type = 'rare' # กำหนดประเภทของปลาเป็นประเภท rare
            return self.fish_types['rare'] # ส่งค่าปลาประเภท rare กลับ
        self.fish_type = 'common' # กำหนดประเภทของปลาเป็นประเภท common
        return self.fish_types['common'] # ส่งค่าปลาประเภท common กลับ
        
    def medium_catch(self): # สร้างเมธอด medium_catch สำหรับจับปลาที่ลึกกลาง
        roll = random.random() # สุ่มค่า
        if roll > 0.8: # ถ้าค่าสุ่มมากกว่า 0.8
            self.fish_type = 'legendary' # กำหนดประเภทของปลาเป็นประเภท legendary
            return self.fish_types['legendary'] # ส่งค่าปลาประเภท legendary กลับ
        elif roll > 0.4:  # ถ้าค่าสุ่มมากกว่า 0.4
            self.fish_type = 'rare' # กำหนดประเภทของปลาเป็นประเภท rare
            return self.fish_types['rare'] # ส่งค่าปลาประเภท rare กลับ
        self.fish_type = 'common' # กำหนดประเภทของปลาเป็นประเภท common
        return self.fish_types['common'] # ส่งค่าปลาประเภท common กลับ
        
    def deep_catch(self): # สร้างเมธอด deep_catch สำหรับจับปลาที่ลึก
        roll = random.random() # สุ่มค่า
        if roll > 0.6: # ถ้าค่าสุ่มมากกว่า 0.6
            self.fish_type = 'legendary' # กำหนดประเภทของปลาเป็นประเภท legendary
            return self.fish_types['legendary'] # ส่งค่าปลาประเภท legendary กลับ
        elif roll > 0.3: # ถ้าค่าสุ่มมากกว่า 0.3
            self.fish_type = 'rare' # กำหนดประเภทของปลาเป็นประเภท rare
            return self.fish_types['rare'] # ส่งค่าปลาประเภท rare กลับ
        self.fish_type = 'common' # กำหนดประเภทของปลาเป็นประเภท common
        return self.fish_types['common'] # ส่งค่าปลาประเภท common กลับ
