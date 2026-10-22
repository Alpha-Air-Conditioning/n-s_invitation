from django.contrib import admin
from .models import RSVP

@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "guests", "side", "attendance", "created_at")
    list_filter = ("attendance", "side", "created_at")
    search_fields = ("name", "phone", "message")
    readonly_fields = ("created_at",)
