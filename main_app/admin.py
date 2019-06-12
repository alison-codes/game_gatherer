from django.contrib import admin

# Register your models here.
from .models import Game, Played

admin.site.register(Game)
admin.site.register(Played)