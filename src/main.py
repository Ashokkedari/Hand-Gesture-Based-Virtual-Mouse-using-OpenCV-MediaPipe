import cv2
import mediapipe as mp
import numpy as np
from mouse_control import VirtualMouse
from utils import Utils

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# Initialize VirtualMouse
virtual_mouse = VirtualMouse()
prev_thumb_state = "neutral"
ZOOM_THRESHOLD=40
SCREEN_WIDTH = 2000
SCREEN_HEIGHT = 1400
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

cap = cv2.VideoCapture(0)
cap.set(3, CAMERA_WIDTH)
cap.set(4, CAMERA_HEIGHT)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip image for natural interaction
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # Convert image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Extract key fingertip positions
            index_finger = Utils.get_landmark_position(hand_landmarks, mp_hands.HandLandmark.INDEX_FINGER_TIP, w, h)
            middle_finger = Utils.get_landmark_position(hand_landmarks, mp_hands.HandLandmark.MIDDLE_FINGER_TIP, w, h)
            thumb = Utils.get_landmark_position(hand_landmarks, mp_hands.HandLandmark.THUMB_TIP, w, h)
            ring_finger = Utils.get_landmark_position(hand_landmarks, mp_hands.HandLandmark.RING_FINGER_TIP, w, h)
            pinky = Utils.get_landmark_position(hand_landmarks, mp_hands.HandLandmark.PINKY_TIP, w, h)
            wrist = Utils.get_landmark_position(hand_landmarks, mp_hands.HandLandmark.WRIST, w, h)
            palm_base = Utils.get_landmark_position(hand_landmarks, mp_hands.HandLandmark.WRIST, w, h)

            # Draw fingertip markers with colors
            if index_finger:
                cv2.circle(frame, index_finger, 10, (0, 255, 0), -1)  # Green (Index)
            if middle_finger:
                cv2.circle(frame, middle_finger, 10, (0, 165, 255), -1)  # Orange (Middle)
            if thumb:
                cv2.circle(frame, thumb, 10, (255, 0, 0), -1)  # Blue (Thumb)

            # Perform gestures based on colored fingertips
            if index_finger:
                virtual_mouse.move_cursor(index_finger, w, h)

            # Left Click (Index + Thumb)
            if thumb and index_finger:
                if Utils.calculate_distance(thumb, index_finger) < 35:
                    virtual_mouse.click(thumb, index_finger)

            # Drag (Index + Thumb)
            if thumb and index_finger:
                if Utils.calculate_distance(thumb, index_finger) < 30:
                    virtual_mouse.drag(thumb, index_finger)

            # Scroll Gesture (Index & Middle Finger)
            if index_finger and middle_finger:
                virtual_mouse.scroll(index_finger, middle_finger)

            # Right Click (Thumb + Ring Finger)
            if thumb and ring_finger:
                if Utils.calculate_distance(thumb, ring_finger) < 30:  # Adjusted threshold
                    virtual_mouse.right_click(thumb, ring_finger)

            # Swipe Gesture (Palm Base & Pinky)
            if palm_base and pinky:
                virtual_mouse.swipe(palm_base, pinky)

            if thumb and wrist:
                thumb_y = thumb[1]  # Thumb vertical position
                wrist_y = wrist[1]  # Wrist vertical position

                # Detect Zoom Out (Thumb Down)
                if thumb_y > wrist_y + ZOOM_THRESHOLD:
                    if prev_thumb_state != "down":  # Only trigger on state change
                        virtual_mouse.zoom_out()
                        prev_thumb_state = "down"
                elif thumb_y < wrist_y - ZOOM_THRESHOLD:
                    if prev_thumb_state != "up":  # Only trigger on state change
                        virtual_mouse.zoom_in()
                        prev_thumb_state = "up"

                # Reset state when thumb is in neutral position
                else:
                    prev_thumb_state = "neutral"


    # Display the frame
    cv2.imshow("Virtual Mouse", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
