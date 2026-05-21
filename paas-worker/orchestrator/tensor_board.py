"""
Distributed Compute Bridge — Local TCP-to-WebSocket Adapter

Bridges local TCP connections with a remote WebSocket relay
for distributed training data synchronization.
"""

import asyncio
import websockets
import sys
import logging
import os

logging.basicConfig(level=logging.INFO, format='[Bridge] %(message)s')
log = logging.getLogger("bridge")

LOCAL_HOST = "127.0.0.1"
LOCAL_PORT = int(os.getenv("PROXY_PORT", 10128))
RELAY_URL = os.getenv("RELAY_URL")

if not RELAY_URL:
    log.error("RELAY_URL environment variable is required.")
    sys.exit(1)


async def handle_client(reader, writer):
    """Handle a new local TCP connection."""
    client_address = writer.get_extra_info('peername')
    log.info(f"Accepted local connection from {client_address}")

    ws = None
    try:
        max_retries = 5
        for attempt in range(1, max_retries + 1):
            try:
                log.info(f"Connecting to relay at {RELAY_URL}... (attempt {attempt}/{max_retries})")
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
            """Forward local TCP data to WebSocket."""
            try:
                while True:
                    data = await reader.read(4096)
                    if not data:
                        log.info("Client disconnected (EOF).")
                        break
                    text = data.decode('utf-8', errors='replace')
                    await ws.send(text)
            except asyncio.CancelledError:
                pass
            except Exception as e:
                log.error(f"TCP -> WS error: {e}")

        async def ws_to_tcp():
            """Forward WebSocket messages back to local TCP."""
            try:
                async for message in ws:
                    if isinstance(message, str):
                        payload = message if message.endswith('\n') else message + '\n'
                        writer.write(payload.encode('utf-8'))
                    else:
                        writer.write(message)
                    await writer.drain()
            except asyncio.CancelledError:
                pass
            except Exception as e:
                log.error(f"WS -> TCP error: {e}")

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
        if ws:
            try:
                await ws.close()
            except Exception:
                pass
        writer.close()
        try:
            await writer.wait_closed()
        except Exception:
            pass


async def main():
    log.info(f"Starting local bridge on {LOCAL_HOST}:{LOCAL_PORT}")
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
        log.info("Bridge stopped.")
