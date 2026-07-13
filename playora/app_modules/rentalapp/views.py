# from django.shortcuts import render,redirect
from urllib import request

from app_modules.rentalapp import forms
# from app_modules.rentalapp import models
# from django.http import HttpResponse


# from django.contrib.auth.models import User
# from django.contrib.auth import login,logout,authenticate

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from app_modules.rentalapp import models
from app_modules.adminapp.models import banner, category, coupon, damagereport, siteSettings, subcategory, toy, contactmessage, RentalRequest
from django.contrib.auth.decorators import login_required








User = get_user_model()

# Create your views here.
# def rentalindex_view(request):
#     return render(request,'tmp_rental/rentalindex.html')

@login_required
def rentalindex_view(request):
    if request.user.role.upper() != 'RENTAL':
        return redirect('login')

    return render(request, 'tmp_rental/rentalindex.html')


# def derenatalregister_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         password1 = request.POST.get('password1')
#         role = request.POST.get('role')

#         if password != password1:
#             messages.error(request, "Passwords do not match!")
#             return redirect('register')

#         if User.objects.filter(username=username).exists():
#             messages.warning(request, "Username already exists! Try another.")
#             return redirect('register')

#         user = User.objects.create_user(username=username, password=password, role=role)

#         if role == "Admin":
#             user.is_approved = True
#         else:
#             user.is_approved = False

#         user.save()
#         messages.success(request, "Registration successful! Wait for admin approval before login.")
#         return redirect('login')
#     return render(request, 'tmp_rental/derentalregister.html')



# def logout_view(request):
#     logout(request)
#     messages.info(request, "You have been logged out successfully.")
#     return redirect('login')


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# def rentallogin_view(request):
#     if request.method =='POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         confirmpaasword = request.POST.get('confirmpaasword')
#         # captcha = request.POST.get('captcha')
        
#         user = authenticate(username= username,password=password,confirmpaasword=confirmpaasword )
#         if user is not None:
#             login(request,user)
#             return redirect(rentalindex_view)
#         else:
#             return HttpResponse("user does not exits")
#     return render(request,'tmp_rental/rentallogin.html') 


# def rentalregister_view(request):
#     if request.method =='POST':
#         username = request.POST.get('username')
#         # emailaddress = request.POST.get('emailaddress')
#         # mobilenumber = request.POST.get('mobilenumber')
#         # city = request.POST.get('city')
#         password = request.POST.get('password')
#         confirmpaasword = request.POST.get('confirmpaasword')
        
#         # captcha = request.POST.get('captcha')
#         if password==confirmpaasword:
#             try:
#                 User.objects.get(username==username)
#                 return HttpResponse("username alredy exits please Try Again")
#             except:
#                 User.objects.create_user(username=username,password=confirmpaasword)
#                 return redirect(login_view)
#         else:
#             return HttpResponse("password do not match!!!")
#     return render(request,'tmp_rental/rentalregister.html') 

# def logout_view(request):
#     logout(request)
#     return redirect(login_view)







# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++





# my rental model 

def create_category_rental(request):
    if request.method == 'POST':
        form = forms.cate_form(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect(list_category_rental)
        else:
            print(form.errors)
    return render(request,'tmp_rental/create_category_rental.html')  

def list_category_rental(request):
    cate =  category.objects.all()
    context = {'cate': cate }
    return render (request,'tmp_rental/list_category_rental.html',context)  

def update_category_rental(request, pk):
    cate = get_object_or_404(category, id=pk)
    if request.method == 'POST':
        form = forms.cate_form(request.POST,request.FILES, instance=cate)
        if form.is_valid():
            form.save()
            return redirect(list_category_rental)
        else:
            print(form.errors)
    context = {'cate': cate}
    return render(request,'tmp_rental/update_category_rental.html', context)

def delete_category_rental(request, pk):
    cate = get_object_or_404(category, id=pk)
    cate.delete()
    return redirect(list_category_rental)

# ____________________________________________________________________________________________________________________________________________________________________________________________________________________________

def create_subcategory_rental(request):
    category_list = category.objects.all()
    if request.method == 'POST':
        form = forms.subc_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_subcategory_rental)
        else:
            print(form.errors)
    context = {'category':category_list}           
    return render(request,'tmp_rental/create_subcategory_rental.html', context) 


