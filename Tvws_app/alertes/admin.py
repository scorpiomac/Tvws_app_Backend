from django.contrib import admin
from .models import *

class AlerteAdmin(admin.ModelAdmin):
    list_display = ('pirogue', 'message', 'type_alerte', 'timestamp')
    search_fields = ('message', 'type_alerte')
    list_filter = ('type_alerte', 'timestamp')

admin.site.register(Alerte, AlerteAdmin)
