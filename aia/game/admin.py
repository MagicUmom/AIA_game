from django.contrib import admin

# Register your models here.
from .models import game_detail
from .models import game_overview

admin.site.register(game_detail)
admin.site.register(game_overview)
