import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from asgiref.sync import async_to_sync


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract employee_id from the URL (e.g., ws://yourdomain.com/ws/employee/123/)
        self.employee_id = self.scope["url_route"]["kwargs"]["employee_id"]
        self.room_name = f"employee_{self.employee_id}"
        print("room_", self.room_name)

        # Join the room
        await self.channel_layer.group_add(self.room_name, self.channel_name)

        # Accept the WebSocket connection
        await self.accept()

        # message
        await self.send(text_data=json.dumps({"message": "Connected"}))

    async def disconnect(self, close_code):
        # Leave the room
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        # Receive data from the customer
        data = json.loads(text_data)

        # You can process the data as needed (e.g., handle appointment details)

        # Broadcast the data to everyone in the room (all connected employees)
        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "notification.message",
                "message": data["message"],
            },
        )

    async def notification_message(self, event):
        # Send the notification message to the connected employee
        message = event["message"]
        await self.send(
            text_data=json.dumps(
                {
                    "type": "notification.message",
                    "message": message,
                }
            )
        )
