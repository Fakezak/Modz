import pyautogui
import time
import numpy as np
import cv2

# Screen dimensions (for the auto headshot to work)
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

# Define the area to track the player (using a color or pattern)
# For simplicity, we'll use a color-based tracking method for headshot detection.
TARGET_COLOR = (255, 0, 0)  # Red, adjust to the color of the enemy's head

# Function to simulate no recoil by adjusting mouse position
def no_recoil():
    # You can tweak these values to simulate recoil correction
    pyautogui.moveRel(0, -5, duration=0.1)  # Adjust the Y-axis to counter recoil

# Function to find enemy head position using color tracking
def find_enemy_head():
    # Capture a screenshot
    screenshot = pyautogui.screenshot()
    img = np.array(screenshot)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Convert to HSV for better color detection
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define color range for red (you may need to tweak this)
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])

    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Find the position of the red color (head)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        # Get the bounding box of the detected contour
        x, y, w, h = cv2.boundingRect(largest_contour)
        center_x = x + w // 2
        center_y = y + h // 2
        return center_x, center_y
    return None

# Main function
def auto_headshot():
    while True:
        # Find enemy head position
        enemy_pos = find_enemy_head()

        if enemy_pos:
            target_x, target_y = enemy_pos
            # Move the cursor to the target position
            pyautogui.moveTo(target_x, target_y, duration=0.1)
            pyautogui.click()
            no_recoil()
        time.sleep(0.1)

if __name__ == "__main__":
    auto_headshot()
    