import asyncio
import os
from core.colab_watchdog import ColabWatchdog

async def main():
    # Example: Manage 40 accounts
    # In reality, you'd load these from a JSON or .env
    ACCOUNTS = [
        {"index": 0, "session": "./sessions/acc0", "notebook": "https://colab.research.google.com/drive/xxx"},
    ]

    tasks = []
    for acc in ACCOUNTS:
        agent = ColabWatchdog(acc["index"], acc["session"])
        tasks.append(agent.launch_and_manage(acc["notebook"]))

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
