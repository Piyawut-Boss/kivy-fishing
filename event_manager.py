class EventManager:
    def __init__(self):
        self.callbacks = {
            'fish_caught': [],
            'hook_dropped': [],
            'hook_retrieved': [],
            'game_over': [],
            'score_changed': [],
            'boat_moved': []
        }
        
    def add_listener(self, event_name, callback):
        if event_name in self.callbacks:
            self.callbacks[event_name].append(callback)
            
    def trigger_event(self, event_name, *args):
        if event_name in self.callbacks:
            for callback in self.callbacks[event_name]:
                callback(*args)
