from exercises.base_exercise import BaseExercise
from core.angle_utils import calculate_angle

class ShoulderPress(BaseExercise):
    """Logic for detecting and analyzing Shoulder Presses."""
    def __init__(self):
        super().__init__()
        self.name = "Shoulder Press"

    def analyze(self, landmarks):
        if not landmarks:
            return {"counter": self.counter, "stage": self.stage, "feedback": "No landmarks detected"}

        lms = landmarks.landmark
        
        # Points for Left Arm
        l_shoulder = [lms[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, lms[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        l_elbow = [lms[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].x, lms[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        l_wrist = [lms[self.mp_pose.PoseLandmark.LEFT_WRIST.value].x, lms[self.mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        l_hip = [lms[self.mp_pose.PoseLandmark.LEFT_HIP.value].x, lms[self.mp_pose.PoseLandmark.LEFT_HIP.value].y]

        # Points for Right Arm
        r_shoulder = [lms[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, lms[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        r_elbow = [lms[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, lms[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        r_wrist = [lms[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].x, lms[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
        r_hip = [lms[self.mp_pose.PoseLandmark.RIGHT_HIP.value].x, lms[self.mp_pose.PoseLandmark.RIGHT_HIP.value].y]

        # Calculate Angles (Hip-Shoulder-Elbow for overhead movement)
        l_shoulder_angle = calculate_angle(l_hip, l_shoulder, l_elbow)
        r_shoulder_angle = calculate_angle(r_hip, r_shoulder, r_elbow)
        
        # Calculate Elbow Angles (Shoulder-Elbow-Wrist for extension)
        l_elbow_angle = calculate_angle(l_shoulder, l_elbow, l_wrist)
        r_elbow_angle = calculate_angle(r_shoulder, r_elbow, r_wrist)

        # Rep Counting Logic
        # Down: Elbows below shoulders or at 90 degrees
        # Up: Arms extended overhead
        if l_elbow_angle < 100 and r_elbow_angle < 100:
            self.stage = "down"
        
        if l_elbow_angle > 160 and r_elbow_angle > 160 and self.stage == "down":
            self.stage = "up"
            self.counter += 1
            self.feedback = "Full Extension!"

        # Uneven Arms Detection
        angle_diff = abs(l_elbow_angle - r_elbow_angle)
        height_diff = abs(l_wrist[1] - r_wrist[1])
        
        if angle_diff > 20 or height_diff > 0.1:
            self.feedback = "Keep arms even!"
        elif self.stage == "up":
            self.feedback = "Great form!"

        return {
            "counter": self.counter,
            "stage": self.stage,
            "feedback": self.feedback,
            "left_elbow_angle": l_elbow_angle,
            "right_elbow_angle": r_elbow_angle,
            "uneven": angle_diff > 20
        }
