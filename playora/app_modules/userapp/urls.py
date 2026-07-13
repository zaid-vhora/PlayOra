from django.contrib import admin
from django.urls import path,include
from app_modules.userapp import views

urlpatterns = [
    
    
path('',views.index_view,name="index_view"),


#pages

 
path('about_view/',views.about_view,name="about_view"),

# path('blog_view/',views.blog_view,name="blog_view"),

path('shop_view/',views.shop_view,name="shop_view"),

path('cart_view/',views.cart_view,name="cart_view"),

path('checkout_view/',views.checkout_view,name="checkout_view"),

path('contact_view/',views.contact_view,name="contact_view"),

path('faq_view/',views.faq_view,name="faq_view"),

# path('login_view/',views.login_view,name="login_view"),

path('ordersuccess_view/',views.ordersuccess_view,name="ordersuccess_view"),

path('profile_view/',views.profile_view,name="profile_view"),
path('profile_edit/',views.profile_edit_view,name="profile_edit_view"),

# path('register_view/',views.register_view,name="register_view"),

path('services_view/',views.services_view,name="services_view"),

path('shop_view/',views.shop_view,name="shop_view"),

path('toydetail_view/<int:id>/',views.toydetail_view,name="toydetail_view"),

path('toy_view/',views.toy_view,name="toy_view"),

path('categories/',views.all_categories_view,name="all_categories_view"),

path('wishlist_view/',views.wishlist_view,name="wishlist_view"),
path('wishlist/add/<int:id>/', views.wishlist_add, name='wishlist_add'),
path('wishlist/remove/<int:id>/', views.wishlist_remove, name='wishlist_remove'),

    
    #  login register with roll model
    
    
path('user-register/', views.user_register_view, name='user_register'),
path('rental-register/', views.rental_register_view, name='rental_register'),
path('login/', views.login_view, name='login'),
path('logout/', views.logout_view, name='logout'),


path('admin-dashboard/', views.adminindex_view, name='adminindex_view'),
path('approve/<int:rental_id>/', views.approve_rental, name='approve_rental'),
path('reject/<int:rental_id>/', views.reject_rental, name='reject_rental'), 

    
    # cart
path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
path('cart/item_increment/<int:id>/',views.item_increment, name='item_increment'),
path('cart/item_decrement/<int:id>/',views.item_decrement, name='item_decrement'),
path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
path('cart/cart-detail/',views.cart_detail,name='cart_detail'),     
    
    
    
    
path('my_orders/', views.my_orders_view, name='my_orders_view'),
path('initiate_payment/<int:pk>/', views.initiate_payment, name='initiate_payment'),
path('extend_rental/<int:pk>/', views.extend_rental, name='extend_rental'),
path('generate_invoice/<int:pk>/', views.generate_invoice, name='generate_invoice'),
path('cancel_rental/<int:pk>/', views.cancel_rental, name='cancel_rental'),
]