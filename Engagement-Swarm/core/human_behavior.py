import random
import time
import math

class HumanBehaviorEngine:
    """
    Simulates non-deterministic human behavior for browser automation.
    Includes realistic mouse trajectories and randomized wait times.
    """

    @staticmethod
    def sleep_human(min_sec=1, max_sec=5):
        """Randomized sleep with Poisson-like distribution."""
        time.sleep(random.uniform(min_sec, max_sec))

    @staticmethod
    def get_bezier_curve(start, end, steps=20):
        """Generates a realistic curved path for mouse movement."""
        x1, y1 = start
        x2, y2 = end
        
        # Random control point to create a natural curve
        cx = (x1 + x2) / 2 + random.randint(-100, 100)
        cy = (y1 + y2) / 2 + random.randint(-100, 100)
        
        points = []
        for i in range(steps):
            t = i / float(steps - 1)
            px = (1-t)**2 * x1 + 2*(1-t)*t * cx + t**2 * x2
            py = (1-t)**2 * y1 + 2*(1-t)*t * cy + t**2 * y2
            points.append((int(px), int(py)))
        return points

    @staticmethod
    def get_typing_delay():
        """Simulates human typing speed with errors and pauses."""
        return random.uniform(0.05, 0.2)
