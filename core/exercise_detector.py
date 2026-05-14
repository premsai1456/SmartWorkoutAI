import mediapipe as mp
from core.angle_utils import calculate_angle

class ExerciseDetector:
    """Detects specific exercises and counts repetitions."""
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.counter = 0
        self.stage = None
        self.current_exercise = "Bicep Curl"

    def detect(self, landmarks):
        """
        Classifies the current exercise based on pose landmarks.
        Returns: "Bicep Curl" or "Shoulder Press"
        """
        if not landmarks:
            return self.current_exercise
            
        lms = landmarks.landmark
        
        # Extract key points for classification
        l_hip = [lms[self.mp_pose.PoseLandmark.LEFT_HIP.value].x, lms[self.mp_pose.PoseLandmark.LEFT_HIP.value].y]
        l_shoulder = [lms[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, lms[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        l_elbow = [lms[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].x, lms[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        
        # Calculate shoulder angle to distinguish exercises
        # Bicep Curl: Arm at side (small angle)
        # Shoulder Press: Arm raised (large angle)
        shoulder_angle = calculate_angle(l_hip, l_shoulder, l_elbow)
        
        if shoulder_angle < 45:
            self.current_exercise = "Bicep Curl"
        elif shoulder_angle > 70:
            self.current_exercise = "Shoulder Press"
            
        return self.current_exercise

    def process_rep(self, landmarks):
        """Processes landmarks to count repetitions for the detected exercise."""
        if not landmarks:
            return self.counter, self.stage
            
        lms = landmarks.landmark
        l_shoulder = [lms[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, lms[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        l_elbow = [lms[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].x, lms[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        l_wrist = [lms[self.mp_pose.PoseLandmark.LEFT_WRIST.value].x, lms[self.mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        l_hip = [lms[self.mp_pose.PoseLandmark.LEFT_HIP.value].x, lms[self.mp_pose.PoseLandmark.LEFT_HIP.value].y]

        if self.current_exercise == "Bicep Curl":
            angle = calculate_angle(l_shoulder, l_elbow, l_wrist)
            if angle > 160:
                self.stage = "down"
            if angle < 30 and self.stage == "down":
                self.stage = "up"
                self.counter += 1
        
        elif self.current_exercise == "Shoulder Press":
            angle = calculate_angle(l_hip, l_shoulder, l_elbow)
            if angle < 100:
                self.stage = "down"
            if angle > 160 and self.stage == "down":
                self.stage = "up"
                self.counter += 1
                
        return self.counter, self.stage
