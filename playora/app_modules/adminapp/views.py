from django.shortcuts import render, redirect, get_object_or_404
from app_modules.adminapp import forms
from app_modules.adminapp import models
from django.http import HttpResponse
from django.contrib import messages


from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate


from django.contrib.auth.decorators import login_required


# Create your views here. 




#  chart
# def chartjs_view(request):
#     return render(request,'tmp_admin/chart/chartjs.html')

# forms
# def basicelements_view(request):
#     return render(request,'tmp_admin/forms/basicelements.html')


# icnos
# def mdi_view(request):
#     return render(request,'tmp_admin/icnos/mdi.html')    

from app_modules.userapp.models import CustomUser

# index
# def adminindex_view(request):
    
    
#     approved_users = CustomUser.objects.filter(is_approved=True, role__in=['rental', 'User'])
#     rejected_users = CustomUser.objects.filter(is_approved=False, role__in=['rental', 'User'])

#     custo = CustomUser.objects.all()
#     context = {'custo': custo,'approved_users':approved_users, 'rejected_users':rejected_users}
#     return render(request,'tmp_admin/index/adminindex.html',context)

@login_required
def adminindex_view(request):
    
    approved_rental = CustomUser.objects.filter(is_approved=True, role__in=['rental'])
    rejected_rental = CustomUser.objects.filter(is_approved=False, role__in=['rental'])

    custo = CustomUser.objects.all()
    context = {'custo': custo,'approved_rental':approved_rental, 'rejected_users':rejected_rental}
    
    if request.user.role.upper() != 'ADMIN':
        return redirect('login')

    return render(request, 'tmp_admin/index/adminindex.html',context)


#tables 
# def basictable_view(request):
#     return render(request,'tmp_admin/tables/basictable.html') 

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('login')

# def login_view(request):
#     if request.method =='POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(username = username,password = password  )
#         if user is not None:
#             login(request,user)
#             return redirect(adminindex_view)
#         else:
#             return HttpResponse("user does not exits")
#     return render(request,'tmp_admin/demologin.html') 


# def register_view(request):
#     if request.method =='POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         password1 = request.POST.get('password1')
        
        
#         if password ==password1:
           
#             try:
#                 User.objects.get(username==username)
#                 return HttpResponse("username alredy exits please Try Again")
#             except:
#                 User.objects.create_user(username = username,password = password)
#                 return redirect(login_view)
#         else:
            
#             return HttpResponse("password do not match!!!")
#     return render(request,'tmp_admin/register.html') 

# def logout_view(request):
#     logout(request)
#     return redirect(login_view)


    

# ____________________________________________________________________________________________________________________________________________________________________________________________-
# import random
# import string
# from django.shortcuts import render, redirect

# def generate_captcha():
#     return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))


# def login_view(request):

#     # ✅ Always generate new captcha on GET
#     if request.method == "GET":
#         request.session['captcha_text'] = generate_captcha()

#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         captcha_input = request.POST.get('captcha')

#         session_captcha = request.session.get('captcha_text')

#         # ✅ Validate captcha
#         if captcha_input != session_captcha:
#             # regenerate captcha again on failure
#             request.session['captcha_text'] = generate_captcha()

#             return render(request, 'login.html', {
#                 'error': 'Invalid captcha'
#             })

#         # ✅ success
#         return redirect('home')

#     return render(request, 'tmp_admin/login.html')







# ________________________________________________________________________________________________________________________________________________________________________________________________
# import random
# import string

# # Generate captcha
# def generate_captcha():
#     return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))


# def register_view(request):

#     # Generate captcha on GET
#     if request.method == "GET":
#         request.session['captcha_text'] = generate_captcha()

#     if request.method == "POST":

#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         mobile = request.POST.get('mobile')
#         city = request.POST.get('city')
#         password = request.POST.get('password')
#         confirm_password = request.POST.get('confirm_password')
#         captcha_input = request.POST.get('captcha')

#         # STEP 3: CAPTCHA VALIDATION
#         session_captcha = request.session.get('captcha_text')

#         if captcha_input != session_captcha:
#             request.session['captcha_text'] = generate_captcha()
#             return render(request, 'register.html', {
#                 'error': 'Invalid captcha'
#             })

