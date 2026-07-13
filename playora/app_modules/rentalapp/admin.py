from django.contrib import admin
from app_modules.rentalapp import models

# Register your models here.
admin.site.register(models.cart)
admin.site.register(models.rental)
admin.site.register(models.rentalitem)
admin.site.register(models.payment)
admin.site.register(models.ReturnRequest)
admin.site.register(models.Refund)
admin.site.register(models.LateFee)

