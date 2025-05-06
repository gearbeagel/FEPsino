from django.contrib import admin
from .models import Spin, Symbol

@admin.register(Spin)
class SpinAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'bet_amount', 'payout', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('user__username',)

@admin.register(Symbol)
class SymbolAdmin(admin.ModelAdmin):
    list_display = ('name', 'payout_multiplier')
    search_fields = ('name',)
