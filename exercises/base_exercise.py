from abc import ABC, abstractmethod
import mediapipe as mp

class BaseExercise(ABC):
    """Abstract base class for all exercises."""
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.counter = 0
        self.stage = None
        self.feedback = ""

    @abstractmethod
    def analyze(self, landmarks):
        """Analyzes landmarks and returns results."""
        pass

    def get_landmarks_array(self, landmarks):
        """Converts MediaPipe landmarks to a list of [x, y] coordinates."""
        return [[lm.x, lm.y] for lm in landmarks.landmark]
