import cv2
import mediapipe as mp

class PoseDetector:
    """Handles pose estimation using MediaPipe."""
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils

    def process(self, frame):
        """Processes a frame and returns pose landmarks."""
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(img_rgb)
        return results.pose_landmarks

    def draw(self, frame, landmarks):
        """Draws pose landmarks and connections on the frame."""
        if landmarks:
            self.mp_draw.draw_landmarks(
                frame, landmarks, self.mp_pose.POSE_CONNECTIONS
            )
