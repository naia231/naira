import asyncio
import random
import os
import tempfile
from playwright.async_api import async_playwright
from core.gemini_brain import GeminiBrain
from stealth.captcha_solver import CaptchaSolver
from stealth.proxy_rotator import ProxyRotator

class ColabWatchdog:
    """
    Gemini-Powered Controller Agent v3.0.
    Uses AI Vision to manage Colab instances 24/7.
    """

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
    TELEGRAM_CHAT = os.getenv("TELEGRAM_CHAT_ID", "")

    def __init__(self, account_index, session_path):
        self.index = account_index
        self.session_path = session_path
        self.brain = GeminiBrain(self.GEMINI_API_KEY) if self.GEMINI_API_KEY else None
        self.captcha_solver = CaptchaSolver()
        self.proxy_rotator = ProxyRotator()
        self.stats = {"views": 0, "restarts": 0, "uptime_min": 0}

    async def send_telegram(self, message):
        """Sends a status update to Telegram."""
        if not self.TELEGRAM_TOKEN:
            return
        import requests
        url = f"https://api.telegram.org/bot{self.TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": self.TELEGRAM_CHAT, "text": message})

    async def take_screenshot(self, page):
        """Takes a screenshot and saves it to a temp file."""
        path = os.path.join(tempfile.gettempdir(), f"worker_{self.index}.png")
        await page.screenshot(path=path)
        return path

    async def launch_and_manage(self, notebook_url):
        """Main 24/7 management loop."""
        async with async_playwright() as p:
            proxy_config = self.proxy_rotator.get_proxy()
            launch_args = {"headless": True, "args": ["--disable-blink-features=AutomationControlled"]}
            
            if proxy_config:
                launch_args["proxy"] = proxy_config
                print(f"[*] Agent {self.index}: Booting with Residential Proxy: {proxy_config['server']}")

            context = await p.chromium.launch_persistent_context(
                user_data_dir=self.session_path,
                **launch_args
            )

            page = await context.new_page()
            print(f"[*] Agent {self.index}: Opening Colab...")
            await page.goto(notebook_url, timeout=60000)
            await asyncio.sleep(10)

            # Step 1: Run All Cells
            print(f"[*] Agent {self.index}: Triggering 'Run All'...")
            try:
                await page.keyboard.press("Control+F9")
            except:
                pass

            await self.send_telegram(f"🟢 Worker #{self.index} started on Colab.")

            # Step 2: Hybrid Watchdog Loop
            print(f"[*] Agent {self.index}: Entering Hybrid Watchdog mode.")
            cycle = 0
            while True:
                cycle += 1
                self.stats["uptime_min"] += 2
                unknown_error = False

                # 90% Logic: Fast, Free Local DOM Parsing
                try:
                    reconnect_btn = await page.query_selector("text='Reconnect'")
                    if reconnect_btn:
                        print(f"[!] Agent {self.index}: Local DOM detected 'Reconnect'. Clicking...")
                        await reconnect_btn.click()
                        self.stats["restarts"] += 1
                        await asyncio.sleep(5)
                        continue

                    # Check for "Are you still there?" or Captchas
                    captcha_btn = await page.query_selector("text='I am not a robot'")
                    if captcha_btn or await page.query_selector("iframe[title*='reCAPTCHA']"):
                        print(f"[!] Agent {self.index}: Captcha detected!")
                        
                        # Try to solve it locally via Capsolver
                        solved = await self.captcha_solver.solve_recaptcha(page, "SITE_KEY_PLACEHOLDER", notebook_url)
                        if solved:
                            self.stats["restarts"] += 1
                            continue
                            
                        # If Capsolver fails or it's a new unknown popup, fallback to Gemini
                        unknown_error = True 
                        
                except Exception as e:
                    print(f"[*] Agent {self.index}: DOM parse error: {e}")
                    unknown_error = True

                # 10% Logic: Gemini AI Fallback for Unknown States
                if unknown_error and self.brain and (cycle % 5 == 0): # Only ping AI max once per 10 mins
                    print(f"[*] Agent {self.index}: Unknown state. Waking up Gemini...")
                    screenshot_path = await self.take_screenshot(page)
                    
                    # Inject JS to get bounding boxes of all buttons/links
                    dom_data = await page.evaluate('''() => {
                        const elements = Array.from(document.querySelectorAll('button, a'));
                        return elements.map(e => {
                            const rect = e.getBoundingClientRect();
                            return {tag: e.tagName, text: e.innerText.trim(), x: rect.x + rect.width/2, y: rect.y + rect.height/2};
                        }).filter(e => e.text.length > 0);
                    }''')

                    decision = await self.brain.analyze_screen_with_dom(screenshot_path, dom_data)
                    action = decision.get("action", "wait")

                    if action == "click":
                        x = decision.get("x", 400)
                        y = decision.get("y", 400)
                        print(f"[*] Agent {self.index}: Gemini says CLICK exactly at ({x}, {y})")
                        await page.mouse.click(x, y)
                        self.stats["restarts"] += 1

                # Human-like idle behavior
                await page.mouse.move(
                    random.randint(100, 800),
                    random.randint(100, 500)
                )

                # Hourly Telegram report
                if cycle % 30 == 0:  # Every ~60 minutes
                    if self.brain:
                        report = self.brain.generate_report(self.stats)
                    else:
                        report = f"Worker #{self.index} | Uptime: {self.stats['uptime_min']}min | Restarts: {self.stats['restarts']}"
                    await self.send_telegram(report)

                await asyncio.sleep(random.randint(90, 150))  # 1.5-2.5 min cycles

    @staticmethod
    async def create_session(account_email):
        """Launch a visible browser for manual Gmail login. Run once per account."""
        async with async_playwright() as p:
            session_dir = f"./sessions/{account_email.replace('@','_')}"
            os.makedirs(session_dir, exist_ok=True)
            context = await p.chromium.launch_persistent_context(
                user_data_dir=session_dir,
                headless=False  # Visible so user can log in
            )
            page = await context.new_page()
            await page.goto("https://accounts.google.com")
            print(f"[*] Log into {account_email}, then close the browser window.")
            await page.wait_for_event("close", timeout=300000)
            print(f"[+] Session saved to {session_dir}")
