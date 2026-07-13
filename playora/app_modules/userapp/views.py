
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from app_modules.userapp import models
from django.contrib.auth.decorators import login_required
from app_modules.userapp import forms

# from store.models import Product
from cart.cart import Cart


from django.db.models import Q
from app_modules.adminapp import models


User = get_user_model()
# Create your views here.

# def index_view(request):
#     cat = models.category.objects.all()
#     context = {'cat':cat}
#     return render(request,'tmp_user/index.html',context)

def index_view(request):
    categories = models.category.objects.all()[:4]
    
    # "All" or "Featured" section
    featured_toys = models.toy.objects.filter(is_featured=True).order_by('?')[:8]
    if not featured_toys.exists():
        featured_toys = models.toy.objects.filter(is_available=True).order_by('?')[:8]
        
    # New Arrivals
    new_arrivals = models.toy.objects.filter(is_available=True).order_by('-created_at')[:8]
    
    # Popular Toys
    popular_toys = models.toy.objects.filter(is_popular=True, is_available=True).order_by('?')[:8]
    if not popular_toys.exists():
        popular_toys = models.toy.objects.filter(is_available=True).order_by('?')[:8]
        
    # On Sale Toys
    on_sale_toys = models.toy.objects.filter(is_on_sale=True, is_available=True).order_by('?')[:8]
    if not on_sale_toys.exists():
        on_sale_toys = models.toy.objects.filter(is_available=True).order_by('?')[:8]

    context = {
        'cat': categories,
        'toy': featured_toys, # Used for "All" tab
        'new_arrivals': new_arrivals,
        'popular_toys': popular_toys,
        'on_sale_toys': on_sale_toys,
        'featured_toys': featured_toys # Just in case it's used elsewhere
    }
    return render(request, 'tmp_user/index.html', context)


# pages


def about_view(request):  
    return render(request,'tmp_user/about.html')

def shop_view(request):
    cat_id = request.GET.get('cat')
    brand = request.GET.get('brand')
    age = request.GET.get('age')
    q = request.GET.get('q')
    
    toy_list = models.toy.objects.all()

    if q:
        toy_list = toy_list.filter(
            Q(name__icontains=q) | 
            Q(category__name__icontains=q) | 
            Q(brand__icontains=q)
        )
    
    if cat_id:
        toy_list = toy_list.filter(category_id=cat_id)
        current_cat = get_object_or_404(models.category, id=cat_id)
    else:
        current_cat = None
        
    if brand:
        toy_list = toy_list.filter(brand=brand)
        
    if age:
        toy_list = toy_list.filter(age_group=age)
    
    cat = models.category.objects.all()
    brands = models.toy.objects.values_list('brand', flat=True).distinct()
    age_groups = models.toy.objects.values_list('age_group', flat=True).distinct()
    
    context = {
        'cat': cat, 
        'toy': toy_list,
        'current_cat': current_cat,
        'brands': brands,
        'age_groups': age_groups,
        'selected_brand': brand,
        'selected_age': age,
    }
    return render(request,'tmp_user/shop.html', context)

# def blog_view(request):
#     return render(request,'tmp_user/blog.html')

def cart_view(request):
    cart = Cart(request)
    return render(request, 'tmp_user/cart.html', {'cart': cart.cart})

@login_required(login_url="/login")
def checkout_view(request):
    cart = Cart(request)
    
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        delivery_date = request.POST.get('delivery_date')
        
        from datetime import datetime, timedelta
        
        for key, value in cart.cart.items():
            toy_obj = get_object_or_404(models.toy, id=int(value['product_id']))
            rental_provider = toy_obj.added_by
            
            # Calculate rental end date (initial 1 week)
            d_date = datetime.strptime(delivery_date, '%Y-%m-%d').date()
            end_date = d_date + timedelta(weeks=1)
            
            models.RentalRequest.objects.create(
                user=request.user,
                toy=toy_obj,
                rental_provider=rental_provider,
                quantity=int(value['quantity']),
                total_price=float(value['price']) * int(value['quantity']),
                security_deposit=float(toy_obj.security_deposit) * int(value['quantity']),
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                address=address,
                city=city,
                pincode=pincode,
                delivery_date=delivery_date,
                rental_end_date=end_date,
                rental_duration_weeks=1
            )
        
        cart.clear()
        messages.success(request, "Your rental request has been sent to the provider(s). Please wait for approval.")
        return redirect('ordersuccess_view')

    total_bill = 0
    security_deposit = 0
    for key, value in cart.cart.items():
        total_bill += float(value['price']) * int(value['quantity'])
        toy_obj = get_object_or_404(models.toy, id=int(value['product_id']))
        security_deposit += float(toy_obj.security_deposit) * int(value['quantity'])
        
    total_payable = total_bill + security_deposit
    
    context = {
        'cart': cart.cart,
        'security_deposit': security_deposit,
        'total_payable': total_payable,
    }
    
    return render(request, 'tmp_user/checkout.html', context)

