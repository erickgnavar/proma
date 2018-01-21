from django.contrib import admin

from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):

    list_display = ('name', 'email', 'status', 'tax_identifier')
    search_fields = ('name', 'email')
    list_filter = ('status',)
