import asyncio
import os
import subprocess
from playwright.async_api import async_playwright
from personas.persona_manager import PersonaManager
from core.human_behavior import HumanBehaviorEngine

class StealthSwarmEngine:
    """
    The core browser engine. 
    Handles rebrowser-playwright initialization and stealth automation.
    """

    def __init__(self, worker_index):
        self.index = worker_index
        self.persona = PersonaManager.get_persona(worker_index)
        self.behavior = HumanBehaviorEngine()

    async def setup_warp(self):
        """Attempts to rotate IP using Cloudflare WARP (Free Proxy)."""
        try:
            print(f"[*] Worker {self.index}: Rotating IP via WARP...")
            # Note: This requires warp-cli installed on the host
            subprocess.run(["warp-cli", "connect"], stdout=subprocess.DEVNULL)
        except:
            pass

    async def watch_video(self, video_url, duration_sec=600, keyword=None):
        """Watches a video with organic human-like behavior."""
        async with async_playwright() as p:
            # Launch with specific persona
            browser = await p.chromium.launch(headless=True)
            
            context = await browser.new_context(
                user_agent=self.persona["user_agent"],
                viewport={"width": self.persona["width"], "height": self.persona["height"]},
                device_scale_factor=self.persona["device_scale_factor"],
                has_touch=self.persona["has_touch"]
            )

            page = await context.new_page()
            
            if keyword:
                print(f"[*] Worker {self.index}: Searching for '{keyword}'...")
                await page.goto("https://www.youtube.com", wait_until="networkidle")
                await page.fill("input[name='search_query']", keyword)
                await page.keyboard.press("Enter")
                await page.wait_for_selector("ytd-video-renderer", timeout=10000)
                # Click the video that matches our URL or just the first result
                await page.click(f"a[href*='{video_url.split('v=')[1]}']")
            else:
                print(f"[*] Worker {self.index}: Navigating directly to video...")
                await page.goto(video_url, wait_until="networkidle")

            # Human-like interaction: Scroll, hover, and wait
            self.behavior.sleep_human(5, 10)
            await page.mouse.move(random.randint(100, 500), random.randint(100, 500))
            
            print(f"[*] Worker {self.index}: Watching for {duration_sec}s...")
            await asyncio.sleep(duration_sec)
            
            print(f"[*] Worker {self.index}: Finished session.")
            await browser.close()
