import asyncio
import os
import json
import logging
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
from core.colab_watchdog import ColabWatchdog

# Setup logging
logging.basicConfig(level=logging.INFO, format='[Lumen Controller] %(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger("controller")

app = FastAPI(title="Lumen Controller Admin C2")

# Active agents tracking
agents = []
accounts_data = []

@app.on_event("startup")
async def startup_event():
    """Load config and launch autonomous watchdog agents in the background."""
    global agents, accounts_data
    config_path = os.path.join(os.path.dirname(__file__), "accounts.json")
    
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            accounts_data = json.load(f)
    else:
        log.warning("No accounts.json found. Creating template...")
        accounts_data = [
            {
                "index": 0,
                "session": "./sessions/account_0",
                "notebook": "https://colab.research.google.com/drive/YOUR_NOTEBOOK_ID_HERE"
            }
        ]
        with open(config_path, "w") as f:
            json.dump(accounts_data, f, indent=2)
        log.info(f"Template accounts.json created at {config_path}")

    log.info(f"Initializing {len(accounts_data)} autonomous agents...")
    
    for acc in accounts_data:
        # Create a unique session folder path relative to the script directory
        session_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), acc["session"]))
        os.makedirs(session_folder, exist_ok=True)
        
        agent = ColabWatchdog(acc["index"], session_folder)
        agents.append(agent)
        
        # Spawn each agent loop in the background
        asyncio.create_task(agent.launch_and_manage(acc["notebook"]))
        log.info(f"Agent #{acc['index']} spawned for {acc['notebook'][:40]}...")