def contact_view(request):
    return render(request,'tmp_user/contact.html')

def faq_view(request):
    return render(request,'tmp_user/faq.html')



def ordersuccess_view(request):
    recent_requests = models.RentalRequest.objects.filter(user=request.user).order_by('-created_at')[:5]
    total_payable = sum(r.total_price + r.security_deposit for r in recent_requests)
    return render(request, 'tmp_user/ordersuccess.html', {'requests': recent_requests, 'total_payable': total_payable})


def profile_view(request):
    return render(request,'tmp_user/profile.html')

@login_required(login_url="/login")
def profile_edit_view(request):
    if request.method == 'POST':
        form = forms.UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile_view')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = forms.UserProfileForm(instance=request.user)
    
    return render(request, 'tmp_user/profile_edit.html', {'form': form})

# def register_view(request):
#     return render(request,'tmp_user/register.html')

def services_view(request):
    return render(request,'tmp_user/services.html')

def toydetail_view(request, id):
    toy_detail = get_object_or_404(models.toy, id=id)
    # Get toys from same category
    related_toys = list(models.toy.objects.filter(category=toy_detail.category).exclude(id=id)[:4])
    
    # If less than 4, fill with random toys
    if len(related_toys) < 4:
        additional_count = 4 - len(related_toys)
        already_included_ids = [toy_detail.id] + [t.id for t in related_toys]
        additional_toys = models.toy.objects.exclude(id__in=already_included_ids).order_by('?')[:additional_count]
        related_toys.extend(list(additional_toys))
        
    context = {
        'toy': toy_detail,
        'related_toys': related_toys
    }
    return render(request, 'tmp_user/toydetail.html', context)

def toy_view(request):
    cat_param = request.GET.get('cat')
    current_cat = None
    if cat_param:
        if cat_param.isdigit():
            current_cat = models.category.objects.filter(id=cat_param).first()
        else:
            current_cat = models.category.objects.filter(name__iexact=cat_param).first()
    
    if current_cat:
        toy = models.toy.objects.filter(category=current_cat)
    else:
        toy = models.toy.objects.all()
    
    categories = models.category.objects.all()
    context = {
        'toy': toy,
        'categories': categories,
        'current_cat': current_cat
    }
    return render(request, 'tmp_user/toy.html', context)

def all_categories_view(request):
    cat = models.category.objects.all()
    context = {'cat': cat}
    return render(request, 'tmp_user/all_categories.html', context)

from wishlist.wishlist import Wishlist

@login_required(login_url="/login")
def wishlist_add(request, id):
    wishlist = Wishlist(request)
    product = get_object_or_404(models.toy, id=id)
    wishlist.add(product=product)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'message': 'Item added to wishlist'})
    return redirect("wishlist_view")

@login_required(login_url="/login")
def wishlist_remove(request, id):
    wishlist = Wishlist(request)
    product = get_object_or_404(models.toy, id=id)
    wishlist.remove(product)
    return redirect("wishlist_view")

@login_required(login_url="/login")
def wishlist_view(request):
    wishlist = Wishlist(request)
    return render(request, 'tmp_user/wishlist.html', {'wishlist': wishlist.wishlist})
# ________________________________________________________________________________________________________________________________________________
# 




