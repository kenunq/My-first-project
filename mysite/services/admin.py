from django.contrib import admin

from services.models import (
    ClassModel,
    CommunicationModel,
    FractionModel,
    MentorModel,
    ServerModel,
    ServicesModel,
    TypeModel,
)


# Register your models here.


@admin.register(ServicesModel)
class ServicesModelAdmin(admin.ModelAdmin):
    list_display = (
        "type",
        "class_name",
        "mentor",
    )

    search_fields = ("mentor",)


admin.site.register(TypeModel)

admin.site.register(ServerModel)

admin.site.register(FractionModel)

admin.site.register(ClassModel)

admin.site.register(MentorModel)

admin.site.register(CommunicationModel)
