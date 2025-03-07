class EventManager: # สร้างคลาส EventManager สำหรับจัดการกับ event ต่างๆ
    def __init__(self): # สร้างเมธอด __init__ ที่ไม่รับพารามิเตอร์
        self.callbacks = { # ใช้เก็บค่าของ event และ แต่ละอีเวนต์จะมีลิสตืของ callback ที่จะถูกเรียกเมื่อมีการเกิดอีเวนต์นั้นๆ
            'fish_caught': [], # สร้างลิสต์ของ callback ที่จะถูกเรียกเมื่อมีการเกิดอีเวนต์ ปลาถูกจับ
            'hook_dropped': [], # สร้างลิสต์ของ callback ที่จะถูกเรียกเมื่อมีการเกิดอีเวนต์ ปล่อยเบ็ด
            'hook_retrieved': [],   # สร้างลิสต์ของ callback ที่จะถูกเรียกเมื่อมีการเกิดอีเวนต์ ดึงเบ็ตขึ้นมา
            'game_over': [], # สร้างลิสต์ของ callback ที่จะถูกเรียกเมื่อมีการเกิดอีเวนต์ เกมส์จบ
            'score_changed': [], # สร้างลิสต์ของ callback ที่จะถูกเรียกเมื่อมีการเกิดอีเวนต์ คะแนนเปลี่ยน
            'boat_moved': [] # สร้างลิสต์ของ callback ที่จะถูกเรียกเมื่อมีการเกิดอีเวนต์ เรือเคลื่อนที่
        }
        
    def add_listener(self, event_name, callback): # สร้างเมธอด add_listener ที่รับพารามิเตอร์ event_name และ callback
        if event_name in self.callbacks: # เช็คว่า event_name อยู่ใน self.callbacksมั้ย
            self.callbacks[event_name].append(callback) # ถ้าใช่ ให้เพิ่ม callback ลงในลิสต์ของ event_name นั้นๆ
            
    def trigger_event(self, event_name, *args): # สร้างเมธอด trigger_event ที่รับพารามิเตอร์ event_name และ args
        if event_name in self.callbacks: # เช็คว่า event_name อยู่ใน self.callbacksมั้ย
            for callback in self.callbacks[event_name]: # วนลูปเพื่อเรียก callback ทุกตัวในลิสต์ของ event_name นั้นๆ
                callback(*args) # เรียก callback โดยส่ง args ไปด้วย
