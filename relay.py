#!/usr/bin/env python3
import asyncio
import websockets
import json
import os

FIFO = "/tmp/spotify_events.fifo"
if not os.path.exists(FIFO):
    os.mkfifo(FIFO)

async def relay():
    uri = "ws://192.168.1.12:24879"
    async with websockets.connect(uri) as websocket:
        while True:
            with open(FIFO) as f:
                for line in f:
                    event = json.loads(line)
                    print(event)
                    await websocket.send(json.dumps(event))

asyncio.run(relay())
