import asyncio
import websockets

async def send_message(websocket, message):
    try:
        await websocket.send(message)
        response = await websocket.recv()
        print(f"Received response: {response}")
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Connection closed unexpectedly: {e}")

async def send_messages_continuously(websocket):
    while True:
        message_to_send = input("Enter Your Message (type 'exit' to quit): ")
        if message_to_send.lower() == 'exit':
            break
        try:
            await send_message(websocket, message_to_send.strip())
        except Exception as e:
            print(f"An error occurred: {e}")

async def main():
    server_uri = "ws://localhost:8080"
    try:
        async with websockets.connect(server_uri) as websocket:
            await send_messages_continuously(websocket)
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Failed to connect to the server: {e}")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())

