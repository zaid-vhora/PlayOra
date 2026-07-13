from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):

    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        RENTAL = 'RENTAL', 'Rental'
        USER = 'USER', 'User'

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]


    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    emergency_contact = models.CharField(max_length=15, blank=True, null=True)
    alternate_phone = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=10,choices=Role.choices,default=Role.USER)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    # name = models.CharField(max_length=125) 
    # image = models.ImageField(upload_to='products/') 
    # price = models.FloatField()

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_rental(self):
        return self.role == self.Role.RENTAL

    @property
    def is_user(self):
        return self.role == self.Role.USER  