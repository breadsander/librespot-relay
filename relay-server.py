#!/usr/bin/env python3
import asyncio
import websockets
import json
import os

FIFO_PATH = "/tmp/spotify_events.fifo"
WS_PORT = 24879

clients = set()

async def fifo_reader():
    """Continuously read lines from the FIFO and broadcast to clients."""
    while True:
        with open(FIFO_PATH, "r") as fifo:
            for line in fifo:
                line = line.strip()
                if not line:
                    continue
                event = json.loads(line)
                await broadcast(event)

async def broadcast(event):
    """Send event to all connected WebSocket clients."""
    dead_clients = set()
    for ws in clients:
        try:
            await ws.send(json.dumps(event))
        except:
            dead_clients.add(ws)
    clients.difference_update(dead_clients)

async def ws_handler(websocket, path):
    clients.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        clients.remove(websocket)

async def main():
    server = await websockets.serve(ws_handler, "192.168.1.12", WS_PORT)
    print(f"WebSocket server listening on port {WS_PORT}")

    # Run fifo_reader as a background task
    asyncio.create_task(fifo_reader())
    
    # Keep the server running forever
    await asyncio.Future()  # run forever
    
asyncio.run(main())
