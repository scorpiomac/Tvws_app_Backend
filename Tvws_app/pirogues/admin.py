from django.contrib import admin
from .models import *

class PirogueAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'tel', 'is_marine')
    search_fields = ('first_name', 'last_name', 'tel')
    list_filter = ('is_marine',)
    
class PositionAdmin(admin.ModelAdmin):
    list_display = ('pirogue', 'latitude', 'longitude', 'timestamp')
    search_fields = ('pirogue__first_name', 'pirogue__last_name')
    list_filter = ('timestamp',)
    raw_id_fields = ('pirogue',)

admin.site.register(Pirogue, PirogueAdmin)
admin.site.register(Position, PositionAdmin)