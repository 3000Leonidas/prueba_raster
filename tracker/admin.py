from django.contrib import admin
from .models import TrackerURL, Visit


# Register your models here.
@admin.register(TrackerURL)
class TrackerURLAdmin(admin.ModelAdmin):
    list_display = ('name', 'tracker_id','created_at')
    readonly_fields = ('tracker_id',)

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('tracker_url', 'ip_address', 'country', 'city', 'timestamp')
    list_filter = ('tracker_url', 'country') 
    search_fields = ('ip_address', 'user_agent')
    