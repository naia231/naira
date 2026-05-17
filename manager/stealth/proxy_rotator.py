import random
import os

class ProxyRotator:
    """
    Manages Residential Proxies and Cloudflare WARP routing.
    Prevents Google from detecting the headless browser as a Data Center IP.
    """

    def __init__(self, proxy_list_path=None):
        self.proxies = []
        
        # Load from file if provided
        if proxy_list_path and os.path.exists(proxy_list_path):
            with open(proxy_list_path, "r") as f:
                self.proxies = [line.strip() for line in f if line.strip()]
        
        # Fallback to env var (format: IP:PORT:USER:PASS,IP:PORT:USER:PASS)
        elif os.getenv("PROXY_LIST"):
            self.proxies = os.getenv("PROXY_LIST").split(",")

    def get_proxy(self):
        """Returns a random proxy configuration for Playwright."""
        if not self.proxies:
            return None
            
        proxy_str = random.choice(self.proxies)
        
        # Handle format: IP:PORT:USERNAME:PASSWORD
        parts = proxy_str.split(":")
        
        if len(parts) == 4:
            return {
                "server": f"http://{parts[0]}:{parts[1]}",
                "username": parts[2],
                "password": parts[3]
            }
        elif len(parts) == 2:
            return {
                "server": f"http://{parts[0]}:{parts[1]}"
            }
            
        return None

    def get_playwright_args(self, proxy_config):
        """Returns the playwright launch args for a given proxy."""
        if not proxy_config:
            return {}
            
        return {
            "proxy": proxy_config
        }
