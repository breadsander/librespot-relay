import asyncio
import websockets
import json

WS_HOST = "192.168.1.12"
WS_PORT = 24879

TCP_HOST = "127.0.0.1"
TCP_PORT = 24880

connected_websockets = set()

async def handle_tcp_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"TCP client connected: {addr}")

    try:
        while data := await reader.readline():
            msg_text = data.decode().strip()
            if not msg_text:
                continue

            try:
                message = json.loads(msg_text)  # Parse JSON from TCP
                print(f"Received JSON: {message}")
                await broadcast_to_websockets(message)
            except json.JSONDecodeError:
                print(f"Invalid JSON received: {msg_text}")
    except Exception as e:
        print(f"TCP client error: {e}")
    finally:
        writer.close()
        await writer.wait_closed()
        print(f"TCP client disconnected: {addr}")

async def websocket_handler(websocket):
    connected_websockets.add(websocket)
    print("WebSocket client connected.")
    try:
        async for _ in websocket:
            pass  # Ignore incoming WS messages
    finally:
        connected_websockets.remove(websocket)
        print("WebSocket client disconnected.")

async def broadcast_to_websockets(message):
    """Broadcast a Python dict as JSON to all WebSocket clients."""
    if not connected_websockets:
        return
    msg_text = json.dumps(message)
    await asyncio.gather(*[ws.send(msg_text) for ws in connected_websockets])

async def main():
    tcp_server = await asyncio.start_server(handle_tcp_client, TCP_HOST, TCP_PORT)
    ws_server = await websockets.serve(websocket_handler, WS_HOST, WS_PORT)

    print(f"TCP server listening on {TCP_HOST}:{TCP_PORT}")
    print(f"WebSocket server listening on ws://{WS_HOST}:{WS_PORT}")

    async with tcp_server, ws_server:
        await asyncio.gather(tcp_server.serve_forever(), ws_server.wait_closed())

if __name__ == "__main__":
    asyncio.run(main())
