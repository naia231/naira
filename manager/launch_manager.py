import asyncio
import os
import json
from core.colab_watchdog import ColabWatchdog

async def main():
    """
    Master Launcher for the Gemini-Powered Controller Agent.
    Manages all Colab instances simultaneously.
    """

    # Load account config
    config_path = os.path.join(os.path.dirname(__file__), "accounts.json")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            accounts = json.load(f)
    else:
        print("[!] No accounts.json found. Creating template...")
        accounts = [
            {
                "index": 0,
                "session": "./sessions/account_0",
                "notebook": "https://colab.research.google.com/drive/YOUR_NOTEBOOK_ID"
            }
        ]
        with open(config_path, "w") as f:
            json.dump(accounts, f, indent=2)
        print(f"[+] Template created at {config_path}. Edit it with your accounts.")
        return

    print(f"🚀 Launching Gemini Controller for {len(accounts)} accounts...")

    tasks = []
    for acc in accounts:
        agent = ColabWatchdog(acc["index"], acc["session"])
        tasks.append(agent.launch_and_manage(acc["notebook"]))

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
