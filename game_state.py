from enum import Enum # ใช้Enum ในการกำหนดสถานะของเกม

class GameState(Enum): # สร้างคราสที่สืบทอดจาก Enum ในการกำหนดสถานะของเกม
    MENU = 1 # สถานะเมนู
    PLAYING = 2 # สถานะเล่นเกม
    PAUSED = 3 # สถานะเกมหยุด
    GAME_OVER = 4 # สถานะเกมจบ

class GameStateManager:
    def __init__(self):
        self.state = GameState.MENU
        self.callbacks = {state: [] for state in GameState}
        self.score = 0
        self.best_score = 0
        
    def change_state(self, new_state):
        self.state = new_state
        self._trigger_callbacks(new_state)
        
    def add_callback(self, state, callback):
        self.callbacks[state].append(callback)
        
    def _trigger_callbacks(self, state):
        for callback in self.callbacks[state]:
            callback()