def list_subcategory_rental(request):
    subc = subcategory.objects.all()
    context = {'subc': subc}
    return render (request,'tmp_rental/list_subcategory_rental.html',context) 

def update_subcategory_rental(request, pk):
    subc = get_object_or_404(subcategory, id=pk)
    if request.method == 'POST':
        form = forms.subc_form(request.POST, instance=subc)
        if form.is_valid():
            form.save()
            return redirect(list_subcategory_rental)
        else:
            print(form.errors)
    context = {'subc': subc}
    return render(request,'tmp_rental/update_subcategory_rental.html', context) 

def delete_subcategory_rental(request, pk):
    subc = get_object_or_404(subcategory, id=pk)
    subc.delete()
    return redirect(list_subcategory_rental)

# ___________________________________________________________________________________________________________________________________________________________________________________________________________________________

def create_toy_rental(request):
    category_list = category.objects.all()
    subcategory_list = subcategory.objects.all()
    if request.method == 'POST':
        form = forms.toy_form(request.POST,request.FILES)
        if form.is_valid():
            toy_obj = form.save(commit=False)
            toy_obj.added_by = request.user
            toy_obj.save()
            return redirect(list_toy_rental)
        else:
            print(form.errors)
    context = {'category':category_list ,'subcategory':subcategory_list}  
            
    return render(request,'tmp_rental/create_toy_rental.html',context)

def list_toy_rental(request):
    toys = toy.objects.filter(added_by=request.user)
    context = {'toy': toys }
    return render (request,'tmp_rental/list_toy_rental.html',context)  

def update_toy_rental(request, pk):
    toy_instance = get_object_or_404(toy, id=pk)
    category_list = category.objects.all()
    subcategory_list = subcategory.objects.all()
    if request.method == 'POST':
        form = forms.toy_form(request.POST,request.FILES, instance=toy_instance)
        if form.is_valid():
            form.save()
            return redirect(list_toy_rental)
        else:
            print(form.errors)
    context = {'toy': toy_instance, 'category': category_list, 'subcategory': subcategory_list}
    return render(request,'tmp_rental/update_toy_rental.html', context)

def delete_toy_rental(request, pk):
    toy_instance = get_object_or_404(toy, id=pk)
    toy_instance.delete()
    return redirect(list_toy_rental)

# ___________________________________________________________________________________________________________________________________________________________________________________________________________________________


# def create_toyimage_rental(request):
#     if request.method == 'POST':
#         form = forms.toyi_form(request.POST,request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect(list_toyimage_rental)
#         else:
#             print(form.errors)
#     toys = toy.objects.all()
#     context = {'toy': toys}
#     return render(request,'tmp_rental/create_toyimage_rental.html', context) 

# def list_toyimage_rental(request):
#     toy = toyimage.objects.all()
#     context = {'toy': toy}
#     return render (request,'tmp_rental/list_toyimage_rental.html',context)  


# ___________________________________________________________________________________________________________________________________________________________________________________________________________________________

