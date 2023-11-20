from django.contrib import admin
from .models import Player

class PlayerAdmin(admin.ModelAdmin):
    search_fields = ['id','name']

admin.site.register(Player, PlayerAdmin)

