# Oracle Cloud Stealth Mining Guide (The Gold Mine)

Oracle Cloud's "Always Free" tier provides **4 ARM Ampere Cores** and **24GB of RAM**. This is the most profitable free cloud resource for CPU mining in 2026.

## Estimated Earnings
- **Hashrate**: ~2,500 - 3,500 H/s (using all 4 cores).
- **Daily Profit**: ~$0.20 - $0.35.
- **Monthly Profit**: ~$6.00 - $10.50 (per account).
- **Cost**: $0.00 (Forever).

## The Stealth Setup
Oracle is very strict. You **MUST** use the Lumen Stealth configuration to avoid being flagged.

### 1. Instance Creation
- Image: **Canonical Ubuntu 22.04** (ARM).
- Shape: **VM.Standard.A1.Flex** (4 OCPUs, 24GB RAM).
- Ensure you download your SSH Private Key (`.key`).

### 2. Deployment Script
Once you SSH into your Oracle instance, run these commands:

```bash
# 1. Update system
sudo apt update && sudo apt install -y docker.io docker-compose cpulimit

# 2. Clone your Lumen repository
git clone https://github.com/YOUR_USERNAME/Lumen.git
cd Lumen

# 3. Configure ARC for Oracle (Multi-core Stealth)
# On Oracle, we can use 4 cores, but we keep each core at ~40% to look like a node
echo "ARC_TURBO=false" >> .env
echo "ARC_CPU_MIN=35" >> .env
echo "ARC_CPU_MAX=50" >> .env

# 4. Start the swarm
docker-compose up -d
```

## Why this works on Oracle
- **Multi-Core Camouflage**: We distribute the mining across all 4 cores but keep the intensity low (40%) per core.
- **Shadow Tunnel**: By using the Relay server (on Render), Oracle's network monitors only see a single connection to a "Data Sync" server, not a mining pool.
- **Always Free**: As long as you keep the CPU patterns "wavy" (ARC jitter), the account remains active indefinitely.

---

## Scaling Tip
If you manage to open **5 Oracle accounts** (using different family members' cards), you can earn **$30 - $50 per month** for doing absolutely nothing.
