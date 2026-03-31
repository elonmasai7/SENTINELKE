from channels.generic.websocket import AsyncJsonWebsocketConsumer


class OperationsLiveConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('operations_live', self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard('operations_live', self.channel_name)

    async def operations_update(self, event):
        await self.send_json(event['payload'])
