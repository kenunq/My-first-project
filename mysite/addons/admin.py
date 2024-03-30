from django.contrib import admin
from django.db.models import TextField
from tinymce.widgets import TinyMCE

from addons.models import Addon, AddonCategory, AddonImage, Compatible_Versions, Order


# Register your models here.


@admin.register(AddonCategory)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Compatible_Versions)
class VersionsAdmin(admin.ModelAdmin):
    list_display = ("version",)


class ImageInline(admin.TabularInline):
    fk_name = "addon"
    model = AddonImage


@admin.register(Addon)
class AddonAdmin(admin.ModelAdmin):
    list_display = ("name", "price")
    inlines = [
        ImageInline,
    ]

    formfield_overrides = {
        TextField: {
            "widget": TinyMCE(
                attrs={"cols": 80, "rows": 30},
                # https://www.tiny.cloud/docs/general-configuration-guide/
                mce_attrs={
                    "skin": "oxide-dark",
                    "content_css": "dark",
                    "readonly": False,
                },
            )
        },
    }


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "addon", "created_at", "status")
    readonly_fields = ("created_at",)
