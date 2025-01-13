from fastapi import WebSocket
#import RPi.GPIO as GPIO
import time

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def handle_message(self, websocket: WebSocket,  message: str, client_id: str):
        if message == 'POW':
            self.trigger_door()
            await websocket.send_text('You have triggered the batcave')
            announcement = f"{client_id} has triggered the batcave"
            await self.broadcast(announcement)
        else:
            await websocket.send_text(f'I do not understand the message "{message}"')

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    def trigger_door(self):
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup(4, GPIO.OUT, initial=GPIO.HIGH)
        # GPIO.output(4, GPIO.LOW)
        time.sleep(1)
        # GPIO.output(4, GPIO.HIGH)
        # GPIO.cleanup()