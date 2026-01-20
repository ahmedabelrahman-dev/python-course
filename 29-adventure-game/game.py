import tkinter as tk
from tkinter import messagebox, ttk
import random


class AdventureGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Forest Adventure v2.0")
        self.root.geometry("650x650")
        self.root.configure(bg="#121212")

        # Player Data
        self.player = {"health": 100, "gold": 50, "items": []}
        self.current_enemy = None

        # Style Definitions based on your images
        self.bg_color = "#121212"
        self.panel_color = "#1e1e1e"
        self.accent_gold = "#ffcc00"  # Bright Gold border
        self.btn_bg = "#333333"       # Dark Gray button face
        self.btn_fg = "#ffffff"       # Pure White text
        self.btn_hover = "#444444"

        self.setup_ui()
        self.show_town()

    def setup_ui(self):
        # Stats Bar with HP Progress
        self.stats_frame = tk.Frame(
            self.root, bg=self.panel_color, pady=15, padx=20)
        self.stats_frame.pack(fill="x")

        # Health Bar Styling
        self.hp_bar = ttk.Progressbar(
            self.stats_frame, orient="horizontal", length=150, mode="determinate")
        self.hp_bar.pack(side="left", padx=10)
        self.hp_bar["value"] = 100

        self.stats_label = tk.Label(
            self.stats_frame, text=self.get_stats_text(),
            font=("Courier", 11, "bold"), bg=self.panel_color, fg=self.accent_gold
        )
        self.stats_label.pack(side="right")

        # Text Console
        self.text_area = tk.Text(
            self.root, height=10, wrap="word", bg=self.bg_color, fg="#e0e0e0",
            font=("Verdana", 11), padx=30, pady=30, borderwidth=0, highlightthickness=0
        )
        self.text_area.pack(pady=10, padx=20, fill="both", expand=True)
        self.text_area.config(state="disabled")

        # Gold Divider Line
        line = tk.Frame(self.root, height=2, bg=self.accent_gold)
        line.pack(fill="x", padx=50, pady=5)

        # Buttons Container
        self.button_frame = tk.Frame(self.root, bg=self.bg_color, pady=20)
        self.button_frame.pack(fill="x")

    def create_button(self, text, command):
        """Matches the button styling in the uploaded image exactly."""
        # 1. Outer Gold Border Frame
        outer_gold = tk.Frame(
            self.button_frame, bg=self.accent_gold, padx=2, pady=2)
        outer_gold.pack(pady=8)

        # 2. Inner Black Frame (creates the high-contrast gap)
        inner_black = tk.Frame(outer_gold, bg="#000000", padx=2, pady=2)
        inner_black.pack()

        # 3. The Button itself
        btn = tk.Button(
            inner_black,
            text=text,
            command=command,
            width=30,
            bg=self.btn_bg,
            fg=self.btn_fg,
            activebackground=self.accent_gold,
            activeforeground="black",
            font=("Arial", 12, "bold"),
            relief="flat",
            cursor="hand2",
            pady=10,
            bd=0,
            highlightthickness=0
        )
        btn.pack()

        # Hover logic
        btn.bind("<Enter>", lambda e: btn.config(bg=self.btn_hover))
        btn.bind("<Leave>", lambda e: btn.config(bg=self.btn_bg))

    # --- Game Logic ---
    def log(self, text):
        self.text_area.config(state="normal")
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, text)
        self.text_area.config(state="disabled")
        self.update_stats()

    def update_stats(self):
        self.stats_label.config(text=self.get_stats_text())
        self.hp_bar["value"] = self.player["health"]

    def get_stats_text(self):
        items = f"🎒 {len(self.player['items'])} items" if self.player["items"] else "🎒 Empty"
        return f"💰 {self.player['gold']}G | {items} "

    def clear_buttons(self):
        for widget in self.button_frame.winfo_children():
            widget.destroy()

    def show_town(self):
        self.log(
            "🏠 TOWN SQUARE\nYou are back in the safety of the town. What is your next move?")
        self.clear_buttons()
        self.create_button("🛒 Visit the Shop", self.show_shop)
        self.create_button("🌲 Enter the Forest", self.show_forest)
        self.create_button("🛏️ Rest at Inn (10G)", self.rest_at_inn)
        self.create_button("❌ Quit Game", self.root.quit)

    def show_shop(self):
        self.log("🛒 THE SHOP\n'Welcome traveler! Browse my wares.'")
        self.clear_buttons()
        self.create_button("🧪 Health Potion (20G)",
                           lambda: self.buy_item("health potion", 20))
        self.create_button("⚔️ Sharp Sword (50G)",
                           lambda: self.buy_item("sword", 50))
        self.create_button("🚶 Back to Town", self.show_town)

    def show_forest(self):
        self.log(
            "🌲 THE DEEP FOREST\nThe trees whisper as you enter. Danger could be anywhere.")
        self.clear_buttons()
        self.create_button("🔍 Explore Deeper", self.explore_logic)
        self.create_button("⛺ Set up Camp (+10 HP)", self.camp_logic)
        self.create_button("🏠 Return to Town", self.show_town)

    def buy_item(self, item, price):
        if self.player["gold"] >= price:
            if item == "sword" and "sword" in self.player["items"]:
                self.log("You already own a sword!")
            else:
                self.player["gold"] -= price
                self.player["items"].append(item)
                self.log(f"✅ Purchased {item.capitalize()}!")
        else:
            self.log("❌ Not enough gold!")
        self.root.after(1000, self.show_shop)

    def rest_at_inn(self):
        if self.player["gold"] >= 10:
            self.player["gold"] -= 10
            self.player["health"] = 100
            self.log("✨ Fully rested! HP restored to 100.")
        else:
            self.log("❌ You can't afford a room.")
        self.root.after(1000, self.show_town)

    def camp_logic(self):
        self.player["health"] = min(100, self.player["health"] + 10)
        self.log("🔥 You rest by the fire. +10 HP.")
        self.root.after(1000, self.show_forest)

    def explore_logic(self):
        roll = random.random()
        if roll < 0.6:
            self.start_combat()
        elif roll < 0.9:
            gold = random.randint(15, 40)
            self.player["gold"] += gold
            self.log(f"💰 Found a pouch with {gold} gold!")
            self.root.after(1500, self.show_forest)
        else:
            self.log("The forest remains still...")
            self.root.after(1500, self.show_forest)

    def start_combat(self):
        self.current_enemy = random.choice([
            {"name": "Shadow Goblin", "hp": 30, "atk": 8, "gold": 20},
            {"name": "Dire Wolf", "hp": 25, "atk": 12, "gold": 15},
            {"name": "Bandit Leader", "hp": 50, "atk": 15, "gold": 45}
        ])
        self.update_combat_screen()

    def update_combat_screen(self):
        self.log(
            f"⚔️ FIGHT!\nA {self.current_enemy['name']} attacks!\nEnemy HP: {self.current_enemy['hp']}")
        self.clear_buttons()
        self.create_button("⚔️ Attack Enemy", self.attack_logic)
        if "health potion" in self.player["items"]:
            self.create_button("🧪 Drink Potion", self.use_potion_combat)
        self.create_button("🏃 Run Away", self.run_logic)

    def attack_logic(self):
        dmg = 10 + (10 if "sword" in self.player["items"] else 0)
        self.current_enemy["hp"] -= dmg
        if self.current_enemy["hp"] <= 0:
            self.player["gold"] += self.current_enemy["gold"]
            self.log(f"🏆 VICTORY! Gained {self.current_enemy['gold']} gold.")
            self.root.after(1500, self.show_forest)
        else:
            self.player["health"] -= self.current_enemy["atk"]
            if self.player["health"] <= 0:
                self.game_over()
            else:
                self.update_combat_screen()

    def use_potion_combat(self):
        self.player["items"].remove("health potion")
        self.player["health"] = min(100, self.player["health"] + 30)
        self.log("🧪 Restored 30 HP!")
        self.update_combat_screen()

    def run_logic(self):
        if random.random() > 0.5:
            self.log("🏃 You managed to flee!")
            self.root.after(1000, self.show_forest)
        else:
            self.player["health"] -= 10
            self.log("⚠️ Failed to flee! You take 10 damage.")
            if self.player["health"] <= 0:
                self.game_over()
            else:
                self.update_combat_screen()

    def game_over(self):
        messagebox.showinfo("Game Over", "You have fallen in the woods...")
        self.player = {"health": 100, "gold": 50, "items": []}
        self.show_town()


if __name__ == "__main__":
    root = tk.Tk()
    game = AdventureGame(root)
    root.mainloop()
