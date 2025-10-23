from django.contrib import admin
from .models import Price, ClubInfo

@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('time_period', 'price', 'duration', 'is_dinner_price')
    list_filter = ('is_dinner_price',)

@admin.register(ClubInfo)
class ClubInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')