from django.urls import re_path

from support import consumers


websocket_urlpatterns = [
    re_path(r"ws/support/chat/(?P<user_id>[\w\d\-]+)/$", consumers.ChatConsumer.as_asgi()),
    re_path("ws/support/chat/admin/", consumers.AdminChatConsumer.as_asgi()),
]
