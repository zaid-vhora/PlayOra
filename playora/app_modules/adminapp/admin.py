from django.contrib import admin
from app_modules.adminapp import models

# Register your models here.
admin.site.register(models.category)
admin.site.register(models.subcategory)
admin.site.register(models.toy)
# admin.site.register(models.toyimage)
admin.site.register(models.damagereport)
admin.site.register(models.banner)
admin.site.register(models.contactmessage)
admin.site.register(models.coupon)
admin.site.register(models.siteSettings)
