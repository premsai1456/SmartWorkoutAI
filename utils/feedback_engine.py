# utils/feedback_engine.py

class FeedbackEngine:
    """Generates intelligent, personalized feedback based on exercise form and performance."""
    
    DESCRIPTIONS = {
        "Bicep Curl": "Lift weights by bending elbows while keeping upper arm stable.",
        "Shoulder Press": "Push weights upward until arms are fully extended overhead."
    }
    
    @staticmethod
    def get_description(exercise_name):
        """Returns the description for the given exercise."""
        return FeedbackEngine.DESCRIPTIONS.get(exercise_name, "Perform the exercise with controlled movements.")
    
    @staticmethod
    def process_feedback(exercise_name, analysis_results):
        """
        Generates smart, dynamic feedback based on specific exercise analysis.
        """
        feedback = analysis_results.get("feedback", "")
        
        # Smart Feedback Enhancements
        if exercise_name == "Bicep Curl":
            if "drift" in feedback.lower():
                feedback = "Keep elbow close"
            elif not feedback or "good" in feedback.lower():
                feedback = "Perfect curl!"
        
        elif exercise_name == "Shoulder Press":
            if "extension" in feedback.lower():
                feedback = "Strong press!"
            elif "even" in feedback.lower():
                feedback = "Balance both arms"
            elif "No landmarks" not in feedback:
                # Default if moving but not yet full extension
                feedback = "Push higher"

        # Correctness flag
        warnings = ["tucked", "even", "drift", "No landmarks", "higher", "close"]
        is_correct = not any(w.lower() in feedback.lower() for w in warnings)
        
        return feedback, is_correct

    @staticmethod
    def calculate_accuracy(analysis_results):
        """
        Calculates accuracy percentage based on form analysis.
        """
        feedback = analysis_results.get("feedback", "").lower()
        if "good" in feedback or "perfect" in feedback or "strong" in feedback or not feedback:
            return 95
        elif "keep" in feedback or "control" in feedback or "balance" in feedback:
            return 65
        else:
            return 40

    @staticmethod
    def get_personalization_advice(accuracy):
        """
        Provides personalized advice based on the user's accuracy performance.
        """
        if accuracy < 50:
            return "Focus on proper form"
        elif 50 <= accuracy <= 75:
            return "Good, but improve control"
        else:
            return "Great form! Increase reps or weight"
