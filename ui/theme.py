# ui/theme.py

class Theme:
    """Defines the color palette and constants for the dark theme UI."""
    
    # Colors (BGR format for OpenCV)
    BG_DARK = (20, 20, 20)
    PANEL_DARK = (35, 35, 35)
    ACCENT_BLUE = (255, 191, 0)
    
    TEXT_PRIMARY = (240, 240, 240)
    TEXT_SECONDARY = (180, 180, 180)
    
    SUCCESS = (0, 255, 0)
    WARNING = (0, 255, 255)
    DANGER = (0, 0, 255)
    
    # Layout Constants
    TOP_BAR_HEIGHT = 60
    LEFT_PANEL_WIDTH = 200
    DESC_BOX_HEIGHT = 100
    STOP_BTN_SIZE = (120, 40)
    
    # Fonts
    FONT = 0 # cv2.FONT_HERSHEY_SIMPLEX
    FONT_SCALE_LG = 0.8
    FONT_SCALE_MD = 0.6
    FONT_SCALE_SM = 0.4
