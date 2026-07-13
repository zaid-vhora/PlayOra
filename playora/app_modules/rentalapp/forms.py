from django import forms
from app_modules.rentalapp import models

from app_modules.adminapp.models import category, contactmessage, coupon, damagereport, siteSettings, subcategory, toy,  banner




class cate_form(forms.ModelForm):
    class Meta:
        model = category
        fields = '__all__'
        
  
class subc_form(forms.ModelForm):
    class Meta:
        model = subcategory
        fields = '__all__'    
        
        
class toy_form(forms.ModelForm):
    class Meta:
        model = toy
        exclude = ('added_by',) 
        
# class toyi_form(forms.ModelForm):
#     class Meta:
#         model = toyimage
#         fields = '__all__'  
        
class dama_form(forms.ModelForm):
    class Meta:
        model = damagereport
        fields = '__all__' 
        
class bann_form(forms.ModelForm):
    class Meta:
        model = banner
        fields = '__all__'                                  
        
class cont_form(forms.ModelForm):
    class Meta:
        model = contactmessage
        fields = '__all__' 
        
class cou_form(forms.ModelForm):
    class Meta:
        model = coupon
        fields = '__all__'  
        
      
class sit_form(forms.ModelForm):
    class Meta:
        model = siteSettings
        fields = '__all__'                       

class cart_form(forms.ModelForm):
    class Meta:
        model = models.cart
        fields = '__all__'
        
        
class ren_form(forms.ModelForm):
    class Meta:
        model = models.rental
        fields = '__all__'        
        
        
        
class reni_form(forms.ModelForm):
    class Meta:
        model = models.rentalitem
        fields = '__all__'
        


class pay_form(forms.ModelForm):
    class Meta:
        model = models.payment
        fields = '__all__'
        
        
                                
                                
class Ret_form(forms.ModelForm):
    class Meta:
        model = models.ReturnRequest
        fields = '__all__'
        
        
class Ref_form(forms.ModelForm):
    class Meta:
        model = models.Refund
        fields = '__all__'  
        
        
        
class lat_form(forms.ModelForm):
    class Meta:
        model = models.LateFee
        fields = '__all__'                                                
                                