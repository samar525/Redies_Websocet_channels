import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ProductConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("products", self.channel_name)
        await self.accept()
        print("📡 WebSocket Connected!")  # ✅ تأكد من اتصال WebSocket

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("products", self.channel_name)
        print("❌ WebSocket Disconnected!")  # ✅ تأكد من قطع الاتصال

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(f"📩 Received Message: {data}")  # ✅ تحقق من استلام البيانات

        await self.channel_layer.group_send(
            "products",
            {
                "type": "send_update",
                "message": data["message"]
            }
        )

    async def send_update(self, event):
        print(f"📢 Sending Update: {event}")  # ✅ تأكد من إرسال الرسائل
        await self.send(text_data=json.dumps({"message": event["message"]}))