def user_register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('user_register')

        if User.objects.filter(username=username).exists():
            messages.warning(request, "Username already exists!")
            return redirect('user_register')

        user = User.objects.create_user(
            username=username, 
            email=email, 
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            address=address,
            date_of_birth=date_of_birth if date_of_birth else None,
            gender=gender,
            city=city,
            pincode=pincode,
        )
        user.role = 'USER'
        user.is_approved = True  
        user.save()

        messages.success(request, "Registration successful! You can now login.")
        return redirect('login')
    return render(request, 'tmp_user/user_register.html')

def rental_register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('rental_register')

        if User.objects.filter(username=username).exists():
            messages.warning(request, "Username already exists!")
            return redirect('rental_register')

        user = User.objects.create_user(
            username=username, 
            email=email, 
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            address=address,
            date_of_birth=date_of_birth if date_of_birth else None,
            gender=gender,
            city=city,
            pincode=pincode,
        )
        user.role = 'RENTAL'
        user.is_approved = False  # Rental needs admin approval
        user.save()

        messages.success(request, "Registration successful! Please wait for admin approval.")
        return redirect('login')
    return render(request, 'tmp_user/rental_register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if not user.is_approved:
                messages.warning(request, "Your account is pending admin approval.")
                return redirect('login')

            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            
            if user.role.upper() == 'ADMIN':
                return redirect('adminindex_view')
            elif user.role.upper() == 'RENTAL':
                return redirect('rentalindex_view')
            else:
                return redirect('index_view')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'tmp_user/login.html')


@login_required
def adminindex_view(request):
    if request.user.role.upper() != 'ADMIN':
        messages.error(request, "You are not authorized to view this page.")
        return redirect('login')

    all_users = User.objects.filter(role='RENTAL')
    approved_rental = User.objects.filter(is_approved=True, role='RENTAL')
    pending_rental = User.objects.filter(is_approved=False, role='RENTAL')

    return render(request, 'tmp_admin/index/adminindex.html', {
         'custo': all_users,
         'approved_rental': approved_rental,
         'rejected_rental': pending_rental,
     })

@login_required
def approve_rental(request, rental_id):    
    if request.user.role.upper() != 'ADMIN':
        messages.error(request, "You are not authorized to perform this action.")
        return redirect('login')
    
    rental_user = get_object_or_404(User, id=rental_id)

    if rental_user.role.upper() == 'ADMIN':
        messages.warning(request, "You cannot approve another Admin account.")
        return redirect('adminindex_view')

    rental_user.is_approved = True
    rental_user.save()
    messages.success(request, f"{rental_user.username} has been approved successfully!")
    return redirect('adminindex_view')

@login_required
def reject_rental(request, rental_id):
    if request.user.role.upper() != 'ADMIN':
        messages.error(request, "You are not authorized to perform this action.")
        return redirect('login')

    rental_user = get_object_or_404(User, id=rental_id)

    if rental_user.role.upper() == 'ADMIN':
        messages.warning(request, "You cannot reject another Admin account.")
        return redirect('adminindex_view')

    # For rejection, we might want to delete or just keep is_approved=False
    # Let's keep it as is_approved=False but maybe rename the variable for clarity in the template if needed.
    rental_user.is_approved = False
    rental_user.save()

    messages.error(request, f"{rental_user.username} has been rejected.")
    return redirect('adminindex_view')

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('login')



# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 


# add to cart views are in cart app

from django.http import JsonResponse

@login_required(login_url="/login")
def cart_add(request, id):
    cart = Cart(request)
    product = get_object_or_404(models.toy, id=id)
    cart.add(product=product)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'message': 'Item added to cart'})
    return redirect("index_view")


@login_required(login_url="/login")
def item_clear(request, id):
    cart = Cart(request)
    product = get_object_or_404(models.toy, id=id)
    cart.remove(product)
    return redirect("cart_view")


@login_required(login_url="/login")
def item_increment(request, id):
    cart = Cart(request)
    product = get_object_or_404(models.toy, id=id)
    cart.add(product=product)
    return redirect("cart_view")


