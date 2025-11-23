from django.contrib import admin
from .models import Conference

@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'location', 'format')
    list_filter = ('format', 'start_time', 'location')
    search_fields = ('title', 'location', 'description')
