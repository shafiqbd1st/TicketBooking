from django.contrib import admin
from .import models
# Register your models here.

admin.site.register(models.Train)
admin.site.register(models.UserProfile)
admin.site.register(models.BuyTicket)
admin.site.register(models.Comment)
