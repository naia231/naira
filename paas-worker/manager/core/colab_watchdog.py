import asyncio
import random
from playwright.async_api import async_playwright

class ColabWatchdog:
    """
    Automated Controller Agent.
    1. Logs into Gmail/Colab.
    2. Runs the notebook.
    3. Keeps it alive by mimicking human interaction.
    4. Restarts on disconnect.
    """

    def __init__(self, account_index, session_path):
        self.index = account_index
        self.session_path = session_path

    async def launch_and_manage(self, notebook_url):
        async with async_playwright() as p:
            # Load persistent session (GMAIL Login)
            context = await p.chromium.launch_persistent_context(
                user_data_dir=self.session_path,
                headless=True,
                args=["--disable-blink-features=AutomationControlled"]
            )
            
            page = await context.new_page()
            print(f"[*] Agent {self.index}: Opening Colab...")
            await page.goto(notebook_url)

            # Step 1: Run All
            print(f"[*] Agent {self.index}: Triggering 'Run All'...")
            try:
                await page.keyboard.press("Control+F9")
            except:
                # Manual click if keyboard shortcut fails
                await page.click("#runtime-menu-button")
                await page.click("#run-all-item")

            # Step 2: Keep Alive Loop
            print(f"[*] Agent {self.index}: Entering 24/7 Watchdog mode.")
            while True:
                # Check for "Disconnect" or "Are you still there?" popups
                if await page.query_selector("text='Reconnect'"):
                    print(f"[!] Agent {self.index}: Disconnect detected! Reconnecting...")
                    await page.click("text='Reconnect'")
                
                # Human-like interaction to prevent sleep
                await page.mouse.move(random.randint(100, 500), random.randint(100, 500))
                await asyncio.sleep(random.randint(60, 180)) # Check every 1-3 mins

    @staticmethod
    def create_session(account_email):
        """Helper to manually log in once and save the session cookie."""
        # This will launch a non-headless browser for the user to log in
        pass
