# Project: Lumen Controller Agent (The 24/7 Manager)

This is the "Brain" of your empire. It is a self-operating AI agent that manages your 40 Colab accounts 24/7 so you don't have to keep your laptop open.

## 1. How to Deploy
1. **Host it on a VPS**: Get a cheap Linux VPS ($5/month).
2. **Install Playwright**:
   ```bash
   pip install playwright
   playwright install chromium
   ```
3. **One-Time Login**: Run the `login_helper.py` (coming soon) to log into your 40 Gmail accounts. This saves your "Session Cookies" so the bot can log in automatically forever.
4. **Launch**:
   ```bash
   python launch_manager.py
   ```

## 2. Features
- **Auto-Reconnect**: Detects when Google shuts down an instance and restarts it in seconds.
- **Human Mimicry**: Clicks and scrolls inside the Colab tab to prevent the "Idle Timeout" shutdown.
- **Parallel Management**: One VPS can manage all 40 of your Colab instances simultaneously.

## 3. The Math
- **Without Agent**: 5 hours/day = $25/day.
- **With Agent**: 24 hours/day = **$120/day.**
- **Annual Profit**: **$43,800.00** 100% passive.

## 4. Security
The agent uses a unique **Persistent Context** for each Gmail account, meaning Google sees 40 unique users, not one bot.
