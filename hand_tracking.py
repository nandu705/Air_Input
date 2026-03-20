import cv2
import mediapipe as mp


class HandTracker:
    def __init__(self, max_hands=1, detection_conf=0.7, track_conf=0.7):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=detection_conf,
            min_tracking_confidence=track_conf
        )
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

        return img

    def get_positions(self, img):
        lm_list = []
        hand_label = None
        if self.results.multi_hand_landmarks:
            # take the first detected hand
            hand = self.results.multi_hand_landmarks[0]
            for id, lm in enumerate(hand.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])

            # get handedness if available
            if self.results.multi_handedness:
                try:
                    hand_label = self.results.multi_handedness[0].classification[0].label
                except Exception:
                    hand_label = None

        return lm_list, hand_label