def create_damagereport_rental(request):
    toys = toy.objects.all()
    if request.method == 'POST':
        form = forms.dama_form(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect(list_damagereport_rental)
        else:
            print(form.errors)
    
    context = {'toy': toys}
    return render(request,'tmp_rental/create_damagereport_rental.html', context)

def list_damagereport_rental(request):
    dama = damagereport.objects.all()
    context = {'dama': dama }
    return render (request,'tmp_rental/list_damagereport_rental.html',context)

def update_damagereport_rental(request, id):
    dama = get_object_or_404(damagereport, id=id)
    toys = toy.objects.all()
    if request.method == 'POST':
        form = forms.dama_form(request.POST,request.FILES, instance=dama)
        if form.is_valid():
            form.save()
            return redirect(list_damagereport_rental)
        else:
            print(form.errors)
    context = {'dama': dama, 'toy': toys}
    return render(request,'tmp_rental/update_damagereport_rental.html', context)

def delete_damagereport_rental(request, id):
    dama = get_object_or_404(damagereport, id=id)
    dama.delete()
    return redirect(list_damagereport_rental)
# ____________________________________________________________________________________________________________________________________________________________________________________________________________________________

def create_banner_rental(request):
    if request.method == 'POST':
        form = forms.bann_form(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect(list_banner_rental)
        else:
            print(form.errors)
    return render(request,'tmp_rental/create_banner_rental.html')

def list_banner_rental(request):
    bann = banner.objects.all()
    context = {'bann': bann}
    return render (request,'tmp_rental/list_banner_rental.html',context)

def update_banner_rental(request, id):
    bann = get_object_or_404(banner, id=id)
    if request.method == 'POST':
        form = forms.bann_form(request.POST,request.FILES, instance=bann)
        if form.is_valid():
            form.save()
            return redirect(list_banner_rental)
        else:
            print(form.errors) 
        context = {'bann': bann}
    return render(request,'tmp_rental/update_banner_rental.html', context)       

def delete_banner_rental(request, id):
    bann = get_object_or_404(banner, id=id)
    bann.delete()
    return redirect(list_banner_rental)        

       
# ___________________________________________________________________________________________________________________________________________________________________________________________________________________________


def create_contactmessage_rental(request):
    if request.method == 'POST':
        form = forms.cont_form(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect(list_contactmessage_rental)
        else:
            print(form.errors)
    return render(request,'tmp_rental/create_contactmessage_rental.html') 


def list_contactmessage_rental(request):
    cont = contactmessage.objects.all()
    context = {'cont': cont}
    return render (request,'tmp_rental/list_contactmessage_rental.html',context)

def update_contactmessage_rental(request,id):
    cont = get_object_or_404(contactmessage, id=id)
    if request.method  == 'POST':
        form = forms.cont_form(request.POST, request.FILES, instance=cont)
        if form.is_valid():
            form.save()
            return redirect(list_contactmessage_rental)
        else:
            form.errors
    context = {'cont': cont}
    return render(request,'tmp_rental/update_contactmessage_rental.html',context)

def delete_contactmessage_rental(request,id):
    cont = get_object_or_404(contactmessage, id=id)
    cont.delete()
    return redirect(list_contactmessage_rental)
# ___________________________________________________________________________________________________________________________________________________________________________________________________________________________

def create_coupon_rental(request):
    if request.method == 'POST':
        form = forms.cou_form(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect(list_coupon_rental)
        else:
            print(form.errors)
    return render(request,'tmp_rental/create_coupon_rental.html') 

def list_coupon_rental(request):
    cou = coupon.objects.all()
    context = {'cou': cou}
    return render (request,'tmp_rental/list_coupon_rental.html',context)
 
def update_coupon_rental(request,id):
    cou = get_object_or_404(coupon, id=id)
    if request.method == 'POST':
        form = forms.cou_form(request.POST, request.FILES, instance=cou)
        if form.is_valid():
            form.save()
            return redirect(list_coupon_rental)
        else:
            form.errors
    context = {'cou': cou}
    return render(request,'tmp_rental/update_coupon_rental.html',context)

def delete_coupon_rental(request,id):
    cou = get_object_or_404(coupon, id=id)
    cou.delete()
    return redirect(list_coupon_rental)

# _____________________________________________________________________________________________________________________________________________________________________________________________________________________________

def create_siteSettings_rental(request):
    if request.method == 'POST':
        form = forms.sit_form(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect(list_siteSettings_rental)
        else:
            print(form.errors)
    return render(request,'tmp_rental/create_siteSettings_rental.html') 

def list_siteSettings_rental(request):
    sit = siteSettings.objects.all()
    context = {'sit': sit}
    return render (request,'tmp_rental/list_siteSettings_rental.html',context)

def update_siteSettings_rental(request,id):
    sit = get_object_or_404(siteSettings, id=id)
    if request.method == 'POST':
        form = forms.sit_form(request.POST, request.FILES, instance=sit)
        if form.is_valid():
            form.save()
            return redirect(list_siteSettings_rental)
        else:
            form.errors
    context = {'sit': sit}
    return render(request,'tmp_rental/update_siteSettings_rental.html',context)     

def delete_siteSettings_rental(request,id):
    sit = get_object_or_404(siteSettings, id=id)
    sit.delete()
    return redirect(list_siteSettings_rental)






# ____________________________________________________________________________________________________________________________________________________________________________________________________________________________
def create_cart(request):
    if request.method == 'POST':
        form = forms.cart_form(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect(list_cart)
        else:
            print(form.errors)
    return render(request,'tmp_rental/create_cart.html')

def list_cart(request):
    cart =  models.cart.objects.all()
    context = {'cart': cart }
    return render (request,'tmp_rental/list_cart.html',context)

def update_cart(request, id):
    cart = get_object_or_404(models.cart, id=id)
    if request.method == 'POST':
        form = forms.cart_form(request.POST,request.FILES, instance=cart)
        if form.is_valid():
            form.save()
            return redirect(list_cart)
        else:
            print(form.errors)
    context = {'cart': cart}
    return render(request,'tmp_rental/update_cart.html', context)

def delete_cart(request, id):
    cart = get_object_or_404(models.cart, id=id)
    cart.delete()
    return redirect(list_cart)

# ___________________________________________________________________________________________________________________________________________________________________________________________________________________________
def create_rental(request):
    if request.method == 'POST':
        form = forms.ren_form(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect(list_rental)
        else:
            print(form.errors)
    return render(request,'tmp_rental/create_rental.html')

def list_rental(request):
    ren =  models.rental.objects.all()
    context = {'ren':ren }
    return render (request,'tmp_rental/list_rental.html',context)

def update_rental(request, id):
    ren = get_object_or_404(models.rental, id=id)
    if request.method == 'POST':
        form = forms.ren_form(request.POST,request.FILES, instance=ren)
        if form.is_valid():
            form.save()
            return redirect(list_rental)
        else:
            print(form.errors)
    context = {'ren': ren}
    return render(request,'tmp_rental/update_rental.html', context)

def delete_rental(request, id):
    ren = get_object_or_404(models.rental, id=id)
    ren.delete()
    return redirect(list_rental)
# ____________________________________________________________________________________________________________________________________________________________________________________________________________________________

def create_rentalitem(request):
    ren = models.rental.objects.all()
    if request.method == 'POST':
        form = forms.reni_form(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect(list_rentalitem)
        else:
            print(form.errors)
    context = {'ren': ren}
    return render(request,'tmp_rental/create_rentalitem.html',context)

def list_rentalitem(request):
    reni =  models.rentalitem.objects.all()
    context = {'reni':reni }
    return render (request,'tmp_rental/list_rentalitem.html',context)

def update_rentalitem(request, id):
    ren = models.rental.objects.all()
    reni = get_object_or_404(models.rentalitem, id=id)
    if request.method == 'POST':
        form = forms.reni_form(request.POST,request.FILES, instance=reni)
        if form.is_valid():
            form.save()
            return redirect(list_rentalitem)
        else:
            print(form.errors)
    context = {'reni': reni, 'ren': ren}
    return render(request,'tmp_rental/update_rentalitem.html', context)

def delete_rentalitem(request, id):
    reni = get_object_or_404(models.rentalitem, id=id)
    reni.delete()
    return redirect(list_rentalitem)

# ___________________________________________________________________________________________________________________________________________________________________________________________________________________________
def create_payment(request):
    
    if request.method == 'POST':
        form = forms.pay_form(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect(rentalindex_view)
        else:
            print(form.errors)
    return render(request,'tmp_rental/create_payment.html')

def list_payment(request):
    pay =  models.payment.objects.all()
    context = {'pay':pay }
    return render (request,'tmp_rental/list_payment.html',context)

def update_payment(request, id):
    pay = get_object_or_404(models.payment, id=id)
    if request.method == 'POST':
        form = forms.pay_form(request.POST,request.FILES, instance=pay)
        if form.is_valid():
            form.save()
            return redirect(list_payment)
        else:
            print(form.errors)
    context = {'pay': pay}
    return render(request,'tmp_rental/update_payment.html', context)

def delete_payment(request, id):
    pay = get_object_or_404(models.payment, id=id)
    pay.delete()
    return redirect(list_payment)

# ___________________________________________________________________________________________________________________________________________________________________________________________________________________________

def create_ReturnRequest(request):
    if request.method == 'POST':
        form = forms.Ret_form(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect(rentalindex_view)
        else:
            print(form.errors)
    return render(request,'tmp_rental/create_ReturnRequest.html')


def create_Refund(request):
    if request.method == 'POST':
        form = forms.Ref_form(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect(rentalindex_view)
        else:
            print(form.errors)
    return render(request,'tmp_rental/create_Refund.html')


def create_LateFee(request):
    if request.method == 'POST':
        form = forms.lat_form(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect(rentalindex_view)
        else:
            print(form.errors)
    return render(request,'tmp_rental/create_LateFee.html')


@login_required
def rental_requests_list(request):
    if request.user.role.upper() != 'RENTAL':
        return redirect('login')
    
    from django.db.models import Sum
    all_requests = RentalRequest.objects.filter(rental_provider=request.user).order_by('-created_at')
    pending_requests = all_requests.filter(status='PENDING')
    total_revenue = all_requests.filter(status__in=['ACCEPTED', 'PAID']).aggregate(Sum('total_price'))['total_price__sum'] or 0
    
    context = {
        'requests': all_requests,
        'total_requests': all_requests.count(),
        'paid_count': all_requests.filter(status='PAID').count(),
        'pending_count': pending_requests.count(),
        'total_revenue': total_revenue,
    }
    return render(request, 'tmp_rental/rental_requests.html', context)





@login_required
def approve_rental_request(request, pk):
    if request.user.role.upper() != 'RENTAL':
        return redirect('login')
    
    rental_req = get_object_or_404(RentalRequest, id=pk, rental_provider=request.user)
    rental_req.status = 'ACCEPTED'
    rental_req.save()
    messages.success(request, f"Request for {rental_req.toy.name} accepted.")
    return redirect('rental_requests_list')

@login_required
def reject_rental_request(request, pk):
    if request.user.role.upper() != 'RENTAL':
        return redirect('login')
    
    rental_req = get_object_or_404(RentalRequest, id=pk, rental_provider=request.user)
    rental_req.status = 'REJECTED'
    rental_req.save()
    messages.warning(request, f"Request for {rental_req.toy.name} rejected.")
    return redirect('rental_requests_list')

@login_required
def rental_profile_view(request):
    if request.user.role.upper() != 'RENTAL':
        return redirect('login')
    
    user = request.user
    if request.method == 'POST':
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        user.phone = request.POST.get('phone', user.phone)
        user.gender = request.POST.get('gender', user.gender)
        user.address = request.POST.get('address', user.address)
        user.city = request.POST.get('city', user.city)
        user.state = request.POST.get('state', user.state)
        user.pincode = request.POST.get('pincode', user.pincode)
        user.alternate_phone = request.POST.get('alternate_phone', user.alternate_phone)
        user.emergency_contact = request.POST.get('emergency_contact', user.emergency_contact)
        
        if 'profile_image' in request.FILES:
            user.profile_image = request.FILES['profile_image']
            
        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('rental_profile_view')
        
    from app_modules.adminapp.models import toy, RentalRequest
    toy_count = toy.objects.filter(added_by=user).count()
    request_count = RentalRequest.objects.filter(rental_provider=user).count()
    
    return render(request, 'tmp_rental/rental_profile.html', {
        'user': user,
        'toy_count': toy_count,
        'request_count': request_count
    })

@login_required
def update_rental_status(request):
    if request.method == 'POST':
        rental_id = request.POST.get('rental_id')
        new_status = request.POST.get('status')
        
        try:
            # Allow both RENTAL provider and ADMIN to update status
            if request.user.role.upper() == 'RENTAL':
                rental_req = get_object_or_404(RentalRequest, id=rental_id, rental_provider=request.user)
            elif request.user.is_superuser or request.user.role.upper() == 'ADMIN':
                rental_req = get_object_or_404(RentalRequest, id=rental_id)
            else:
                return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)

            rental_req.status = new_status
            rental_req.save()
            return JsonResponse({'status': 'success', 'message': f'Status updated to {new_status}'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
