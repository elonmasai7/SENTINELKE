from django.urls import re_path

from .consumers import OperationsLiveConsumer

websocket_urlpatterns = [
    re_path(r'ws/operations/live/$', OperationsLiveConsumer.as_asgi()),
]
