from django.contrib import admin

# Register your models here.
from . import models


class StationAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name", "slug"]


admin.site.register(models.Station, StationAdmin)
