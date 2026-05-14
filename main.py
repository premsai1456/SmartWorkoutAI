import cv2
import time

from core.camera import Camera
from core.pose_detector import PoseDetector
from core.exercise_detector import ExerciseDetector
from core.session_manager import SessionManager

from exercises.bicep_curl import BicepCurl
from exercises.shoulder_press import ShoulderPress

from ui.overlay import Overlay
from utils.feedback_engine import FeedbackEngine

# NEW FEATURES
from utils.progress_tracker import save_progress
from utils.voice import speak


def main():
    # ---------------- INIT ----------------
    try:
        cam = Camera(0)
    except ValueError as e:
        print(f"Error: {e}")
        return

    pose_detector = PoseDetector()
    exercise_classifier = ExerciseDetector()
    session_manager = SessionManager()
    overlay = Overlay()

    exercises = {
        "Bicep Curl": BicepCurl(),
        "Shoulder Press": ShoulderPress()
    }

    window_name = 'Workout Form Detection'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(window_name, overlay.handle_mouse_events)

    print("Starting AI Workout System...")
    print("Press 'q' or click 'STOP' to exit.")

    # ---------------- FPS ----------------
    prev_time = 0
    fps = 0

    # ---------------- VOICE CONTROL ----------------
    last_voice_time = 0
    voice_delay = 3  # seconds

    try:
        while True:
            # -------- FRAME CAPTURE --------
            ret, frame = cam.read()
            if not ret:
                break

            h, w, _ = frame.shape  # IMPORTANT (fix crash)

            # -------- FPS CALCULATION --------
            current_time = time.time()
            if prev_time != 0:
                fps = 1 / (current_time - prev_time)
            prev_time = current_time

            # -------- POSE DETECTION --------
            landmarks = pose_detector.process(frame)

            # -------- EXERCISE DETECTION --------
            current_exercise_name = exercise_classifier.detect(landmarks)
            exercise_obj = exercises.get(current_exercise_name)

            results = {}

            if landmarks and exercise_obj:
                results = exercise_obj.analyze(landmarks)
                pose_detector.draw(frame, landmarks)

            # -------- FEEDBACK ENGINE --------
            description = FeedbackEngine.get_description(current_exercise_name)

            feedback, is_correct = FeedbackEngine.process_feedback(
                current_exercise_name, results
            )

            accuracy = FeedbackEngine.calculate_accuracy(results)
            personal_advice = FeedbackEngine.get_personalization_advice(accuracy)

            results["feedback"] = f"{feedback} | {personal_advice}"

            # -------- SESSION TRACKING --------
            if exercise_obj:
                session_manager.update_session(
                    current_exercise_name,
                    results.get("counter", 0),
                    accuracy
                )

                # -------- SAVE PROGRESS --------
                save_progress(
                    current_exercise_name,
                    results.get("counter", 0),
                    accuracy
                )

            # -------- VOICE FEEDBACK --------
            if time.time() - last_voice_time > voice_delay:
                if is_correct:
                    speak("Good rep")
                else:
                    speak("Fix your form")

                last_voice_time = time.time()

            # -------- UI OVERLAY --------
            frame = overlay.apply(
                frame,
                current_exercise_name,
                results,
                accuracy,
                description
            )

            # -------- FPS DISPLAY (FIXED POSITION) --------
            cv2.rectangle(frame, (w - 160, 10), (w - 10, 60), (40, 40, 40), -1)

            cv2.putText(
                frame,
                f"FPS: {int(fps)}",
                (w - 150, 45),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            cv2.imshow(window_name, frame)

            # -------- EXIT --------
            if cv2.waitKey(1) & 0xFF == ord('q') or overlay.should_stop:
                break

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # -------- CLEANUP --------
        cam.release()
        cv2.destroyAllWindows()
        session_manager.print_summary()


if __name__ == "__main__":
    main()