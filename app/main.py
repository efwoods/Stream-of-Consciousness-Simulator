
async def send_data():
    uri = "ws://localhost:8000/ws"  # replace with your server URL
    async with websockets.connect(uri) as websocket:
        # Create data
        np_data = np.random.rand(4, 4).astype(np.float32)  # example data

        # Create metadata
        meta_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "source": "brainstream_simulator",
            "signal_type": "EEG",
        }

        # Serialize
        message = create_message(np_data, meta_data)

        # Send over websocket
        await websocket.send(message)
        print("Data sent.")

# Run client
asyncio.run(send_data())