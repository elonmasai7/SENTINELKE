from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from .models import LiveAssetPosition


class OperationsLiveConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('operations_live', self.channel_name)
        await self.accept()
        await self.send_json(
            {
                'event': 'bootstrap',
                'positions': await self._recent_positions(),
            }
        )

    async def disconnect(self, code):
        await self.channel_layer.group_discard('operations_live', self.channel_name)

    async def operations_update(self, event):
        await self.send_json(event['payload'])

    @sync_to_async
    def _recent_positions(self):
        positions = []
        for position in LiveAssetPosition.objects.order_by('-observed_at')[:12]:
            location = position.location or {}
            positions.append(
                {
                    'event': 'live_position',
                    'id': position.id,
                    'asset_type': position.asset_type,
                    'identifier': position.identifier,
                    'location': location,
                    'lat': location.get('lat') or location.get('latitude'),
                    'lng': location.get('lng') or location.get('longitude'),
                    'label': location.get('label') or position.identifier,
                    'threat_overlay': position.threat_overlay,
                    'observed_at': position.observed_at.isoformat(),
                }
            )
        return positions
