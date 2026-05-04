#ai.py
import random

class SwordAI:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.memory = []
        # [Reaction(ms), Parry%, Counter%, MoveSpeed]
        self.levels = {
            "Beginner": [1000, 0.05, 0.05, 1],
            "noob": [700, 0.15, 0.1, 2],
            "eh?": [500, 0.3, 0.2, 3],
            "Medium": [300, 0.5, 0.4, 4],
            "hard": [150, 0.7, 0.6, 6],
            "GRANDMASTER": [80, 0.9, 0.85, 8],
            "Matt the master!": [30, 0.99, 1.0, 12]
        }
        self.stats = self.levels.get(difficulty, [500, 0.3, 0.2, 3])

    def decide_reaction(self, player_action, distance):
        speed, parry_rate, counter_rate, _ = self.stats
        
        # Memory/Pattern Tracking
        self.memory.append(player_action)
        if len(self.memory) > 5: self.memory.pop(0)
        
        # Spam Penalty: AI becomes perfect if player spams attack
        if self.memory.count("attack") >= 3:
            parry_rate = min(1.0, parry_rate + 0.4)

        # Distance logic: Too far = ignore
        if distance > 170: return "ignore"

        if player_action == "attack":
            if random.random() < parry_rate:
                return "parry_counter" if random.random() < counter_rate else "parry"
            return "get_hit"
        return "idle"

    def get_stats(self):
        return self.stats