import cv2
import numpy as np

class VisionManager:
    """
    Agent Vision System.
    Analyzes screenshots to find UI elements (buttons, popups)
    without relying on HTML selectors.
    """

    @staticmethod
    def find_button(screenshot_path, template_path):
        """
        Uses template matching to find a button on the screen.
        Example: Find the 'Run All' play button icon.
        """
        img_rgb = cv2.imread(screenshot_path)
        template = cv2.imread(template_path)
        
        res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)
        
        for pt in zip(*loc[::-1]):
            # Return the center of the first match
            return (pt[0] + template.shape[1] // 2, pt[1] + template.shape[0] // 2)
        return None

    @staticmethod
    def is_popup_visible(screenshot_path, text="Reconnect"):
        """Checks if a specific warning popup is on the screen."""
        # Note: In a real implementation, we'd use EasyOCR here
        pass
