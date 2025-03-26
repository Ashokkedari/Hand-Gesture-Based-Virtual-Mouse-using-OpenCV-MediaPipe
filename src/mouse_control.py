import pyautogui
import numpy as np
import time
from utils.utils import Utils

class VirtualMouse:
    def __init__(self, screen_width=1920, screen_height=1080):
        """Initialize virtual mouse with default screen dimensions."""
        self.screen_width = screen_width  # Ensure this attribute exists
        self.screen_height = screen_height
        self.prev_x, self.prev_y = 0, 0
        self.dragging = False
        self.last_click_time = 0
        self.smooth_factor = 5
        self.drag_start_time = 0
        self.SWIPE_COOLDOWN = 1.0
        self.last_zoom_time = time.time()
        self.last_swipe_time = 0 

        # Mouse action thresholds
        self.CLICK_THRESHOLD = 30
        self.RIGHT_CLICK_THRESHOLD = 40
        self.DRAG_THRESHOLD = 35
        self.SCROLL_THRESHOLD = 20
        self.ZOOM_DELAY = 0.5
        self.SCROLL_SPEED = 30
        self.ZOOM_IN_THRESHOLD = 100
        self.ZOOM_OUT_THRESHOLD = 50
        self.SWIPE_THRESHOLD = 200
        self.DOUBLE_CLICK_INTERVAL = 0.3

        self.prev_click_time = 0
        self.last_zoom_distance = None

    def move_cursor(self, finger_pos, cam_width, cam_height):
        """Move the mouse cursor smoothly based on index finger position."""
        x, y = finger_pos
        screen_x = Utils.map_coordinates(x, (0, cam_width), (0, self.screen_width))
        screen_y = Utils.map_coordinates(y, (0, cam_height), (0, self.screen_height))

        # Apply smoothing to reduce jitter
        self.prev_x, self.prev_y = Utils.smooth_cursor_movement(self.prev_x, self.prev_y, screen_x, screen_y, smooth_factor=3)
        
        pyautogui.moveTo(self.prev_x, self.prev_y, duration=0.05)  # Faster movement



    def click(self, thumb, index_finger, threshold=40):
        """Perform a mouse click if thumb and index finger are close enough."""
        if Utils.calculate_distance(thumb, index_finger) < threshold:
            self.prev_click_time, can_click = Utils.prevent_double_click(self.prev_click_time)
            if can_click:
                pyautogui.click()


    def right_click(self, middle_finger, thumb):
        """Perform a right-click when middle finger & thumb touch."""
        if Utils.calculate_distance(middle_finger, thumb) < self.RIGHT_CLICK_THRESHOLD:
            if self.prevent_double_click():
                pyautogui.rightClick()
    def zoom_in(self):
        current_time = time.time()
        if current_time - self.last_zoom_time > self.ZOOM_DELAY:
            pyautogui.hotkey("ctrl", "+")
            self.last_zoom_time = current_time

    def zoom_out(self):
        current_time = time.time()
        if current_time - self.last_zoom_time > self.ZOOM_DELAY:
            pyautogui.hotkey("ctrl", "-")
            self.last_zoom_time = current_time



    def drag(self, thumb, index_finger):
        """ Drag when thumb and index finger are close together """
        if Utils.calculate_distance(thumb, index_finger) < self.DRAG_THRESHOLD:
            pyautogui.mouseDown()
            pyautogui.mouseUp()

    def scroll(self, index_finger, middle_finger):
        """Scroll up/down based on vertical finger movement."""
        distance = index_finger[1] - middle_finger[1]  # Measure vertical movement
        if abs(distance) > self.SCROLL_THRESHOLD:
            direction = 1 if distance < 0 else -1  # Up if negative, down if positive
            pyautogui.scroll(self.SCROLL_SPEED * direction)



    def swipe(self, palm_base, pinky):
            """Detect left/right swipe with a cooldown to prevent multiple triggers."""
            current_time = time.time()
            if current_time - self.last_swipe_time < self.SWIPE_COOLDOWN:
                return  # Ignore swipes if cooldown is active

            distance = abs(palm_base[0] - pinky[0])  # Horizontal movement
            if distance > self.SWIPE_THRESHOLD:
                if palm_base[0] < pinky[0]:  # Right swipe
                    pyautogui.hotkey("alt", "tab")  # Switch application
                else:  # Left swipe
                    pyautogui.hotkey("ctrl", "shift", "tab")  # Switch browser tab
                
                self.last_swipe_time = current_time  # Update last swipe time


    def prevent_double_click(self):
            """Prevent accidental double clicks by adding a delay between clicks."""
            current_time = time.time()
            if current_time - self.last_click_time > self.DOUBLE_CLICK_INTERVAL:
                self.last_click_time = current_time
                return True
            return False
