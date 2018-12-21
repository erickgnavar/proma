from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):

    list_display = ("name", "client", "status", "start_date", "end_date")
    search_fields = ("name", "client__name")
    list_filter = ("status", "payment_type", "currency")
