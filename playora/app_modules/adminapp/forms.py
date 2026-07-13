from django import forms
from app_modules.adminapp import models




class cate_form(forms.ModelForm):
    class Meta:
        model = models.category
        fields = '__all__'
        
    
class subc_form(forms.ModelForm):
    class Meta:
        model = models.subcategory
        fields = '__all__'        
        
class toy_form(forms.ModelForm):
    class Meta:
        model = models.toy
        exclude = ('added_by',) 
        
# class toyi_form(forms.ModelForm):
#     class Meta:
#         model = models.toyimage
#         fields = '__all__' 
        
class dama_form(forms.ModelForm):
    class Meta:
        model = models.damagereport
        fields = '__all__'
        
class bann_form(forms.ModelForm):
    class Meta:
        model = models.banner
        fields = '__all__'
       
class cont_form(forms.ModelForm):
    class Meta:
        model = models.contactmessage
        fields = '__all__'   
        
class cou_form(forms.ModelForm):
    class Meta:
        model = models.coupon
        fields = '__all__'  
        
      
class sit_form(forms.ModelForm):
    class Meta:
        model = models.siteSettings
        fields = '__all__'                 
        
                              
        
        
                               