@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    """Render a premium dark-mode Glassmorphism C2 Dashboard."""
    # Build status cards dynamically
    status_cards_html = ""
    for idx, agent in enumerate(agents):
        stats = getattr(agent, "stats", {"views": 0, "restarts": 0, "uptime_min": 0})
        uptime = stats.get("uptime_min", 0)
        restarts = stats.get("restarts", 0)
        notebook_url = accounts_data[idx]["notebook"] if idx < len(accounts_data) else "N/A"
        
        # Color coding status based on uptime
        status_color = "#10B981" if uptime > 0 else "#EF4444"
        status_text = "ACTIVE" if uptime > 0 else "CONNECTING..."
        
        status_cards_html += f"""
        <div class="card">
            <div class="card-header">
                <span class="agent-id">Agent #{agent.index}</span>
                <span class="status-badge" style="background: {status_color}22; color: {status_color}; border: 1px solid {status_color}55;">
                    <span class="status-dot" style="background: {status_color};"></span>
                    {status_text}
                </span>
            </div>
            <div class="stat-row">
                <span class="stat-label">Uptime</span>
                <span class="stat-val">{uptime} mins</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">Restarts / Reconnects</span>
                <span class="stat-val">{restarts}</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">Notebook URL</span>
                <span class="stat-val truncate"><a href="{notebook_url}" target="_blank">{notebook_url}</a></span>
            </div>
        </div>
        """

    # If no agents loaded yet
    if not status_cards_html:
        status_cards_html = """
        <div class="card" style="grid-column: 1 / -1; text-align: center; padding: 3rem;">
            <p style="color: #9CA3AF; font-size: 1.1rem;">No accounts loaded. Create and configure <code>manager/accounts.json</code> with your sessions.</p>
        </div>
        """

    total_uptime = sum(getattr(a, "stats", {}).get("uptime_min", 0) for a in agents)
    total_restarts = sum(getattr(a, "stats", {}).get("restarts", 0) for a in agents)

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Lumen Autonomous C2 Dashboard</title>
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=JetBrains+Mono&display=swap" rel="stylesheet">
        <style>
            :root {{
                --bg-gradient: linear-gradient(135deg, #0F172A 0%, #020617 100%);
                --glass-bg: rgba(30, 41, 59, 0.45);
                --glass-border: rgba(255, 255, 255, 0.08);
                --text-primary: #F8FAFC;
                --text-secondary: #94A3B8;
                --accent: #6366F1;
                --accent-glow: rgba(99, 102, 241, 0.3);
            }}

            * {{
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }}

            body {{
                font-family: 'Outfit', sans-serif;
                background: var(--bg-gradient);
                color: var(--text-primary);
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                overflow-x: hidden;
            }}

            header {{
                backdrop-filter: blur(12px);
                -webkit-backdrop-filter: blur(12px);
                background: rgba(15, 23, 42, 0.6);
                border-bottom: 1px solid var(--glass-border);
                padding: 1.5rem 2rem;
                display: flex;
                justify-content: space-between;
                align-items: center;
                position: sticky;
                top: 0;
                z-index: 100;
            }}

            .logo-container {{
                display: flex;
                align-items: center;
                gap: 0.75rem;
            }}

            .logo-glow {{
                width: 12px;
                height: 12px;
                background: var(--accent);
                border-radius: 50%;
                box-shadow: 0 0 15px var(--accent);
                animation: pulse 2s infinite;
            }}

            h1 {{
                font-size: 1.5rem;
                font-weight: 800;
                letter-spacing: -0.5px;
                background: linear-gradient(90deg, #F8FAFC 0%, #CBD5E1 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }}

            .container {{
                max-width: 1400px;
                width: 100%;
                margin: 0 auto;
                padding: 2.5rem 2rem;
                flex-grow: 1;
            }}

            .overview-bar {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
                gap: 1.5rem;
                margin-bottom: 2.5rem;
            }}

            .overview-card {{
                background: var(--glass-bg);
                backdrop-filter: blur(8px);
                -webkit-backdrop-filter: blur(8px);
                border: 1px solid var(--glass-border);
                border-radius: 16px;
                padding: 1.5rem;
                display: flex;
                flex-direction: column;
                gap: 0.5rem;
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
            }}

            .overview-title {{
                font-size: 0.875rem;
                color: var(--text-secondary);
                text-transform: uppercase;
                letter-spacing: 1px;
            }}

            .overview-val {{
                font-size: 2rem;
                font-weight: 800;
                color: var(--text-primary);
                background: linear-gradient(90deg, #818CF8, #C084FC);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }}

            .section-title {{
                font-size: 1.25rem;
                font-weight: 600;
                margin-bottom: 1.5rem;
                color: var(--text-primary);
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }}

            .grid {{
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
                gap: 1.5rem;
            }}

            .card {{
                background: var(--glass-bg);
                backdrop-filter: blur(12px);
                -webkit-backdrop-filter: blur(12px);
                border: 1px solid var(--glass-border);
                border-radius: 20px;
                padding: 1.75rem;
                display: flex;
                flex-direction: column;
                gap: 1.25rem;
                transition: transform 0.3s ease, border-color 0.3s ease;
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.15);
            }}

            .card:hover {{
                transform: translateY(-4px);
                border-color: rgba(99, 102, 241, 0.3);
                box-shadow: 0 12px 40px 0 rgba(99, 102, 241, 0.1);
            }}

            .card-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 1px solid rgba(255, 255, 255, 0.05);
                padding-bottom: 1rem;
            }}

            .agent-id {{
                font-size: 1.1rem;
                font-weight: 600;
            }}

            .status-badge {{
                display: flex;
                align-items: center;
                gap: 0.5rem;
                padding: 0.35rem 0.75rem;
                border-radius: 99px;
                font-size: 0.75rem;
                font-weight: 600;
                letter-spacing: 0.5px;
            }}

            .status-dot {{
                width: 6px;
                height: 6px;
                border-radius: 50%;
            }}

            .stat-row {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 0.9rem;
            }}

            .stat-label {{
                color: var(--text-secondary);
            }}

            .stat-val {{
                font-weight: 600;
                color: var(--text-primary);
            }}

            .truncate {{
                max-width: 180px;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }}

            .truncate a {{
                color: var(--accent);
                text-decoration: none;
            }}

            .truncate a:hover {{
                text-decoration: underline;
            }}

            footer {{
                text-align: center;
                padding: 2rem;
                color: var(--text-secondary);
                font-size: 0.85rem;
                border-top: 1px solid var(--glass-border);
                backdrop-filter: blur(8px);
                background: rgba(15, 23, 42, 0.4);
                margin-top: auto;
            }}

            @keyframes pulse {{
                0% {{ transform: scale(1); opacity: 1; }}
                50% {{ transform: scale(1.2); opacity: 0.5; }}
                100% {{ transform: scale(1); opacity: 1; }}
            }}

            @keyframes rotate {{
                from {{ transform: rotate(0deg); }}
                to {{ transform: rotate(360deg); }}
            }}
        </style>
        <script>
            // Refresh stats every 10 seconds automatically
            setInterval(() => {{
                window.location.reload();
            }}, 15000);
        </script>
    </head>
    <body>
        <header>
            <div class="logo-container">
                <div class="logo-glow"></div>
                <h1>Lumen Swarm Controller</h1>
            </div>
            <div style="font-size: 0.875rem; color: var(--text-secondary);">
                Active Workers: <strong>{len(agents)}</strong>
            </div>
        </header>

        <div class="container">
            <div class="overview-bar">
                <div class="overview-card">
                    <span class="overview-title">Total Active Agents</span>
                    <span class="overview-val">{len(agents)}</span>
                </div>
                <div class="overview-card">
                    <span class="overview-title">Swarm Cumulative Uptime</span>
                    <span class="overview-val">{total_uptime} min</span>
                </div>
                <div class="overview-card">
                    <span class="overview-title">Total Auto-Recoveries</span>
                    <span class="overview-val">{total_restarts}</span>
                </div>
            </div>

            <h2 class="section-title">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="color: var(--accent);">
                    <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
                    <line x1="8" y1="21" x2="16" y2="21"></line>
                    <line x1="12" y1="17" x2="12" y2="21"></line>
                </svg>
                Swarm Status Monitor
            </h2>

            <div class="grid">
                {status_cards_html}
            </div>
        </div>

        <footer>
            Lumen Autonomous Swarm C2 &copy; 2026. Made with ❤️ for maximum passive yield.
        </footer>
    </body>
    </html>
    """
    return html_content

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    log.info(f"Starting C2 server on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)
