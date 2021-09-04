"""
ASGI config for apexindustries project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""



import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path

from apex.consumer import *

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apexindustries.settings')
django.setup()
application = get_asgi_application()

ws_patterns = [
    path('ws/alert/', AlertSystem),
    path('ws/user-alert/<room_code>/', UserAlert)
]

application = ProtocolTypeRouter({
    'websocket' : AuthMiddlewareStack(URLRouter(ws_patterns))
})