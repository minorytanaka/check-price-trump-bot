import asyncio
import websockets
import json


async def on_message(websocket):
    async for message in websocket:
        data = json.loads(message)
        print(data.get("p"))

async def subscribe():
    uri = "wss://fstream.binance.com/ws/trumpusdt@aggTrade"
    async with websockets.connect(uri) as websocket:
        # Subscribe to the stream
        subscription_message = {
            "method": "SUBSCRIBE",
            "params": ["trumpusdt@aggTrade"],
            "id": 1,
        }
        await websocket.send(json.dumps(subscription_message))

        # Process incoming messages
        await on_message(websocket)


if __name__ == "__main__":
    asyncio.run(subscribe())