#         # PASSWORD MATCH CHECK
#         if password != confirm_password:
#             request.session['captcha_text'] = generate_captcha()
#             return render(request, 'register.html', {
#                 'error': 'Passwords do not match'
#             })

        
#         return redirect('login_view')

#     return render(request, 'tmp_admin/register.html')
# __________________________________________________________________________________________________________________________________________________________________________________________________________




#ui_features
# def buttons_view(request):
#     return render(request,'tmp_admin/ui_features/buttons.html')
# def dropdowns_view(request):
#     return render(request,'tmp_admin/ui_features/dropdowns.html')
# def typography_view(request):
#     return render(request,'tmp_admin/ui_features/typography.html')

    
    
 # MY MODELS
 
 

def create_category(request):
    if request.method == 'POST':
        form = forms.cate_form(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect(list_category)
        else:
            print(form.errors)
    return render(request,'tmp_admin/create_category.html')  

def list_category(request):
    cate =  models.category.objects.all()
    context = {'cate': cate }
    return render (request,'tmp_admin/list_category.html',context)  

def update_category(request,id):
    cate = get_object_or_404(models.category, id=id)   
    if request.method == 'POST':
        form = forms.cate_form(request.POST, request.FILES, instance=cate)
        if form.is_valid():
            form.save()
            return redirect(list_category)
        else:
            form.errors
    context = {'cate': cate }
    return render(request,'tmp_admin/update_category.html',context)         
        
        
def delete_category(request, id):
    try:
        cate = models.category.objects.get(id=id)
        cate.delete()
        messages.success(request, "Category deleted successfully.")
    except models.category.DoesNotExist:
        messages.warning(request, "Category not found or already deleted.")
    return redirect(list_category)
    
            
# ______________________________________________________________________________________________________________________________________________________________


def create_subcategory(request):
    category = models.category.objects.all()
    if request.method == 'POST':
        form = forms.subc_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_subcategory)
        else:
            print(form.errors)
    context = {'category':category}           
    return render(request,'tmp_admin/create_subcategory.html', context) 


def list_subcategory(request):
    subc = models.subcategory.objects.all()
    context = {'subc': subc}
    return render (request,'tmp_admin/list_subcategory.html',context)   

def update_subcategory(request,id):
    subc = get_object_or_404(models.subcategory, id=id)   
    category = models.category.objects.all()
    if request.method == 'POST':
        form = forms.subc_form(request.POST, request.FILES, instance=subc)
        if form.is_valid():
            form.save()
            return redirect(list_subcategory)
        else:
            form.errors
    context = {'subc': subc, 'category': category }
    return render(request,'tmp_admin/update_subcategory.html',context)         
        
        
def delete_subcategory(request, id):
    try:
        subc = models.subcategory.objects.get(id=id)
        subc.delete()
        messages.success(request, "Subcategory deleted successfully.")
    except models.subcategory.DoesNotExist:
        messages.warning(request, "Subcategory not found or already deleted.")
    return redirect(list_subcategory)    

# __________________________________________________________________________________________________________________________________________________

# def create_toy(request):
#     category = models.category.objects.all()
#     subcategory = models.subcategory.objects.all()
#     if request.method == 'POST':
#         form = forms.toy_form(request.POST,request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect(list_toy)
#         else:
#             print(form.errors)
#     context = {'category':category ,'subcategory':subcategory}  
            
#     return render(request,'tmp_admin/create_toy.html',context)

def list_toy(request):
    toy = models.toy.objects.all()
    context = {'toy': toy}
    return render (request,'tmp_admin/list_toy.html',context)  

def update_toy(request,id):
    toy = get_object_or_404(models.toy, id=id)   
    category = models.category.objects.all()
    subcategory = models.subcategory.objects.all()
    if request.method == 'POST':
        form = forms.toy_form(request.POST, request.FILES, instance=toy)
        if form.is_valid():
            form.save()
            return redirect(list_toy)
        else:
            print(form.errors)
    context = {'toy': toy, 'category': category, 'subcategory': subcategory}
    return render(request,'tmp_admin/update_toy.html',context)         
        
        