@login_required(login_url="/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = get_object_or_404(models.toy, id=id)
    cart.decrement(product=product)
    return redirect("cart_view")


@login_required(login_url="/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_view")


@login_required(login_url="/login")
def cart_detail(request):
    cart = Cart(request)
    return render(request, 'tmp_user/cart.html', {'cart': cart.cart})


# ________________________________________________________________________________________________________________________________________________________________________________--

# CHANGE KAR VA MATE KARELU KAMMMMMMMMMM


# def demoregister_view(request):
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

#         user.is_approved = True
#         user.save()
#         messages.success(request, "Registration successful! You can now login.")
#         return redirect('login')
#     return render(request, 'tmp_user/demoregister.html')

# ________________________________________________________________________________________________________________________________________________________________________________--
    
# login register roll baseddd

#main code %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


# def demoregister_view(request):
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
#     return render(request, 'tmp_user/demoregister.html')


# _______________________________________________________________________________________________________________________________________________________________________________--


# def demologin_view(request): 
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             # if user.role == 'Admin' or user.is_approved:
#                 login(request, user)
#                 messages.success(request, f"Welcome back, {user.username}!")
#                 if user.role == 'Admin':
#                     return redirect('adminindex_view')
#                 elif user.role == 'rental':
#                     return redirect('rentalindex_view')
#                 else:
#                     return redirect('index_view')
#         else:
#             messages.error(request, "Invalid username or password.")
#     return render(request, 'tmp_user/demologin.html')

# def logout_view(request):
#     logout(request)
#     messages.info(request, "You have been logged out successfully.")
#     return redirect('login')


# @login_required
# def adminindex_view(request):
#     if request.user.role != 'Admin':
#         messages.error(request, "You are not authorized to view this page.")
#         return redirect('login')

#     all_users = models.CustomUser.objects.exclude(role='Admin')
#     approved_users = models.CustomUser.objects.filter(is_approved=True, role__in=['rental', 'User'])
#     rejected_users = models.CustomUser.objects.filter(is_approved=False, role__in=['rental', 'User'])

#     return render(request, 'dashboard_admin.html', {
#         'all_users': all_users,
#         'approved_users': approved_users,
#         'rejected_users': rejected_users,
#     })




# _________________________________________________________________________________________________________________________________________________________________________________--

# main code %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# def demologin_view(request): 
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             if user.role == 'Admin' or user.is_approved:
#                 login(request, user)
#                 messages.success(request, f"Welcome back, {user.username}!")
#                 if user.role == 'Admin':
#                     return redirect('adminindex_view')
#                 elif user.role == 'rental':
#                     return redirect('rentalindex_view')
#                 else:
#                     return redirect('index_view')
#             else:
#                 messages.warning(request, "Your account is not yet approved by admin.")
#         else:
#             messages.error(request, "Invalid username or password.")
#     return render(request, 'tmp_user/demologin.html')

# def logout_view(request):
#     logout(request)
#     messages.info(request, "You have been logged out successfully.")
#     return redirect('login')


# @login_required
# def adminindex_view(request):
#     if request.user.role != 'Admin':
#         messages.error(request, "You are not authorized to view this page.")
#         return redirect('login')

#     all_users = models.CustomUser.objects.exclude(role='Admin')
#     approved_users = models.CustomUser.objects.filter(is_approved=True, role__in=['rental', 'User'])
#     rejected_users = models.CustomUser.objects.filter(is_approved=False, role__in=['rental', 'User'])

#     return render(request, 'dashboard_admin.html', {
#         'all_users': all_users,
#         'approved_users': approved_users,
#         'rejected_users': rejected_users,
#     })



  
# @login_required
# def approve_user(request, user_id):    
#     if request.user.role != 'Admin':
#         messages.error(request, "You are not authorized to perform this action.")
#         return redirect('login')
#     user = get_object_or_404(User, id=user_id)

#     if user.role == 'Admin':
#         messages.warning(request, "You cannot approve another Admin account.")
#         return redirect('adminindex_view')

#     user.is_approved = True
#     user.save()
#     messages.success(request, f"{user.username} has been approved successfully!")
#     return redirect('adminindex_view')




    
# @login_required
# def reject_user(request, user_id):
#     if request.user.role != 'Admin':
#         messages.error(request, "You are not authorized to perform this action.")
#         return redirect('login')

#     user = get_object_or_404(User, id=user_id)

#     if user.role == 'Admin':
#         messages.warning(request, "You cannot reject another Admin account.")
#         return redirect('adminindex_view')

#     user.is_approved = False
#     user.save()
#     messages.error(request, f"{user.username} has been rejected.")
#     return redirect('adminindex_view')
    


# def calltoaction_view(request):
#     return render(request,'tmp_user/calltoaction.html')

# def classes_view(request):
#     return render(request,'tmp_user/classes.html')

# def contact_view(request):
#     return render(request,'tmp_user/contact.html')



# def team_view(request):
#     return render(request,'tmp_user/team.html')

@login_required(login_url="/login")
def my_orders_view(request):
    requests = models.RentalRequest.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'tmp_user/my_orders.html', {'requests': requests})

