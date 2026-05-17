"""
Lumen Shadow Tunnel — Local WebSocket-to-TCP Proxy

This script bridges XMRig's native Stratum TCP protocol
with the Render-deployed Shadow Tunnel WebSocket.

Protocol details:
  - XMRig sends newline-delimited JSON over TCP (Stratum v2)
  - Shadow Tunnel (index.js) expects text WebSocket frames
  - This proxy converts between the two transparently
"""

import asyncio
import websockets
import sys
import logging
import os

logging.basicConfig(level=logging.INFO, format='[WS Proxy] %(message)s')
log = logging.getLogger("ws_proxy")

LOCAL_HOST = "127.0.0.1"
LOCAL_PORT = int(os.getenv("PROXY_PORT", 10128))
RELAY_URL = os.getenv("RELAY_URL")

if not RELAY_URL:
    log.error("RELAY_URL environment variable is required.")
    sys.exit(1)


async def handle_client(reader, writer):
    """Handle a new local TCP connection from XMRig."""
    client_address = writer.get_extra_info('peername')
    log.info(f"Accepted local connection from {client_address}")

    ws = None
    try:
        # Connect to the remote WebSocket relay with retry for cold starts
        max_retries = 5
        for attempt in range(1, max_retries + 1):
            try:
                log.info(f"Connecting to relay tunnel at {RELAY_URL}... (attempt {attempt}/{max_retries})")
                ws = await asyncio.wait_for(
                    websockets.connect(
                        RELAY_URL,
                        ping_interval=30,
                        ping_timeout=10,
                        close_timeout=5
                    ),
                    timeout=20
                )
                log.info("WebSocket tunnel established.")
                break
            except (asyncio.TimeoutError, OSError, Exception) as conn_err:
                if attempt == max_retries:
                    raise ConnectionError(
                        f"Failed to connect after {max_retries} attempts: {conn_err}"
                    )
                backoff = 5 * attempt
                log.warning(f"Connection attempt {attempt} failed: {conn_err}. Retrying in {backoff}s...")
                await asyncio.sleep(backoff)

        async def tcp_to_ws():
            """Forward XMRig TCP data to WebSocket as text frames."""
            try:
                while True:
                    data = await reader.read(4096)
                    if not data:
                        log.info("XMRig disconnected (EOF).")
                        break
                    # Stratum is text-based newline-delimited JSON.
                    # Must send as text, not binary, for shadow-tunnel compatibility.
                    text = data.decode('utf-8', errors='replace')
                    await ws.send(text)
            except asyncio.CancelledError:
                pass
            except Exception as e:
                log.error(f"TCP -> WS error: {e}")

        async def ws_to_tcp():
            """Forward WebSocket messages from pool back to XMRig TCP."""
            try:
                async for message in ws:
                    if isinstance(message, str):
                        # Pool responses are text; add newline delimiter for Stratum
                        payload = message if message.endswith('\n') else message + '\n'
                        writer.write(payload.encode('utf-8'))
                    else:
                        writer.write(message)
                    await writer.drain()
            except asyncio.CancelledError:
                pass
            except Exception as e:
                log.error(f"WS -> TCP error: {e}")

        # Run both directions concurrently; cancel the other when one ends
        tasks = [
            asyncio.create_task(tcp_to_ws()),
            asyncio.create_task(ws_to_tcp()),
        ]
        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        for task in pending:
            task.cancel()

    except websockets.exceptions.ConnectionClosedError as e:
        log.error(f"WebSocket closed unexpectedly: {e}")
    except Exception as e:
        log.error(f"Failed to connect to relay: {e}")
    finally:
        log.info("Closing local connection.")
        if ws and not ws.closed:
            await ws.close()
        writer.close()
        try:
            await writer.wait_closed()
        except Exception:
            pass


async def main():
    log.info(f"Starting local WS proxy on {LOCAL_HOST}:{LOCAL_PORT}")
    log.info(f"Targeting relay: {RELAY_URL}")

    server = await asyncio.start_server(
        handle_client, LOCAL_HOST, LOCAL_PORT
    )

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info("Proxy stopped.")
