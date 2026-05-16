import random

class PersonaManager:
    """
    Manages unique identities for each swarm worker.
    Ensures that every browser instance has a different hardware/software profile.
    """

    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1"
    ]

    RESOLUTIONS = [
        (1920, 1080), (1366, 768), (1440, 900), (1536, 864), (2560, 1440)
    ]

    @classmethod
    def get_persona(cls, index):
        """Returns a stable persona based on the worker index."""
        random.seed(index) # Ensure the same worker always has the same persona
        
        ua = random.choice(cls.USER_AGENTS)
        res = random.choice(cls.RESOLUTIONS)
        
        return {
            "user_agent": ua,
            "width": res[0],
            "height": res[1],
            "hardware_concurrency": random.choice([4, 8, 12, 16]),
            "device_scale_factor": random.choice([1, 2]),
            "has_touch": "iPhone" in ua
        }
