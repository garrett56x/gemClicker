import time
import pyautogui
from PIL import Image
import numpy as np
import cv2
import matplotlib.pyplot as plt
import random

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

# Load the button reference image
button_image_path = "./button.png"
button_image = Image.open(button_image_path)
count = 0

# Function to capture the screen and look for the button
def find_and_click_button():
    global count
    # Take a screenshot of the game area
    screenshot = pyautogui.screenshot(region=(screen_x, screen_y, screen_width, screen_height))
    screenshot.save("screenshot.png")
    screenshot = np.array(screenshot)  # Convert to NumPy array (OpenCV uses this format)

    # Convert button image to NumPy array
    button_image_np = np.array(button_image)

    # Perform template matching to find the button image in the screenshot
    result = cv2.matchTemplate(screenshot, button_image_np, cv2.TM_CCOEFF_NORMED)

    # Get the best match location (highest correlation)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # print("Max Val: ", max_val)
    # If a good match is found, click it
    if max_val > 0.85:  # Adjust threshold if needed
        button_x, button_y = max_loc
        click_x = screen_x + button_x + button_image.width // 2
        click_y = screen_y + button_y + button_image.height // 2

        pyautogui.moveTo(click_x, click_y, duration=0.1)
        pyautogui.doubleClick()

        count += 5
        return True
    else:
        print("Button not found.")
        return False

try:
    while True:
        clicked = find_and_click_button()

        if clicked:
            # If the button was found, reset to the full interval
            sleep_time = random.randint(15 * 60, 17 * 60)
        else:
            # If the button was NOT found, retry after 1-2 minutes
            sleep_time = random.randint(1 * 60, 2 * 60)

        print(f"Sleeping for {sleep_time / 60:.2f} minutes before the next check.")

        if count % 5 == 0:
            print(f"{count} gems collected so far!")

        time.sleep(sleep_time)

except KeyboardInterrupt:
    # Convert count to an integer to remove decimals
    count_int = int(count)

    # Calculate the width of the total line
    count_length = len(str(count_int))
    line_length = 55  # Adjust this based on how wide you want the border to be
    message = f"***  Automation complete. Total gems collected: {count_int}!  ***"
    message_length = len(message)

    # Calculate the padding on both sides to center the message
    padding_length = (line_length - message_length) // 2

    # Create the formatted lines
    border_line = "*" * line_length
    padded_message_line = " " * padding_length + message

    # Print the message with the border
    print(f"\n\n{border_line}")
    print(padded_message_line)
    print(border_line)
    print("\n\n")
