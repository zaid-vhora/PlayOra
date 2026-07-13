from django.db import models
from django.conf import settings



# Create your models here.

class category(models.Model):
    name =  models.CharField(max_length=100)
    description = models.TextField()
    image = models.FileField(upload_to='category_image')
    is_active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name    

    
    
class subcategory (models.Model):
    category =  models.ForeignKey(category,on_delete=models.CASCADE)
    name =  models.CharField(max_length=100)
    description = models.TextField()
    is_active = models.BooleanField()
    created_at =models.DateTimeField(auto_now_add=True)  
    
    def __str__(self):
        return self.name    

class toy (models.Model):
    category =  models.ForeignKey(category,on_delete=models.CASCADE, null=True, blank=True)
    subcategory = models.ForeignKey(subcategory,on_delete=models.CASCADE, null=True, blank=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    name =  models.CharField(max_length=100)
    description = models.TextField()
    long_description = models.TextField(null=True, blank=True)
    whats_included = models.TextField(null=True, blank=True)
    brand = models.CharField(max_length=255)
    age_group = models.CharField(max_length=255)
    rental_price_per_week = models.IntegerField()
    security_deposit = models.IntegerField()
    stock_quantity = models.IntegerField()
    available_quantity = models.IntegerField()
    condition = models.CharField(max_length=100)
    image = models.FileField(upload_to='toy_image')
    is_available = models.BooleanField(default=True)
    is_popular = models.BooleanField(default=False)
    is_on_sale = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name    
    
# class toyimage (models.Model):
#     toy = models.ForeignKey(toy, on_delete=models.CASCADE)
#     image = models.FileField(upload_to='toyimage_image')
#     uploaded_at = models.DateTimeField(auto_now_add=True) 

    # def __str__(self):
    #     return str(self.toy)
    
class damagereport (models.Model):  
    toys = models.ForeignKey(toy, on_delete=models.CASCADE)
    description = models.TextField()
    fine_amount =  models.IntegerField()
    resolved = models.DateField(null=True , blank=True)
    reportedss_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
class banner(models.Model):
    title = models.CharField(max_length=100)
    image = models.FileField(upload_to='banner_image')
    description = models.TextField()
    is_active = models.BooleanField()
    created_at =models.DateField(null=True , blank=True)    
    
class contactmessage(models.Model):
    name =  models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=100)
    is_replied  =  models.CharField(max_length=100)  
    created_at =models.DateField(null=True , blank=True)
    
    
class coupon(models.Model):
    code  = models.IntegerField()
    discount_type = models.CharField(max_length=100)
    discount_value = models.IntegerField()
    minimum_amount = models.IntegerField()
    expiry_date = models.DateField(null=True , blank=True)
    is_active = models.BooleanField()
    created_at = models.DateField(null=True , blank=True)
            

class siteSettings(models.Model):
    site_name  =  models.CharField(max_length=100)
    logo  =  models.FileField(upload_to='siteSettings_logo')
    contact_email  =   models.EmailField()
    contact_phone  =  models.CharField(max_length=15)
    address  =  models.CharField(max_length=100)
    late_fee_per_day  =   models.IntegerField()
    deposit_policy  =   models.IntegerField()
    updated_at  = models.DateField(null=True , blank=True) 


    
    
        


    





class RentalRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        REJECTED = 'REJECTED', 'Rejected'
        PAID = 'PAID', 'Paid'
        SHIPPED = 'SHIPPED', 'Shipped'
        DELIVERING = 'DELIVERING', 'Out for Delivery'
        COMPLETED = 'COMPLETED', 'Delivered'

    class PaymentMethod(models.TextChoices):
        CARD = 'CARD', 'Credit/Debit Card'
        COD = 'COD', 'Cash on Delivery'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rental_requests')
    toy = models.ForeignKey(toy, on_delete=models.CASCADE)
    rental_provider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='provided_rentals')
    quantity = models.IntegerField()
    total_price = models.FloatField()
    security_deposit = models.FloatField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.CARD)

    
    # Delivery Info
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=20, null=True, blank=True)
    delivery_date = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Rental Duration Info
    rental_duration_weeks = models.IntegerField(default=1)
    rental_end_date = models.DateField(null=True, blank=True)
    is_extension = models.BooleanField(default=False)
    original_rental = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='extensions')

    def __str__(self):
        return f"{self.user.username} - {self.toy.name} ({self.status})"

    @property
    def days_remaining(self):
        from datetime import date
        if self.rental_end_date:
            today = date.today()
            delta = self.rental_end_date - today
            return delta.days
        return None

    @property
    def days_overdue(self):
        days = self.days_remaining
        if days is not None and days < 0:
            return abs(days)
        return 0
