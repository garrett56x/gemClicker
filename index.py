import time
import pyautogui
from PIL import Image
import numpy as np
import cv2
import random
from datetime import datetime, timedelta
import pytz

# Game window values
screen_x = 0
screen_y = 65
screen_width = 635
screen_height = 915

# screen shot of button
# screen_x = 70
# screen_y = 745
# screen_width = 120
# screen_height = 75

button_image_path = "./img/button.png"
button_image = Image.open(button_image_path)

button_total = 0
floater_total = 0

pst = pytz.timezone('America/Los_Angeles')

def find_and_click_button():    
    screenshot = pyautogui.screenshot(region=(screen_x, screen_y, screen_width, screen_height))
    # screenshot.save("screenshot.png")
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
    else:
        return False

try:
    while True:
        clicked = find_and_click_button()
        current_time = datetime.now(pst).strftime("%I:%M:%S %p")

        if clicked:
            sleep_time = random.randint(9 * 60, 11 * 60)
            button_total += 5
            print(f"[{current_time}] {button_total + floater_total} gems collected so far!")
        else:
            sleep_time = random.randint(30, 90)

        wake_time = (datetime.now(pst) + timedelta(seconds=sleep_time)).strftime("%I:%M:%S %p")
        print(f"[{current_time}] Sleeping until {wake_time}.")

        time.sleep(sleep_time)

except KeyboardInterrupt:
    print(f"\n\n*********************************************")
    print(f"*********************************************\n")
    print(f"Automation complete. Gems collected: {button_total + floater_total}.")
    print(f"\n*********************************************")
    print(f"*********************************************\n\n")