@login_required(login_url="/login")
def initiate_payment(request, pk):
    rental_req = get_object_or_404(models.RentalRequest, id=pk, user=request.user)
    if rental_req.status == 'ACCEPTED':
        if request.method == 'POST':
            method = request.POST.get('payment_method', 'CARD')
            rental_req.payment_method = method
            rental_req.status = 'PAID'
            rental_req.save()
            
            # If this is an extension, update the original rental
            if rental_req.is_extension and rental_req.original_rental:
                orig = rental_req.original_rental
                from datetime import timedelta, date
                
                # Fallback if rental_end_date was not set (for older orders)
                base_date = orig.rental_end_date if orig.rental_end_date else (orig.delivery_date if orig.delivery_date else date.today())
                
                orig.rental_end_date = base_date + timedelta(weeks=rental_req.rental_duration_weeks)
                orig.rental_duration_weeks = (orig.rental_duration_weeks or 0) + rental_req.rental_duration_weeks
                orig.total_price += rental_req.total_price
                orig.save()
                messages.success(request, f"Rental extended successfully! New return date: {orig.rental_end_date}")
            else:
                messages.success(request, f"Payment successful via {method} for {rental_req.toy.name}! Your rental is now confirmed.")
        else:
            messages.warning(request, "Please submit the payment form.")
    else:
        messages.error(request, "This request is not ready for payment.")
    return redirect('my_orders_view')

@login_required(login_url="/login")
def extend_rental(request, pk):
    original_req = get_object_or_404(models.RentalRequest, id=pk, user=request.user)
    
    if request.method == 'POST':
        weeks = int(request.POST.get('weeks', 1))
        toy_obj = original_req.toy
        price_per_week = toy_obj.rental_price_per_week
        
        # Create a new request for the extension
        extension_req = models.RentalRequest.objects.create(
            user=request.user,
            toy=toy_obj,
            rental_provider=original_req.rental_provider,
            quantity=original_req.quantity,
            total_price=float(price_per_week) * weeks * original_req.quantity,
            security_deposit=0, # No new deposit for extension
            status='PENDING', # Requires approval from provider
            is_extension=True,
            original_rental=original_req,
            rental_duration_weeks=weeks,
            # Use original delivery/address info
            first_name=original_req.first_name,
            last_name=original_req.last_name,
            email=original_req.email,
            phone=original_req.phone,
            address=original_req.address,
            city=original_req.city,
            pincode=original_req.pincode
        )
        
        messages.success(request, f"Extension request submitted for {weeks} week(s). Awaiting provider approval.")
        return redirect('my_orders_view')
    
    return redirect('my_orders_view')

@login_required(login_url="/login")
def generate_invoice(request, pk):
    rental_req = get_object_or_404(models.RentalRequest, id=pk, user=request.user)
    if rental_req.status != 'PAID' and rental_req.status != 'COMPLETED':
        messages.error(request, "Invoice is available only for paid orders.")
        return redirect('my_orders_view')
    return render(request, 'tmp_user/invoice.html', {'req': rental_req})

@login_required(login_url="/login")
def cancel_rental(request, pk):
    rental_req = get_object_or_404(models.RentalRequest, id=pk, user=request.user)
    
    # Allow cancellation only if status is PENDING or ACCEPTED
    if rental_req.status in ['PENDING', 'ACCEPTED']:
        rental_req.status = 'REJECTED'
        rental_req.save()
        messages.success(request, f"Order #{pk} has been cancelled successfully.")
    else:
        messages.error(request, "This order cannot be cancelled at its current stage.")
        
    return redirect('my_orders_view')

