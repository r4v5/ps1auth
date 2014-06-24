from django.contrib import admin
from .models import PointAccount, PointTransaction

class TransactionInline(admin.TabularInline):
    model = PointTransaction
    extra = 0

class PointAdmin(admin.ModelAdmin):
    fields = ['user']
    inlines = [TransactionInline]
    #search_fields = ['user']

admin.site.register(PointAccount, PointAdmin)

