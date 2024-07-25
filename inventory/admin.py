from django.contrib import admin
from .models import InventoryItem, Category, Warehouse, Profile

admin.site.register(InventoryItem)
admin.site.register(Category)
admin.site.register(Warehouse)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'id']
    raw_id_fields = ['user']