# ui/overlay.py
import cv2
import numpy as np
from ui.theme import Theme

class Overlay:
    """Handles the OpenCV-based UI overlay for the workout system."""
    
    def __init__(self):
        self.stop_btn_rect = (0, 0, 0, 0) # (x1, y1, x2, y2)
        self.should_stop = False

    def draw_rounded_rect(self, img, pt1, pt2, color, thickness, r):
        """Draws a rectangle with rounded corners."""
        x1, y1 = pt1
        x2, y2 = pt2
        # Top left
        cv2.ellipse(img, (x1 + r, y1 + r), (r, r), 180, 0, 90, color, thickness)
        # Top right
        cv2.ellipse(img, (x2 - r, y1 + r), (r, r), 270, 0, 90, color, thickness)
        # Bottom right
        cv2.ellipse(img, (x2 - r, y2 - r), (r, r), 0, 0, 90, color, thickness)
        # Bottom left
        cv2.ellipse(img, (x1 + r, y2 - r), (r, r), 90, 0, 90, color, thickness)
        
        cv2.line(img, (x1 + r, y1), (x2 - r, y1), color, thickness)
        cv2.line(img, (x1 + r, y2), (x2 - r, y2), color, thickness)
        cv2.line(img, (x1, y1 + r), (x1, y2 - r), color, thickness)
        cv2.line(img, (x2, y1 + r), (x2, y2 - r), color, thickness)

    def draw_accuracy_bar(self, img, x, y, w, h, value):
        """Draws an animated, color-coded accuracy bar."""
        # Background
        cv2.rectangle(img, (x, y), (x + w, y + h), (50, 50, 50), -1)
        
        # Color based on value
        if value > 75:
            color = Theme.SUCCESS
        elif value > 50:
            color = Theme.WARNING
        else:
            color = Theme.DANGER
            
        bar_w = int((value / 100) * w)
        cv2.rectangle(img, (x, y), (x + bar_w, y + h), color, -1)
        cv2.putText(img, f"{value}%", (x + w + 5, y + h - 2), Theme.FONT, Theme.FONT_SCALE_SM, Theme.TEXT_PRIMARY, 1)

    def handle_mouse_events(self, event, x, y, flags, param):
        """Handles mouse clicks for the STOP button."""
        if event == cv2.EVENT_LBUTTONDOWN:
            x1, y1, x2, y2 = self.stop_btn_rect
            if x1 <= x <= x2 and y1 <= y <= y2:
                self.should_stop = True

    def apply(self, frame, exercise_name, results, accuracy, description):
        """Applies the full UI overlay to the frame."""
        h, w, _ = frame.shape
        
        # 1. Top Bar
        cv2.rectangle(frame, (0, 0), (w, Theme.TOP_BAR_HEIGHT), Theme.PANEL_DARK, -1)
        cv2.putText(frame, exercise_name.upper(), (20, 40), Theme.FONT, Theme.FONT_SCALE_LG, Theme.ACCENT_BLUE, 2)
        
        # 2. Left Panel
        cv2.rectangle(frame, (0, Theme.TOP_BAR_HEIGHT), (Theme.LEFT_PANEL_WIDTH, h), Theme.PANEL_DARK, -1)
        
        # Stats in Left Panel
        reps = results.get("counter", 0)
        stage = results.get("stage", "-")
        feedback = results.get("feedback", "")
        
        y_offset = Theme.TOP_BAR_HEIGHT + 40
        cv2.putText(frame, "REPS", (20, y_offset), Theme.FONT, Theme.FONT_SCALE_SM, Theme.TEXT_SECONDARY, 1)
        cv2.putText(frame, str(reps), (20, y_offset + 30), Theme.FONT, 1.2, Theme.TEXT_PRIMARY, 2)
        
        y_offset += 80
        cv2.putText(frame, "STAGE", (20, y_offset), Theme.FONT, Theme.FONT_SCALE_SM, Theme.TEXT_SECONDARY, 1)
        cv2.putText(frame, str(stage).upper(), (20, y_offset + 30), Theme.FONT, Theme.FONT_SCALE_MD, Theme.TEXT_PRIMARY, 2)
        
        y_offset += 80
        cv2.putText(frame, "ACCURACY", (20, y_offset), Theme.FONT, Theme.FONT_SCALE_SM, Theme.TEXT_SECONDARY, 1)
        self.draw_accuracy_bar(frame, 20, y_offset + 20, 120, 10, accuracy)
        
        # 3. Form Indicator (Center Bottom)
        is_correct = "Good" in feedback or not any(w in feedback.lower() for w in ["keep", "even", "drift"])
        indicator_text = "FORM: CORRECT" if is_correct else "FORM: INCORRECT"
        indicator_color = Theme.SUCCESS if is_correct else Theme.DANGER
        cv2.putText(frame, indicator_text, (w // 2 - 80, h - 120), Theme.FONT, Theme.FONT_SCALE_MD, indicator_color, 2)
        cv2.putText(frame, feedback, (w // 2 - 100, h - 150), Theme.FONT, Theme.FONT_SCALE_MD, Theme.TEXT_PRIMARY, 1)

        # 4. STOP Button (Top Right)
        btn_w, btn_h = Theme.STOP_BTN_SIZE
        bx1, by1 = w - btn_w - 20, 10
        bx2, by2 = w - 20, 10 + btn_h
        self.stop_btn_rect = (bx1, by1, bx2, by2)
        
        cv2.rectangle(frame, (bx1, by1), (bx2, by2), Theme.DANGER, -1)
        cv2.putText(frame, "STOP", (bx1 + 35, by1 + 28), Theme.FONT, Theme.FONT_SCALE_MD, (255, 255, 255), 2)

        # 5. Description Box (Bottom Right)
        box_h = Theme.DESC_BOX_HEIGHT
        box_w = 300
        dx1, dy1 = w - box_w - 20, h - box_h - 20
        dx2, dy2 = w - 20, h - 20
        
        # Semi-transparent background for box
        overlay = frame.copy()
        cv2.rectangle(overlay, (dx1, dy1), (dx2, dy2), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
        cv2.rectangle(frame, (dx1, dy1), (dx2, dy2), Theme.ACCENT_BLUE, 1)
        
        # Wrap text for description
        words = description.split()
        lines = []
        current_line = ""
        for word in words:
            if len(current_line + word) < 35:
                current_line += word + " "
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)
        
        for i, line in enumerate(lines[:3]):
            cv2.putText(frame, line.strip(), (dx1 + 10, dy1 + 25 + (i * 20)), Theme.FONT, Theme.FONT_SCALE_SM, Theme.TEXT_PRIMARY, 1)

        return frame
