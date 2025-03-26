
import numpy as np
import time

class Utils:
    @staticmethod
    def calculate_distance(pt1, pt2):
        if pt1 is None or pt2 is None:
            return float('inf')  # Return a large number instead of crashing
        try:
            return np.linalg.norm(np.array(pt1, dtype=np.float32) - np.array(pt2, dtype=np.float32))
        except Exception as e:
            print(f"Distance Calculation Error: {e}, pt1: {pt1}, pt2: {pt2}")
            return float('inf')

    @staticmethod
    def smooth_cursor_movement(prev_x: float, prev_y: float, 
                               target_x: float, target_y: float, 
                               smooth_factor: int = 5) -> tuple:
        """Apply weighted smoothing to cursor movement."""
        smoothed_x = (prev_x * (smooth_factor - 1) + target_x) / smooth_factor
        smoothed_y = (prev_y * (smooth_factor - 1) + target_y) / smooth_factor
        return smoothed_x, smoothed_y

    @staticmethod
    def map_coordinates(value, from_range: tuple, to_range: tuple):
        """Map a value or list from one range to another (used for screen mapping)."""
        return np.interp(value, from_range, to_range)

    @staticmethod
    def prevent_double_click(last_click_time: float, interval: float = 0.3) -> tuple:
        """Prevent accidental double clicks by enforcing a time delay."""
        current_time = time.time()
        return (current_time, True) if current_time - last_click_time > interval else (last_click_time, False)
    @staticmethod
    def get_landmark_position(hand_landmarks, landmark, img_width, img_height):
        """Extract (x, y) position of a given hand landmark and scale to image size."""
        if hand_landmarks is None:
            return None
        lm = hand_landmarks.landmark[landmark]
        return int(lm.x * img_width), int(lm.y * img_height)
    












