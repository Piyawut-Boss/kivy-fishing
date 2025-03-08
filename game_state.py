from enum import Enum # ใช้Enum ในการกำหนดสถานะของเกม

class GameState(Enum): # สร้างคราสที่สืบทอดจาก Enum ในการกำหนดสถานะของเกม
    MENU = 1 # สถานะเมนู
    PLAYING = 2 # สถานะเล่นเกม
    PAUSED = 3 # สถานะเกมหยุด
    GAME_OVER = 4 # สถานะเกมจบ

class GameStateManager:
    def __init__(self): # สร้างเมธอด __init__ สำหรับกำหนดค่าเริ่มต้นของคลาส
        self.state = GameState.MENU # กำหนดสถานะเริ่มต้นของเกม
        self.callbacks = {state: [] for state in GameState} # สร้างดิกชันนารีเพื่อเก็บฟังก์ชันที่จะถูกเรียกเมื่อสถานะเปลี่ยน
        self.score = 0 # กำหนดคะแนนเริ่มต้นของเกม
        self.best_score = 0 # กำหนดคะแนนสูงสุดของเกม
        
    def change_state(self, new_state): # สร้างเมธอด change_state สำหรับเปลี่ยนสถานะของเกม
        self.state = new_state # กำหนดสถานะของเกม
        self._trigger_callbacks(new_state) # เรียกใช้เมธอด _trigger_callbacks เพื่อเรียกใช้ฟังก์ชันที่จะถูกเรียกเมื่อสถานะเปลี่ยน
        
    def add_callback(self, state, callback): # สร้างเมธอด add_callback สำหรับเพิ่มฟังก์ชันที่จะถูกเรียกเมื่อสถานะเปลี่ยน
        self.callbacks[state].append(callback) # เพิ่มฟังก์ชันที่จะถูกเรียกเมื่อสถานะเปลี่ยน
        
    def _trigger_callbacks(self, state): # สร้างเมธอด _trigger_callbacks สำหรับเรียกใช้ฟังก์ชันที่จะถูกเรียกเมื่อสถานะเปลี่ยน
        for callback in self.callbacks[state]: # วนลูปเพื่อเรียกใช้ฟังก์ชันที่จะถูกเรียกเมื่อสถานะเปลี่ยน
            callback() # เรียกใช้ฟังก์ชันที่จะถูกเรียกเมื่อสถานะเปลี่ยน
