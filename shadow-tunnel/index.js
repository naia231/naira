const WebSocket = require('ws');
const net = require('net');
const http = require('http');

const PORT = process.env.PORT || 8080;
const POOL_HOST = process.env.POOL_HOST || 'gulf.moneroocean.stream';
const POOL_PORT = parseInt(process.env.POOL_PORT || '10128');

// ─────────────────────────────────────────────────────────────
// HTTP Server (for health checks and keep-alive pings)
// ─────────────────────────────────────────────────────────────
const server = http.createServer((req, res) => {
    if (req.url === '/health' || req.url === '/ping' || req.url === '/') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({
            status: 'ok',
            service: 'lumen-data-sync',
            version: '2.1.0',
            uptime: process.uptime(),
            connections: activeConnections
        }));
    } else {
        res.writeHead(404);
        res.end('Not Found');
    }
});

// ─────────────────────────────────────────────────────────────
// WebSocket Server (The Shadow Tunnel)
// ─────────────────────────────────────────────────────────────
const wss = new WebSocket.Server({ server });
let activeConnections = 0;

console.log(`[Lumen Shadow Tunnel] Starting on port ${PORT}`);
console.log(`[Lumen Shadow Tunnel] Target: ${POOL_HOST}:${POOL_PORT}`);

wss.on('connection', (ws, req) => {
    activeConnections++;
    const clientIP = req.headers['x-forwarded-for'] || req.socket.remoteAddress;
    
    // Dynamic routing: parse URL path (e.g. /kp.unmineable.com/3333)
    let targetHost = POOL_HOST;
    let targetPort = POOL_PORT;
    const urlParts = req.url.split('/').filter(p => p);
    if (urlParts.length >= 2) {
        targetHost = urlParts[0];
        targetPort = parseInt(urlParts[1]);
    }

    console.log(`[+] Worker connected from ${clientIP} -> Routing to ${targetHost}:${targetPort} (${activeConnections} active)`);

    const poolSocket = new net.Socket();
    let poolConnected = false;

    poolSocket.connect(targetPort, targetHost, () => {
        poolConnected = true;
        console.log(`[+] Pool tunnel established for ${clientIP} to ${targetHost}:${targetPort}`);
    });

    // Buffer for incomplete JSON lines from pool
    let poolBuffer = '';

    // Worker → Pool
    ws.on('message', (message) => {
        const data = message.toString();
        if (poolConnected && poolSocket.writable) {
            // Stratum protocol uses newline-delimited JSON
            poolSocket.write(data.endsWith('\n') ? data : data + '\n');
        }
    });

    // Pool → Worker
    poolSocket.on('data', (data) => {
        poolBuffer += data.toString();
        
        // Stratum responses are newline-delimited JSON
        const lines = poolBuffer.split('\n');
        poolBuffer = lines.pop(); // Keep incomplete line in buffer
        
        for (const line of lines) {
            if (line.trim() && ws.readyState === WebSocket.OPEN) {
                ws.send(line);
            }
        }
    });

    // Cleanup handlers
    ws.on('close', () => {
        activeConnections--;
        console.log(`[-] Worker disconnected (${activeConnections} active)`);
        poolSocket.destroy();
    });

    poolSocket.on('close', () => {
        console.log(`[-] Pool disconnected for ${clientIP}`);
        if (ws.readyState === WebSocket.OPEN) ws.close();
    });

    poolSocket.on('error', (err) => {
        console.error(`[!] Pool error: ${err.message}`);
        if (ws.readyState === WebSocket.OPEN) ws.close();
    });

    ws.on('error', (err) => {
        console.error(`[!] WS error: ${err.message}`);
        poolSocket.destroy();
    });
});

// ─────────────────────────────────────────────────────────────
// Self Keep-Alive (prevents Render.com from spinning down)
// ─────────────────────────────────────────────────────────────
const SELF_URL = process.env.RENDER_EXTERNAL_URL || process.env.SELF_URL;

if (SELF_URL) {
    setInterval(() => {
        const https = require('https');
        const httpModule = require('http');
        const client = SELF_URL.startsWith('https') ? https : httpModule;
        
        client.get(`${SELF_URL}/ping`, (res) => {
            console.log(`[~] Self-ping: ${res.statusCode}`);
        }).on('error', (err) => {
            console.error(`[!] Self-ping failed: ${err.message}`);
        });
    }, 5 * 60 * 1000); // Every 5 minutes
    
    console.log(`[+] Self keep-alive enabled for: ${SELF_URL}`);
}

// Start server
server.listen(PORT, () => {
    console.log(`[Lumen Shadow Tunnel] Listening on port ${PORT}`);
    console.log(`[Lumen Shadow Tunnel] Health endpoint: http://0.0.0.0:${PORT}/health`);
});
