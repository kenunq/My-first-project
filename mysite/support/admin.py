from django.contrib import admin

from support.models import ChatRoom, Message


# Register your models here.

admin.site.register(Message)


@admin.register(ChatRoom)
class CharRoomAdmin(admin.ModelAdmin):
    model: ChatRoom = ChatRoom

    list_display = (
        "slug",
        "state",
    )

    search_fields = ("user",)
