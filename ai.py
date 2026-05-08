# ai.py
# This code is under the GPL V 2.0
# Made by McaFeehater.
# Use these comments if code is used, plz!

import random


class SwordAI:
    def __init__(self, difficulty):
        self.difficulty = difficulty

        # has the recent player actions:
        
        self.memory = []

        # Learning speed
        self.learning_rate = 0.03

        #proformance tracking
        self.performance = {
            "parry_success": 0,
            "parry_fail": 0,
            "counter_success": 0,
            "counter_fail": 0
        }

        # difficulty levels:
        # Reaction(ms), Parry%, Counter%, MoveSpeed
        self.levels = {
            "Beginner": [1000, 0.05, 0.05, 1],
            "noob": [700, 0.15, 0.10, 2],
            "eh?": [500, 0.30, 0.20, 3],
            "Medium": [300, 0.50, 0.40, 4],
            "hard": [150, 0.70, 0.60, 6],
            "GRANDMASTER": [80, 0.90, 0.85, 8],
            "Matt the master!": [30, 0.99, 1.00, 12]
        }

        # Default states
        self.stats = self.levels.get(difficulty, [500, 0.30, 0.20, 3])

   # AI decision
    def decide_reaction(self, player_action, distance):

        reaction_speed, parry_rate, counter_rate, move_speed = self.stats

        # Store player action
        self.memory.append(player_action)

        # Keep memory size limited
        if len(self.memory) > 10:
            self.memory.pop(0)

     
     #pattern recognitons
        attack_ratio = self.memory.count("attack") / len(self.memory)

        # STOP SPAMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMING!
        if attack_ratio >= 0.6:
            parry_rate = min(1.0, parry_rate + 0.20)

        # Too far 
        if distance > 170:
            return "approach"

#combat logic
        if player_action == "attack":

            # Attempt parry
            if random.random() < parry_rate:

                # counter-attack
                if random.random() < counter_rate:
                    return "parry_counter"

                return "parry"

            # defense failed
            return "get_hit"

        elif player_action == "feint":

            # panic fix
            if random.random() < 0.3:
                return "false_parry"

            return "wait"

        elif player_action == "idle":

            # AI pressures passive players
            if random.random() < 0.4:
                return "attack"

            return "idle"

        return "idle"

   #learning system
    def learn(self, action, success):

        #parry learning system
        if action == "parry":

            if success:
                self.performance["parry_success"] += 1

                # Increase parry skill slightly
                self.stats[1] = min(
                    1.0,
                    self.stats[1] + self.learning_rate
                )

            else:
                self.performance["parry_fail"] += 1

                # Decrease parry skill slightly
                self.stats[1] = max(
                    0.05,
                    self.stats[1] - self.learning_rate
                )

        #Counter learning
        elif action == "counter":

            if success:
                self.performance["counter_success"] += 1

                # increase skill counter
                self.stats[2] = min(
                    1.0,
                    self.stats[2] + self.learning_rate
                )

            else:
                self.performance["counter_fail"] += 1

                # Decrease counter skill slightly
                self.stats[2] = max(
                    0.05,
                    self.stats[2] - self.learning_rate
                )

  
  #Returns the AI learning state
    def get_stats(self):
        return {
            "difficulty": self.difficulty,
            "reaction_speed": self.stats[0],
            "parry_rate": round(self.stats[1], 2),
            "counter_rate": round(self.stats[2], 2),
            "move_speed": self.stats[3],
            "performance": self.performance
        }

   
   #Reset function
    def reset_learning(self):

        self.performance = {
            "parry_success": 0,
            "parry_fail": 0,
            "counter_success": 0,
            "counter_fail": 0
        }

        self.stats = self.levels.get(
            self.difficulty,
            [500, 0.30, 0.20, 3]
        )

        self.memory.clear()
        print("Happy Memorial Day!!!")
