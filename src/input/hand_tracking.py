import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, max_hands=2, detection_conf=0.7, tracking_conf=0.7):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False, # Otimizado para vídeo
            max_num_hands=max_hands,
            min_detection_confidence=detection_conf,
            min_tracking_confidence=tracking_conf
        )
        self.mp_draw = mp.solutions.drawing_utils

    def detect(self, frame, draw=True):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        all_hands = []

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                h, w, _ = frame.shape
                landmarks = []
                for lm in hand_landmarks.landmark:
                    # Mantemos x e y em pixels para o desenho, 
                    # mas guardamos o z nativo para cálculos 3D
                    cx, cy, cz = int(lm.x * w), int(lm.y * h), lm.z
                    landmarks.append((cx, cy, cz))

                all_hands.append(landmarks)
                if draw:
                    self.mp_draw.draw_landmarks(
                        frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                    )

        return all_hands, frame