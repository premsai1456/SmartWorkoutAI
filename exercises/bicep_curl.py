from exercises.base_exercise import BaseExercise
from core.angle_utils import calculate_angle
import mediapipe as mp


class BicepCurl(BaseExercise):
    """Logic for detecting and analyzing Bicep Curls."""

    def __init__(self):
        super().__init__()
        self.name = "Bicep Curl"

        # Separate tracking for both arms
        self.left_stage = "down"
        self.right_stage = "down"

        self.counter = 0
        self.feedback = "Start curling!"

        # MediaPipe reference
        self.mp_pose = mp.solutions.pose

    def analyze(self, landmarks):

        if not landmarks:
            return {
                "counter": self.counter,
                "stage": "No Detection",
                "feedback": "No landmarks detected"
            }

        lms = landmarks.landmark

        # ---------------- LEFT ARM ----------------
        l_shoulder = [
            lms[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
            lms[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y
        ]
        l_elbow = [
            lms[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
            lms[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].y
        ]
        l_wrist = [
            lms[self.mp_pose.PoseLandmark.LEFT_WRIST.value].x,
            lms[self.mp_pose.PoseLandmark.LEFT_WRIST.value].y
        ]

        # ---------------- RIGHT ARM ----------------
        r_shoulder = [
            lms[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
            lms[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y
        ]
        r_elbow = [
            lms[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
            lms[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].y
        ]
        r_wrist = [
            lms[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
            lms[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].y
        ]

        # ---------------- ANGLES ----------------
        l_angle = calculate_angle(l_shoulder, l_elbow, l_wrist)
        r_angle = calculate_angle(r_shoulder, r_elbow, r_wrist)

        # DEBUG (remove later)
        print("Left Angle:", round(l_angle, 2), "Right Angle:", round(r_angle, 2))

        # ---------------- LEFT ARM LOGIC ----------------
        if l_angle > 150:
            self.left_stage = "down"

        elif l_angle < 50 and self.left_stage == "down":
            self.left_stage = "up"
            self.counter += 1
            self.feedback = "Left arm rep!"

        # ---------------- RIGHT ARM LOGIC ----------------
        if r_angle > 150:
            self.right_stage = "down"

        elif r_angle < 50 and self.right_stage == "down":
            self.right_stage = "up"
            self.counter += 1
            self.feedback = "Right arm rep!"

        # ---------------- ACTIVE ARM ----------------
        if l_angle < r_angle:
            active_angle = l_angle
            active_side = "Left Arm"
        else:
            active_angle = r_angle
            active_side = "Right Arm"

        # ---------------- FEEDBACK ----------------
        if active_angle < 30:
            self.feedback = "Too fast! Control movement"
        elif active_angle > 160:
            self.feedback = "Fully extend arm"
        else:
            self.feedback = "Good form!"

        # ---------------- RETURN ----------------
        return {
            "counter": self.counter,
            "stage": active_side,
            "feedback": self.feedback,
            "left_angle": l_angle,
            "right_angle": r_angle
        }