import random

class FishingMechanics:
    def __init__(self, event_manager):
        self.event_manager = event_manager
        self.depth_multiplier = 1.0
        self.catch_chance = 0.8
        self.fish_variety = ['common', 'rare', 'legendary']
        self.fish_points = {
            'common': 1,    # Surface fish (0-300 depth)
            'rare': 3,      # Medium depth fish (301-500 depth)
            'legendary': 5  # Deep water fish (501+ depth)
        }
        
    def calculate_catch(self, hook_depth):
        # Deeper water has better fish
        self.depth_multiplier = min(2.0, hook_depth / 500)
        
        # Calculate fish type based on depth
        if hook_depth < 300:
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
    
    def attempt_catch(self, hook_depth):
        if random.random() < self.catch_chance:
            fish_type = self.calculate_catch(hook_depth)
            points = self.fish_points[fish_type]
            self.event_manager.trigger_event('fish_caught', fish_type, points)
            return True
        return False
