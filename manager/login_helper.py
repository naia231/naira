"""
Lumen Stealth Manager — Persistent Google Session Helper
Usage: Run this script on your Windows laptop once for each Google account.
It will open a visible Chromium window, allow you log in manually to Gmail,
and save the persistent context.
"""

import asyncio
import os
import sys
import shutil

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("[!] Playwright is not installed. Please run:")
    print("    pip install playwright && playwright install")
    sys.exit(1)

def print_header():
    print("=" * 60)
    print("     LUMEN CONTROLLER AGENT — GMAIL LOGIN HELPER")
    print("=" * 60)
    print("This utility launches a visible browser so you can manually")
    print("log into Google. Once logged in, your session is saved")
    print("permanently so the 24/7 autonomous watchdog can take over.")
    print("=" * 60)

async def create_session():
    print_header()
    
    # 1. Ask for email or account index
    email = input("\nEnter Google Account Email (or name/index): ").strip()
    if not email:
        print("[!] Email/name cannot be empty.")
        return

    # Sanitize name for directory
    sanitized_name = email.replace("@", "_").replace(".", "_")
    session_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "sessions", sanitized_name))
    
    print(f"\n[*] Preparing session directory: {session_dir}")
    if os.path.exists(session_dir):
        overwrite = input(f"[?] Session directory '{sanitized_name}' already exists. Overwrite? (y/n): ").strip().lower()
        if overwrite == 'y':
            shutil.rmtree(session_dir)
            os.makedirs(session_dir, exist_ok=True)
        else:
            print("[*] Reusing existing session to log in or update state.")
    else:
        os.makedirs(session_dir, exist_ok=True)

    print("\n[*] Booting visible Chromium browser...")
    async with async_playwright() as p:
        # Launch Chromium with persistent context
        context = await p.chromium.launch_persistent_context(
            user_data_dir=session_dir,
            headless=False,
            viewport={"width": 1280, "height": 720},
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox"
            ]
        )
        
        page = await context.new_page()
        
        # Go to Google Accounts
        print("[*] Navigating to Google Login...")
        await page.goto("https://accounts.google.com")
        
        print("\n" + "!" * 50)
        print(" ACTION REQUIRED:")
        print(" 1. Complete the Google/Gmail login process in the browser window.")
        print(" 2. Complete any 2-Factor Authentication (2FA) if prompted.")
        print(" 3. Once you see your Google Account homepage, type 'done' here.")
        print("!" * 50 + "\n")
        
        while True:
            user_status = input("Type 'done' and press Enter when login is fully complete: ").strip().lower()
            if user_status == 'done':
                break
        
        # Save storage state for an extra layer of backup
        storage_path = os.path.join(session_dir, "storage_state.json")
        await context.storage_state(path=storage_path)
        print(f"[+] Backup storage state saved to {storage_path}")
        
        print("[*] Closing browser...")
        await context.close()
        
    print("\n" + "=" * 60)
    print(" 🎉 SESSION SAVED SUCCESSFULLY!")
    print("=" * 60)
    print(f"Directory: {session_dir}")
    print("\nNext Steps:")
    print("1. Update your 'manager/accounts.json' file with this session path:")
    print(f"   \"session\": \"./sessions/{sanitized_name}\"")
    print("2. Commit the new 'sessions' folder to your Git repository.")
    print("3. Deploy to Railway. The agent will run 24/7 without your laptop!")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(create_session())
