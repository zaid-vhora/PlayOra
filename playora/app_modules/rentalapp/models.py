from django.db import models

# Create your models here.




class cart (models.Model):
    user =  models.CharField(max_length=100)
    toy =  models.CharField(max_length=100)
    quantity = models.CharField(max_length=100) 
    # image = models.FileField(upload_to='category_image')
    rental_start_date = models.DateField(null=True,blank=True)
    rental_end_date =models.DateField(null=True,blank=True)
    added_at = models.CharField(max_length=100) 
    
class rental (models.Model):
    rental_number = models.IntegerField()
    user_name =  models.CharField(max_length=100)
    toy =  models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)
    rental_start_date = models.DateField(null=True,blank=True)
    rental_end_date =models.DateField(null=True,blank=True)
    actual_return_date =  models.DateField(null=True,blank=True)
    total_days = models.IntegerField()
    rental_amount = models.IntegerField()
    security_deposit = models.IntegerField()
    late_fee = models.IntegerField()
    discount_amount = models.IntegerField()
    total_amount = models.IntegerField()
    status =  models.CharField(max_length=100)
    payment_status = models.CharField(max_length=100)
    created_at =models.DateField(null=True,blank=True)

class rentalitem (models.Model):
    rental_number =  models.ForeignKey(rental,on_delete=models.CASCADE)
    toy =  models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)
    price_per_day  = models.IntegerField()
    total_price = models.IntegerField()
   
   
   
class payment (models.Model):
    # rental_id =  models.ForeignKey(rental,on_delete=models.CASCADE)
    transaction_id = models.IntegerField()
    payment_method = models.CharField(max_length=100)
    amount = models.IntegerField()
    payment_status =  models.CharField(max_length=100)
    paid_at = models.DateField(null=True,blank=True)
    


class ReturnRequest (models.Model): 
    # rental_id =  models.ForeignKey(rental,on_delete=models.CASCADE)
    user =  models.CharField(max_length=100)
    return_reason =   models.CharField(max_length=100)
    approval_status =  models.BooleanField()
    requested_at = models.DateField(null=True,blank=True)
    approved_at = models.DateField(null=True,blank=True)
    
    
    
class Refund  (models.Model): 
    # rental_id =  models.ForeignKey(rental,on_delete=models.CASCADE)
    refund_amount = models.IntegerField() 
    refund_status = models.CharField(max_length=100)
    refund_date = models.DateField(null=True,blank=True)
    refund_transaction_id =  models.IntegerField() 




class LateFee   (models.Model):
    rental_id =  models.ForeignKey(rental,on_delete=models.CASCADE)
    extra_days = models.IntegerField() 
    fee_per_day = models.IntegerField()
    total_late_fee = models.IntegerField()
    calculated_at = models.DateField(null=True,blank=True)

