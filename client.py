import asyncio
import websockets
import json

if __name__ == "__main__":
    print("Echo client")

async def main():
    uri = "ws://localhost:6789"
    async with websockets.connect(uri) as websocket:
        # After joining server will send client unique id.
        message = json.loads(await websocket.recv())
        print(message)
        # Get the client_id from the join message
        if message['type'] == 'join_evt':
            client_id = message['client_id']
        else:
            # If first message is not the join message exit
            print("Did not receive a correct join message")

        async def send_message(websocket, message, client_id):
            outward_message = {
                'client_id': client_id,
                'payload': message
            }
            await websocket.send(json.dumps(outward_message))

        async def recv_message(websocket):
            message = json.loads(await websocket.recv())
            return message['payload']

        # Send a ping to the server
        await send_message(websocket, 'ping', client_id)
        # Wait for the 'ping' response from the server
        response = await recv_message(websocket)

        print("The Server Sent Back:")
        print(response)
    
    return 0

asyncio.run(main())


