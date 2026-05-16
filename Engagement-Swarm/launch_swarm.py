import asyncio
import json
import sys
from core.browser_engine import StealthSwarmEngine

async def run_worker(index, targets):
    """Execution loop for a single swarm worker."""
    engine = StealthSwarmEngine(index)
    
    for target in targets:
        print(f"[Swarm] Worker {index} targeting: {target['url']}")
        await engine.watch_video(target['url'], target['duration'], target.get('keyword'))

async def main():
    # Load targets
    try:
        with open("config/targets.json", "r") as f:
            targets = json.load(f)
    except:
        targets = [{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "duration": 60}]

    worker_index = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    
    # Launch 4 parallel tabs per Colab instance to maximize views
    print(f"🚀 [Swarm] Launching Worker {worker_index} with 4-Tab Parallelism...")
    tasks = []
    for tab_id in range(4):
        # We give each tab a unique persona by adjusting the index
        unique_index = (worker_index * 10) + tab_id
        tasks.append(run_worker(unique_index, targets))
    
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
