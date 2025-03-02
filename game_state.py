from enum import Enum

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4

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
