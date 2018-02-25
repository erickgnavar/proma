from django.contrib import admin

from .models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):

    list_display = ('number', 'client', 'status', 'issue_date', 'due_date')
    search_fields = ('number', 'client__name')
    list_filter = ('status', 'client', 'project')
