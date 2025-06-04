from django.contrib import admin
from currency_app.models import CurrencyRate


@admin.register(CurrencyRate)
class CurrencyRateAdmin(admin.ModelAdmin):
    list_display = ['rate', 'source', 'timestamp']
    list_filter = ['source', 'timestamp']
    readonly_fields = ['timestamp']
    ordering = ['-timestamp']
