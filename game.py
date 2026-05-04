import tkinter as tk
import random
from ai import SwordAI

class SwordGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Swordfighter AI: Python Edition")
        
        self.level_names = ["Beginner", "noob", "eh?", "Medium", "hard", "GRANDMASTER", "Matt the master!"]
        self.current_idx = 0
        self.brain = SwordAI(self.level_names[self.current_idx])

        self.canvas = tk.Canvas(root, width=800, height=400, bg="#111", highlightthickness=0)
        self.canvas.pack()
        
        # Players & Swords
        self.player = self.canvas.create_rectangle(100, 200, 150, 320, fill="#3498db", outline="white")
        self.player_sword = self.canvas.create_line(0, 0, 0, 0, fill="silver", width=3)
        self.enemy = self.canvas.create_rectangle(650, 200, 700, 320, fill="#e74c3c", outline="white")
        self.enemy_sword = self.canvas.create_line(0, 0, 0, 0, fill="silver", width=3)

        # State & HUD
        self.is_attacking = False
        self.info = self.canvas.create_text(400, 30, text=f"Opponent: {self.level_names[self.current_idx]}", fill="white", font=("Courier", 14))

        # Controls
        self.root.bind("<Left>", lambda e: self.move_player(-15))
        self.root.bind("<Right>", lambda e: self.move_player(15))
        self.root.bind("<space>", lambda e: self.perform_attack())
        self.root.bind("<Tab>", self.cycle_difficulty)

        self.game_loop()

    def update_swords(self):
        p = self.canvas.coords(self.player)
        e = self.canvas.coords(self.enemy)
        # Player Sword (Offset for attack)
        off = 50 if self.is_attacking else 20
        self.canvas.coords(self.player_sword, p[2], p[1]+50, p[2]+off, p[1]+50)
        # Enemy Sword
        self.canvas.coords(self.enemy_sword, e[0], e[1]+50, e[0]-20, e[1]+50)

    def move_player(self, dx):
        if not self.is_attacking:
            self.canvas.move(self.player, dx, 0)
            self.update_swords()

    def perform_attack(self):
        if self.is_attacking: return
        self.is_attacking = True
        self.canvas.move(self.player, 25, 0) # Lunge
        
        p_x = self.canvas.coords(self.player)[2]
        e_x = self.canvas.coords(self.enemy)[0]
        dist = abs(e_x - p_x)

        # AI Reaction using imported stats
        delay = self.brain.get_stats()[0]
        self.root.after(delay, lambda: self.resolve_hit(dist))

    def resolve_hit(self, dist):
        res = self.brain.decide_reaction("attack", dist)
        if "parry" in res:
            self.shake_screen()
            self.canvas.itemconfig(self.enemy, fill="yellow")
            if "counter" in res: self.root.after(50, self.enemy_lunge)
        elif res == "get_hit":
            self.canvas.itemconfig(self.enemy, fill="#500")

        self.root.after(200, self.reset_combat)

    def enemy_lunge(self):
        self.canvas.move(self.enemy, -50, 0)
        self.root.after(200, lambda: self.canvas.move(self.enemy, 50, 0))

    def reset_combat(self):
        self.canvas.move(self.player, -25, 0)
        self.canvas.itemconfig(self.enemy, fill="#e74c3c")
        self.is_attacking = False
        self.update_swords()

    def game_loop(self):
        # AI Chase Logic
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

root = tk.Tk()
SwordGame(root)
root.mainloop()