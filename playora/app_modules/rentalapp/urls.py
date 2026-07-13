from django.contrib import admin
from django.urls import path,include
from app_modules.rentalapp import views

urlpatterns = [
    
path('rentalindex_view/',views.rentalindex_view,name="rentalindex_view"),
  
  
  
# path('rentallogin_view/',views.rentallogin_view,name="rentallogin_view"), 
# path('rentalregister_view/',views.rentalregister_view,name="rentalregister_view"), 
# path('logout_view/',views.logout_view,name="logout_view"),  



# path('derentalregister/', views.derenatalregister_view, name='register'),
# path('logout/', views.logout_view, name='logout'),



path('create_category_rental/',views.create_category_rental,name="create_category_rental"),
path('list_category_rental/',views.list_category_rental,name="list_category_rental"),
path('rental_profile_view/',views.rental_profile_view,name="rental_profile_view"),
path('update_category_rental/<int:pk>/',views.update_category_rental,name="update_category_rental"),
path('delete_category_rental/<int:pk>/',views.delete_category_rental,name="delete_category_rental"),

path('create_subcategory_rental/',views.create_subcategory_rental,name="create_subcategory_rental"),
path('list_subcategory_rental/',views.list_subcategory_rental,name="list_subcategory_rental"),
path('update_subcategory_rental/<int:pk>/',views.update_subcategory_rental,name="update_subcategory_rental"),
path('delete_subcategory_rental/<int:pk>/',views.delete_subcategory_rental,name="delete_subcategory_rental"),


path('create_toy_rental/',views.create_toy_rental,name="create_toy_rental"),
path('list_toy_rental/',views.list_toy_rental,name="list_toy_rental"),
path('update_toy_rental/<int:pk>/',views.update_toy_rental,name="update_toy_rental"),
path('delete_toy_rental/<int:pk>/',views.delete_toy_rental,name="delete_toy_rental"),
     
# path('create_toyimage_rental/',views.create_toyimage_rental,name="create_toyimage_rental"),
# path('list_toyimage_rental/',views.list_toyimage_rental,name="list_toyimage_rental"),     


path('create_damagereport_rental/',views.create_damagereport_rental,name="create_damagereport_rental"),
path('list_damagereport_rental/',views.list_damagereport_rental,name="list_damagereport_rental"),
path('update_damagereport_rental/<int:id>/',views.update_damagereport_rental,name="update_damagereport_rental"),
path('delete_damagereport_rental/<int:id>/',views.delete_damagereport_rental,name="delete_damagereport_rental"),    


path('create_banner_rental/',views.create_banner_rental,name="create_banner_rental"),
path('list_banner_rental/',views.list_banner_rental,name="list_banner_rental"), 
path('update_banner_rental/<int:id>/',views.update_banner_rental,name="update_banner_rental"),
path('delete_banner_rental/<int:id>/',views.delete_banner_rental,name="delete_banner_rental"),


path('create_contactmessage_rental/',views.create_contactmessage_rental,name="create_contactmessage_rental"),
path('list_contactmessage_rental/',views.list_contactmessage_rental,name="list_contactmessage_rental"),
path('update_contactmessage_rental/<int:id>/',views.update_contactmessage_rental,name="update_contactmessage_rental"),
path('delete_contactmessage_rental/<int:id>/',views.delete_contactmessage_rental,name="delete_contactmessage_rental"),


path('create_coupon_rental/',views.create_coupon_rental,name="create_coupon_rental"),
path('list_coupon_rental/',views.list_coupon_rental,name="list_coupon_rental"),
path('update_coupon_rental/<int:id>/',views.update_coupon_rental,name="update_coupon_rental"),
path('delete_coupon_rental/<int:id>/',views.delete_coupon_rental,name="delete_coupon_rental"),       
     
path('create_siteSettings_rental/',views.create_siteSettings_rental,name="create_siteSettings_rental"),
path('list_siteSettings_rental/',views.list_siteSettings_rental,name="list_siteSettings_rental"),
path('update_siteSettings_rental/<int:id>/',views.update_siteSettings_rental,name="update_siteSettings_rental"),
path('delete_siteSettings_rental/<int:id>/',views.delete_siteSettings_rental,name="delete_siteSettings_rental"),



     
path('create_cart/',views.create_cart,name="create_cart"),
path('list_cart/',views.list_cart,name="list_cart"),
path('update_cart/<int:id>/',views.update_cart,name="update_cart"), 
path('delete_cart/<int:id>/',views.delete_cart,name="delete_cart"),

path('create_rental/',views.create_rental,name="create_rental"),
path('list_rental/',views.list_rental,name="list_rental"),
path("update_rental/<int:id>/",views.update_rental,name="update_rental"),
path('delete_rental/<int:id>/',views.delete_rental,name="delete_rental"),


path('create_rentalitem/',views.create_rentalitem,name="create_rentalitem"),
path('list_rentalitem/',views.list_rentalitem,name="list_rentalitem"),
path("update_rentalitem/<int:id>/",views.update_rentalitem,name="update_rentalitem"),
path('delete_rentalitem/<int:id>/',views.delete_rentalitem,name="delete_rentalitem"),


path('create_payment',views.create_payment,name="create_payment"),


path('create_ReturnRequest',views.create_ReturnRequest,name="create_ReturnRequest"),


path('create_Refund',views.create_Refund,name="create_Refund"),



path('create_LateFee',views.create_LateFee,name="create_LateFee"),




 


# path('create_',views.create_,name="create_"),



path('rental_requests/', views.rental_requests_list, name='rental_requests_list'),
path('rental_requests/approve/<int:pk>/', views.approve_rental_request, name='approve_rental_request'),
path('rental_requests/reject/<int:pk>/', views.reject_rental_request, name='reject_rental_request'),
path('update_rental_status/', views.update_rental_status, name='update_rental_status'),
]