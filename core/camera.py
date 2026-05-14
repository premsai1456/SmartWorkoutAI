import cv2

class Camera:
    """Handles camera initialization and frame capture."""
    def __init__(self, source=0):
        self.cap = cv2.VideoCapture(source)
        if not self.cap.isOpened():
            raise ValueError(f"Unable to open camera source: {source}")

    def read(self):
        """Reads a frame from the camera."""
        ret, frame = self.cap.read()
        return ret, frame

    def release(self):
        """Releases the camera resource."""
        self.cap.release()
