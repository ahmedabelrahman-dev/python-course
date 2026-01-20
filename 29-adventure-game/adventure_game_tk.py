import tkinter as tk
from tkinter import messagebox
import random

# ================= GAME DATA =================

player = {"name": "", "health": 100, "gold": 50, "items": []}

items = {
    "health potion": {"health": 30, "price": 20},
    "sword": {"damage": 10, "price": 50},
}

enemies = [
    {"name": "Goblin", "health": 30, "damage": 5, "gold": 15},
    {"name": "Wolf", "health": 20, "damage": 7, "gold": 10},
    {"name": "Bandit", "health": 40, "damage": 8, "gold": 25},
]

# ================= WINDOW =================

root = tk.Tk()
root.title("🌲 Forest Adventure")
root.geometry("780x560")
root.configure(bg="#0f0f0f")
root.resizable(False, False)

FONT_TITLE = ("Helvetica", 20, "bold")
FONT_TEXT = ("Helvetica", 11)
FONT_BTN = ("Helvetica", 13, "bold")

# ================= UI =================

tk.Label(
    root,
    text="🏆 FOREST ADVENTURE 🏆",
    font=FONT_TITLE,
    fg="#f5c542",
    bg="#0f0f0f",
).pack(pady=10)

stats_label = tk.Label(root, fg="#ddd", bg="#0f0f0f", font=FONT_TEXT)
stats_label.pack()

log_box = tk.Text(
    root,
    height=14,
    bg="#111",
    fg="#eee",
    font=FONT_TEXT,
    wrap="word",
    bd=0,
)
log_box.pack(padx=12, pady=10, fill="both", expand=True)
log_box.config(state="disabled")

button_frame = tk.Frame(root, bg="#0f0f0f")
button_frame.pack(pady=10)

# ================= HELPERS =================


def log(msg):
    log_box.config(state="normal")
    log_box.insert("end", msg + "\n")
    log_box.see("end")
    log_box.config(state="disabled")


def update_stats():
    items_txt = ", ".join(player["items"]) if player["items"] else "None"
    stats_label.config(
        text=f"👤 {player['name']}   ❤️ {player['health']}   💰 {player['gold']}   🎒 {items_txt}"
    )


def clear_buttons():
    for w in button_frame.winfo_children():
        w.destroy()

# ================= CUSTOM DARK BUTTON =================


def game_button(text, command):
    canvas = tk.Canvas(
        button_frame,
        width=360,
        height=48,
        bg="#0f0f0f",
        highlightthickness=0,
    )
    canvas.pack(pady=6)

    rect = canvas.create_rectangle(
        4, 4, 356, 44,
        fill="#1c1c1c",
        outline="#2f2f2f",
        width=2,
    )

    label = canvas.create_text(
        180, 24,
        text=text,
        fill="#ffffff",
        font=FONT_BTN,
    )

    def hover_on(_):
        canvas.itemconfig(rect, fill="#2a2a2a")

    def hover_off(_):
        canvas.itemconfig(rect, fill="#1c1c1c")

    def click(_):
        command()

    canvas.bind("<Enter>", hover_on)
    canvas.bind("<Leave>", hover_off)
    canvas.bind("<Button-1>", click)
    canvas.tag_bind(label, "<Button-1>", click)

# ================= GAME FLOW =================


def start_game():
    clear_buttons()
    log_box.config(state="normal")
    log_box.delete("1.0", "end")
    log_box.config(state="disabled")

    player.update({"health": 100, "gold": 50, "items": []})

    log("🎮 Welcome to Forest Adventure")
    log("Enter your name:")

    name_entry = tk.Entry(
        button_frame,
        font=("Helvetica", 13),
        bg="#111",
        fg="#fff",
        insertbackground="#fff",
        relief="flat",
        width=28,
    )
    name_entry.pack(pady=12)

    def submit():
        name = name_entry.get().strip()
        if not name:
            messagebox.showwarning("Name required", "Please enter your name")
            return
        player["name"] = name
        log(f"✨ Welcome, {name}!")
        town()

    game_button("▶ Start Adventure", submit)


def town():
    clear_buttons()
    update_stats()
    log("\n🏠 You are in the town.")

    game_button("🛒 Go to Shop", shop)
    game_button("🌲 Enter Forest", forest)
    game_button("🛏️ Rest at Inn (10 gold)", rest)
    game_button("👋 Quit Game", root.quit)


def shop():
    clear_buttons()
    update_stats()
    log("\n🛒 You enter the shop.")

    game_button("🧪 Buy Health Potion (20g)", lambda: buy_item("health potion"))
    game_button("⚔️ Buy Sword (50g)", lambda: buy_item("sword"))
    game_button("↩️ Return to Town", town)


def buy_item(item):
    if item in player["items"] and item != "health potion":
        log("❌ You already own this.")
        return
    if player["gold"] < items[item]["price"]:
        log("❌ Not enough gold.")
        return

    player["gold"] -= items[item]["price"]
    if item not in player["items"]:
        player["items"].append(item)

    log(f"✅ Bought {item}")
    update_stats()


def forest():
    clear_buttons()
    update_stats()
    log("\n🌲 You enter the forest.")

    game_button("🔍 Explore", explore)
    game_button("⛺ Camp (+10 HP)", camp)
    game_button("↩️ Return to Town", town)


def camp():
    player["health"] = min(100, player["health"] + 10)
    log("😌 You feel rested.")
    update_stats()


def explore():
    event = random.ch
