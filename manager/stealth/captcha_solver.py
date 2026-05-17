import asyncio
import os
import requests
import time

class CaptchaSolver:
    """
    Automated Captcha Bypass using 2Captcha/Capsolver.
    Bypasses Google's 'I am not a robot' and Turnstile checks dynamically.
    """

    def __init__(self, api_key=None):
        # Fallback to env var if not passed
        self.api_key = api_key or os.getenv("CAPSOLVER_API_KEY", "")

    async def solve_recaptcha(self, page, site_key, url):
        """Sends recaptcha data to Capsolver and injects the token into the page."""
        if not self.api_key:
            print("[!] CaptchaSolver: No API key provided. Cannot solve captcha.")
            return False

        print("[*] Agent: Captcha detected. Requesting AI solve via Capsolver...")
        
        payload = {
            "clientKey": self.api_key,
            "task": {
                "type": "ReCaptchaV2TaskProxyLess",
                "websiteURL": url,
                "websiteKey": site_key
            }
        }
        
        # 1. Create Task
        res = requests.post("https://api.capsolver.com/createTask", json=payload).json()
        if res.get("errorId") != 0:
            print(f"[!] Capsolver Error: {res}")
            return False
            
        task_id = res.get("taskId")
        
        # 2. Wait for result
        print(f"[*] Agent: Task created ({task_id}). Waiting for solution...")
        for _ in range(30):
            await asyncio.sleep(2)
            result = requests.post("https://api.capsolver.com/getTaskResult", json={
                "clientKey": self.api_key,
                "taskId": task_id
            }).json()
            
            if result.get("status") == "ready":
                token = result.get("solution", {}).get("gRecaptchaResponse")
                print("[+] Agent: Captcha solved successfully!")
                
                # 3. Inject token back into the page
                await page.evaluate(f"document.getElementById('g-recaptcha-response').innerHTML='{token}';")
                
                # Try to find the submit callback and execute it
                await page.evaluate("if(typeof callback !== 'undefined') { callback(); } else if (typeof onSubmit !== 'undefined') { onSubmit(); }")
                return True
                
        print("[!] Agent: Captcha solve timed out.")
        return False

    async def handle_checkbox(self, page):
        """Attempts to automatically click the 'I am not a robot' checkbox if it's a simple one."""
        try:
            checkbox = await page.query_selector("iframe[title*='reCAPTCHA']")
            if checkbox:
                await checkbox.click()
                await asyncio.sleep(2)
                return True
        except:
            pass
        return False
