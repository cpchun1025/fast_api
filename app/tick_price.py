import asyncio
import websockets
import json

async def subscribe_to_ticker(websocket, symbol):
    subscribe_message = json.dumps({
        "method": "SUBSCRIBE",
        "params": [
            f"{symbol}@ticker"
        ],
        "id": 1
    })
    await websocket.send(subscribe_message)

async def ticker(websocket, symbol):
    await subscribe_to_ticker(websocket, symbol)
    while True:
        response = await websocket.recv()
        data = json.loads(response)
        # Process the data (e.g., store it in a database)
        print(f"Ticker for {symbol}: {data}")

async def main(symbols):
    connection_tasks = []
    websocket_uri = "wss://api.yourprovider.com/ws"
    
    async with websockets.connect(websocket_uri) as websocket:
        for symbol in symbols:
            task = asyncio.create_task(ticker(websocket, symbol))
            connection_tasks.append(task)

        await asyncio.gather(*connection_tasks)

symbols = [f"{i:04}.HK" for i in range(1, 1001)]  # Generate a list of ticker symbols in the format 0001.HK to 1000.HK

asyncio.run(main(symbols))