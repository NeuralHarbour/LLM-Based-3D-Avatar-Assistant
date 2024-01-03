import asyncio
import websockets

async def send_message(websocket, message):
    await websocket.send(message)
    response = await websocket.recv()
    print(f"Received response: {response}")

async def send_messages_continuously(websocket):
    while True:
        message_to_send = input("Enter Your Message (type 'exit' to quit): ")
        if message_to_send.lower() == 'exit':
            break
        await send_message(websocket, message_to_send.strip())  # Strip to remove leading/trailing whitespaces

async def main():
    # Replace 'localhost' and '8080' with the actual host and port of your server
    server_uri = "ws://localhost:8080"

    async with websockets.connect(server_uri) as websocket:
        await send_messages_continuously(websocket)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