def delete_toy(request, id):
    try:
        toy = models.toy.objects.get(id=id)
        toy.delete()
        messages.success(request, "Toy deleted successfully.")
    except models.toy.DoesNotExist:
        messages.warning(request, "Toy not found or already deleted.")
    return redirect(list_toy)    



# ____________________________________________________________________________________________________________________________________________

# def create_toyimage(request):
#     if request.method == 'POST':
#         form = forms.toyi_form(request.POST,request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect(list_toyimage)
#         else:
#             print(form.errors)
#     toys = models.toy.objects.all()
#     context = {'toy': toys}
#     return render(request,'tmp_admin/create_toyimage.html', context) 

# def list_toyimage(request):
#     toyimage = models.toyimage.objects.all()
#     context = {'toyimage': toyimage}
#     return render (request,'tmp_admin/list_toyimage.html',context)  

# # def update_toyimage(request,id):
# #     toyimage = models.toyimage.objects.get(id=id)   
# #     if request.method == 'POST':
# #         form = forms.toyi_form(request.POST, request.FILES, instance=toyimage)
# #         if form.is_valid():
# #             form.save()
# #             return redirect(list_toyimage)
# #         else:
# #             form.errors
# #     context = {'toyimage': toyimage }
# #     return render(request,'tmp_admin/update_toyimage.html',context)         
        
        
# def delete_toyimage(request, id):
#     toyimage = models.toyimage.objects.get(id=id)
#     toyimage.delete()
#     return redirect(list_toyimage)    

# _________________________________________________________________________________________________________________________________________________________________

