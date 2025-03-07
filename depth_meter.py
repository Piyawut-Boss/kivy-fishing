from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.graphics import Rectangle, Color

class DepthMeter(Widget): #สร้างคลาส DepthMeter ที่สืบทอดมาจากคลาส Widget
    depth = NumericProperty(0) #สร้างคุณสมบัติ ความลึก ค่าเริ่มต้นเป็น 0
    
    def __init__(self, **kwargs): #สร้างเมธอด __init__ ที่รับค่าพารามิเตอร์ kwargs คือรับค่าหลายๆค่าโดยไม่ต้องกำหนดตัวแปรๆไว้ล่วงหน้า
        super().__init__(**kwargs) #เรียกใช้เมธอด __init__ ของคลาสแม่ช่วยส่งอาร์กิวเมนต์ที่ไม่ได้กำหนดล่วงหน้าไปให้คลาส
        self.size_hint = (None, None) #กำหนดขนาดของวิดเจตให้เป็นขนาดเท่ากับขนาดจริง
        self.size = (30, 200) #กำหนดขนาดของวิดเจตเป็น 30x200
        self.bind(pos=self.update_meter, size=self.update_meter) #เรียกใช้เมธอด bind ที่เป็นเมธอดของคลาส Widget โดยให้เมธอด update_meter ทำงานเมื่อมีการเปลี่ยนแปลงค่าของ pos หรือ size
        
    def update_meter(self, *args): #สร้างเมธอด update_meter ที่รับค่าพารามิเตอร์ args คือรับค่าหลายๆค่าโดยไม่ต้องกำหนดตัวแปรๆไว้ล่วงหน้า
        self.canvas.clear() #ลบเนื้อหาทั้งหมดในวิดเจต
        with self.canvas: #กำหนดการวาดรูปภาพ
            # Background
            Color(0.4, 0.4, 0.4)
            Rectangle(pos=self.pos, size=self.size)
            
            # Depth indicator
            Color(0, 0.75, 1)
            height = (self.depth / 700) * self.height
            Rectangle(pos=self.pos, size=(self.width, height))
