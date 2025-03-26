
import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, mode=False, max_hands=2, detection_conf=0.5, tracking_conf=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_conf = detection_conf
        self.tracking_conf = tracking_conf

        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_conf,
            min_tracking_confidence=self.tracking_conf
        )
        self.mp_draw = mp.solutions.drawing_utils  # For drawing landmarks

    def detect_hands(self, frame):
        """Detects hands in the given frame and returns landmarks."""
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
        results = self.hands.process(frame_rgb)  # Process the frame

        landmarks_list = []
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                hand_points = []
                for idx, lm in enumerate(hand_landmarks.landmark):
                    h, w, c = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    hand_points.append((cx, cy))
                
                landmarks_list.append(hand_points)
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

        return frame, landmarks_list  # Return processed frame & detected landmarks