def create_damagereport(request):
    toys = models.toy.objects.all()
    if request.method == 'POST':
        form = forms.dama_form(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect(list_damagereports)
        else:
            print(form.errors)
    context = {'toys': toys}        
    return render(request,'tmp_admin/create_damagereport.html',context) 

def list_damagereports(request):
    damagereport = models.damagereport.objects.all()
    context = {'damagereports': damagereport}
    return render (request,'tmp_admin/list_damagereport.html',context)

def update_damagereport(request,id):
    damagereport = get_object_or_404(models.damagereport, id=id)   
    toys = models.toy.objects.all()
    if request.method == 'POST':
        form = forms.dama_form(request.POST, request.FILES, instance=damagereport)
        if form.is_valid():
            form.save()
            return redirect(list_damagereports)
        else:
            form.errors
    context = {'damagereport': damagereport, 'toys': toys }
    return render(request,'tmp_admin/update_damagereport.html',context)         
        
        
def delete_damagereport(request, id):
    try:
        damagereport = models.damagereport.objects.get(id=id)
        damagereport.delete()
        messages.success(request, "Damage report deleted successfully.")
    except models.damagereport.DoesNotExist:
        messages.warning(request, "Damage report not found or already deleted.")
    return redirect(list_damagereports)    


# __________________________________________________________________________________________________________________________________________________


def create_banner(request):
    if request.method == 'POST':
        form = forms.bann_form(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect(list_banner)
        else:
            print(form.errors)
    return render(request,'tmp_admin/create_banner.html') 

def list_banner(request):
    bann = models.banner.objects.all()
    context = {'bann': bann}
    return render (request,'tmp_admin/list_banner.html',context) 

def update_banner(request,id):
    bann = get_object_or_404(models.banner, id=id)   
    if request.method == 'POST':
        form = forms.bann_form(request.POST, request.FILES, instance=bann)
        if form.is_valid():
            form.save()
            return redirect(list_banner)
        else:
            form.errors
    context = {'bann': bann }
    return render(request,'tmp_admin/update_banner.html',context)         
        
        
def delete_banner(request, id):
    try:
        bann = models.banner.objects.get(id=id)
        bann.delete()
        messages.success(request, "Banner deleted successfully.")
    except models.banner.DoesNotExist:
        messages.warning(request, "Banner not found or already deleted.")
    return redirect(list_banner)    


# ______________________________________________________________________________________________________________________________________________

def create_contactmessage(request):
    if request.method == 'POST':
        form = forms.cont_form(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect(list_contactmessage)
        else:
            print(form.errors)
    return render(request,'tmp_admin/create_contactmessage.html') 

def list_contactmessage(request):
    cont = models.contactmessage.objects.all()
    context = {'cont': cont}
    return render (request,'tmp_admin/list_contactmessage.html',context) 

def update_contactmessage(request,id):
    cont = get_object_or_404(models.contactmessage, id=id)   
    if request.method == 'POST':
        form = forms.cont_form(request.POST, request.FILES, instance=cont)
        if form.is_valid():
            form.save()
            return redirect(list_contactmessage)
        else:
            form.errors
    context = {'cont': cont }
    return render(request,'tmp_admin/update_contactmessage.html',context)         
        
        
def delete_contactmessage(request, id):
    try:
        cont = models.contactmessage.objects.get(id=id)
        cont.delete()
        messages.success(request, "Contact message deleted successfully.")
    except models.contactmessage.DoesNotExist:
        messages.warning(request, "Contact message not found or already deleted.")
    return redirect(list_contactmessage)    


# _______________________________________________________________________________________________________________________________________________________________-

def create_coupon(request):
    if request.method == 'POST':
        form = forms.cou_form(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect(list_coupon)
        else:
            print(form.errors)
    return render(request,'tmp_admin/create_coupon.html') 

def list_coupon(request):
    cou = models.coupon.objects.all()
    context = {'cou': cou}
    return render (request,'tmp_admin/list_coupon.html',context) 

def update_coupon(request,id):
    cou = get_object_or_404(models.coupon, id=id)   
    if request.method == 'POST':
        form = forms.cou_form(request.POST, request.FILES, instance=cou)
        if form.is_valid():
            form.save()
            return redirect(list_coupon)
        else:
            form.errors
    context = {'cou': cou }
    return render(request,'tmp_admin/update_coupon.html',context)         
        
        
def delete_coupon(request, id):
    try:
        cou = models.coupon.objects.get(id=id)
        cou.delete()
        messages.success(request, "Coupon deleted successfully.")
    except models.coupon.DoesNotExist:
        messages.warning(request, "Coupon not found or already deleted.")
    return redirect(list_coupon)    

# _________________________________________________________________________________________________________________________________________________________-

def create_siteSettings(request):
    if request.method == 'POST':
        form = forms.sit_form(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect(list_siteSettings)
        else:
            print(form.errors)
    return render(request,'tmp_admin/create_siteSettings.html') 

def list_siteSettings(request):
    sit = models.siteSettings.objects.all()
    context = {'sit': sit}
    return render (request,'tmp_admin/list_siteSettings.html',context) 

def update_siteSettings(request,id):
    sit = get_object_or_404(models.siteSettings, id=id)   
    if request.method == 'POST':
        form = forms.sit_form(request.POST, request.FILES, instance=sit)
        if form.is_valid():
            form.save()
            return redirect(list_siteSettings)
        else:
            form.errors
    context = {'sit': sit }
    return render(request,'tmp_admin/update_siteSettings.html',context)         
        
        
def delete_siteSettings(request, id):
    try:
        sit = models.siteSettings.objects.get(id=id)
        sit.delete()
        messages.success(request, "Site settings deleted successfully.")
    except models.siteSettings.DoesNotExist:
        messages.warning(request, "Site settings not found or already deleted.")
    return redirect(list_siteSettings)    


@login_required(login_url="/login")
def rental_tracking_list_view(request):
    if request.user.role.upper() != 'ADMIN':
        return redirect('login')
    
    rentals = models.RentalRequest.objects.all().order_by('-created_at')
    
    # Calculate Dynamic Stats
    shipped_count = rentals.filter(status__in=['SHIPPED', 'DELIVERING']).count()
    extension_count = rentals.filter(is_extension=True).count()
    
    context = {
        'rentals': rentals,
        'shipped_count': shipped_count,
        'extension_count': extension_count
    }
    return render(request, 'tmp_admin/rental_tracking.html', context)

@login_required(login_url="/login")
def update_rental_status_view(request, rental_id):
    if request.user.role.upper() != 'ADMIN':
        return redirect('login')
    
    if request.method == 'POST':
        rental = get_object_or_404(models.RentalRequest, id=rental_id)
        new_status = request.POST.get('status')
        if new_status in models.RentalRequest.Status.values:
            rental.status = new_status
            rental.save()
            messages.success(request, f"Status updated for order #{rental.id}.")
        
    return redirect('rental_tracking_list_view')





