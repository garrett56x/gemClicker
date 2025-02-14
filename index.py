import time
import pyautogui
from PIL import Image
import numpy as np
import cv2
import random
import threading
from datetime import datetime, timedelta
import pytz
import tkinter as tk
from tkinter import scrolledtext, ttk

# Game window values test
screen_x = 0
screen_y = 65
screen_width = 635
screen_height = 915

button_image_path = "./img/button.png"
button_image = Image.open(button_image_path)

button_total = 0
running = False

pst = pytz.timezone('America/Los_Angeles')

def find_and_click_button():
    screenshot = pyautogui.screenshot(region=(screen_x, screen_y, screen_width, screen_height))
    screenshot = np.array(screenshot)

    button_image_np = np.array(button_image)
    result = cv2.matchTemplate(screenshot, button_image_np, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val > 0.85:
        button_x, button_y = max_loc
        click_x = screen_x + button_x + button_image.width // 2
        click_y = screen_y + button_y + button_image.height // 2

        offset_x = random.randint(-5, 5)
        offset_y = random.randint(-5, 5)

        click_x += offset_x
        click_y += offset_y

        pyautogui.moveTo(click_x, click_y, duration=0.1)
        pyautogui.doubleClick()

        return True
    return False

def automation_loop():
    global button_total, running

    while running:
        clicked = find_and_click_button()
        current_time = datetime.now(pst).strftime("%I:%M:%S %p")

        if clicked:
            sleep_time = random.randint(9 * 60, 11 * 60)
            button_total += 5
            update_ui(f"[{current_time}] Clicked! Gems collected: {button_total}")
        else:
            sleep_time = random.randint(30, 90)
            update_ui(f"[{current_time}] No button found. Sleeping...")

        update_gem_count()
        wake_time = (datetime.now(pst) + timedelta(seconds=sleep_time)).strftime("%I:%M:%S %p")
        update_ui(f"[{current_time}] Sleeping until {wake_time}.\n")

        time.sleep(sleep_time)

def start_automation():
    global running
    if not running:
        running = True
        threading.Thread(target=automation_loop, daemon=True).start()
        update_ui("Automation started.")

def stop_automation():
    global running
    running = False
    update_ui("Automation stopped.")

def update_ui(message):
    log_text.insert(tk.END, message + "\n")
    log_text.yview(tk.END)  # Auto-scroll

def update_gem_count():
    gem_count_label.config(text=f"Gems Collected: {button_total}")

root = tk.Tk()
root.title("Gem Clicker")
root.geometry("400x400")

style = ttk.Style()
style.theme_use("clam")

style.layout("TStartButton", [
    ("Button.border", {"children": [
        ("Button.padding", {"children": [
            ("Button.label", {"sticky": "nswe"})
        ]})
    ]})
])
style.configure("TStartButton", font=("Arial", 12, "bold"), padding=10, background="green", foreground="white")
style.map("TStartButton",
          foreground=[("pressed", "white"), ("active", "black")],
          relief=[("pressed", "sunken"), ("active", "raised")])

style.layout("TStopButton", [
    ("Button.border", {"children": [
        ("Button.padding", {"children": [
            ("Button.label", {"sticky": "nswe"})
        ]})
    ]})
])
style.configure("TStopButton", font=("Arial", 12, "bold"), padding=10, background="red", foreground="white")
style.map("TStopButton",
          foreground=[("pressed", "white"), ("active", "black")],
          relief=[("pressed", "sunken"), ("active", "raised")])


start_button = ttk.Button(root, text="Start", command=start_automation, style="TStartButton")
start_button.pack(pady=10)

stop_button = ttk.Button(root, text="Stop", command=stop_automation, style="TStopButton")
stop_button.pack(pady=5)

gem_count_label = tk.Label(root, text="Gems Collected: 0", font=("Arial", 14, "bold"))
gem_count_label.pack(pady=10)

log_text = scrolledtext.ScrolledText(root, height=10, width=50, font=("Arial", 10))
log_text.pack(pady=10)

root.mainloop()
