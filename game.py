import tkinter as tk
import random
from ai import SwordAI

class SwordGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Swordfighter AI")
        
        # Boot sequence
        print("LOAD gameai")
        print("RUN gameai")
        try:
            self.level_names = ["Beginner", "noob", "eh?", "Medium", "hard", "GRANDMASTER", "Matt the master!"]
            self.current_idx = 0
            self.brain = SwordAI(self.level_names[self.current_idx])
            print(f"Loaded AI Module [{self.level_names[self.current_idx]}]")
        except Exception as e:
            print(f"Failed to load program! Details: {e}")
            return # closes the game if loading fails

        self.canvas = tk.Canvas(root, width=800, height=400, bg="#111", highlightthickness=0)
        self.canvas.pack()
        
        # player and weapon
        self.player = self.canvas.create_rectangle(100, 200, 150, 320, fill="#001b2e", outline="white")
        self.player_sword = self.canvas.create_line(0, 0, 0, 0, fill="silver", width=3)
        self.enemy = self.canvas.create_rectangle(650, 200, 700, 320, fill="#300500", outline="white")
        self.enemy_sword = self.canvas.create_line(0, 0, 0, 0, fill="silver", width=3)

        # state+hud
        self.is_attacking = False
        self.info = self.canvas.create_text(400, 30, text=f"Opponent: {self.level_names[self.current_idx]}", fill="white", font=("Courier", 14))
        self.msg = self.canvas.create_text(400, 350, text="", fill="yellow", font=("Courier", 18, "bold"))

        #controls
        self.root.bind("<Left>", lambda e: self.move_player(-15))
        self.root.bind("<Right>", lambda e: self.move_player(15))
        self.root.bind("<space>", lambda e: self.perform_attack())
        self.root.bind("<Tab>", self.cycle_difficulty)
        self.root.bind("<Escape>", lambda e: self.exit_game())
        print("listening for user input...")
        self.game_loop()

    def show_message(self, text, color):
        # update screen GUI
        self.canvas.itemconfig(self.msg, text=text, fill=color)
        #update debug color
        print(f"[GAME EVENT]: {text}")
        
        self.root.after(1000, lambda: self.canvas.itemconfig(self.msg, text=""))

    def update_swords(self):
        p = self.canvas.coords(self.player)
        e = self.canvas.coords(self.enemy)
        off = 50 if self.is_attacking else 20
        self.canvas.coords(self.player_sword, p[2], p[1]+50, p[2]+off, p[1]+50)
        self.canvas.coords(self.enemy_sword, e[0], e[1]+50, e[0]-20, e[1]+50)

    def move_player(self, dx):
        if not self.is_attacking:
            self.canvas.move(self.player, dx, 0)
            self.update_swords()

    def perform_attack(self):
        if self.is_attacking: return
        self.is_attacking = True
        print("[INPUT]: Spacebar pressed - Player Lunge")
        self.canvas.move(self.player, 25, 0) 
        
        p_x = self.canvas.coords(self.player)[2]
        e_x = self.canvas.coords(self.enemy)[0]
        dist = abs(e_x - p_x)

        delay = self.brain.get_stats()[0]
        self.root.after(delay, lambda: self.resolve_hit(dist))

    def resolve_hit(self, dist):
        res = self.brain.decide_reaction("attack", dist)
        if "parry" in res:
            print(f"[AI]: Opponent parried! Reaction: {res}")
            self.shake_screen()
            self.canvas.itemconfig(self.enemy, fill="yellow")
            if "counter" in res: 
                self.root.after(50, self.enemy_lunge)
        elif res == "get_hit":
            if dist < 60: 
                self.canvas.itemconfig(self.enemy, fill="#500")
                self.show_message("You hit the enemy!", "#ff00e1")
            else:
                print("[GAME]: Attack missed (Too far)")

        self.root.after(200, self.reset_combat)

    def enemy_lunge(self):
        print("[AI]: Executing Counter-Attack!")
        self.canvas.move(self.enemy, -60, 0)
        
        p_x = self.canvas.coords(self.player)[2]
        e_x = self.canvas.coords(self.enemy)[0]
        
        if abs(e_x - p_x) < 40:
            self.show_message("The enemy hit you!", "#e74c3c")
            self.canvas.itemconfig(self.player, fill="red")
            self.root.after(200, lambda: self.canvas.itemconfig(self.player, fill="#3498db"))

        self.root.after(200, lambda: self.canvas.move(self.enemy, 60, 0))

    def reset_combat(self):
        self.canvas.move(self.player, -25, 0)
        self.canvas.itemconfig(self.enemy, fill="#e74c3c")
        self.is_attacking = False
        self.update_swords()

    def game_loop(self):
        p_x = self.canvas.coords(self.player)[0]
        e_x = self.canvas.coords(self.enemy)[0]
        speed = self.brain.get_stats()[3]
        
        if not self.is_attacking:
            if e_x > p_x + 130: self.canvas.move(self.enemy, -speed, 0)
            elif e_x < p_x + 90: self.canvas.move(self.enemy, speed, 0)
        
        self.update_swords()
        self.root.after(30, self.game_loop)

    def shake_screen(self):
        for i in range(4):
            self.root.after(i*15, lambda: self.canvas.move("all", 5, 0))
            self.root.after(i*15+7, lambda: self.canvas.move("all", -5, 0))

    def cycle_difficulty(self, e):
        self.current_idx = (self.current_idx + 1) % len(self.level_names)
        self.brain = SwordAI(self.level_names[self.current_idx])
        self.canvas.itemconfig(self.info, text=f"Opponent: {self.level_names[self.current_idx]}")
        print(f"[SYSTEM]: Difficulty changed to {self.level_names[self.current_idx]}")

root = tk.Tk()
SwordGame(root)
root.mainloop()