from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import MenuItem, Menu


@admin.register(MenuItem)
class MenuItemAdmin(ModelAdmin):
    list_display = ('title', 'url', 'parent')


admin.site.register(Menu)
