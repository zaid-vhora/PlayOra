from django.contrib import admin
from django.urls import path,include
from app_modules.adminapp import views


urlpatterns = [
path('adminindex_view/',views.adminindex_view,name="adminindex_view"),


# chart
# path('chartjs_view/',views.chartjs_view,name="chartjs_view"),

#forms
# path('basicelements_view/',views.basicelements_view,name="basicelements_view"),


#icnos
# path('mdi_view/',views.mdi_view,name="mdi_view"),


#tables
# path('basictable_view/',views.basictable_view,name="basictable_view"),
# path('login_view/',views.login_view,name="login_view"), 
# path('register_view/',views.register_view,name="register_view"), 
# path('logout_view/',views.logout_view,name="logout_view"),






#ui_features
# path('buttons_view/',views.buttons_view,name="buttons_view"), 
# path('dropdowns_view/',views.dropdowns_view,name="dropdowns_view"),
# path('typography_view/',views.typography_view,name="typography_view"),


#   project urls


path('create_category/',views.create_category,name="create_category"),
path('list_category/',views.list_category,name="list_category"),
path('update_category/<int:id>/',views.update_category,name="update_category"),
path('delete_category/<int:id>/',views.delete_category,name="delete_category"),







path('create_subcategory/',views.create_subcategory,name="create_subcategory"),
path('list_subcategory/',views.list_subcategory,name="list_subcategory"),
path('update_subcategory/<int:id>/',views.update_subcategory,name="update_subcategory"),
path('delete_subcategory/<int:id>/',views.delete_subcategory,name="delete_subcategory"),




# path('create_toy/',views.create_toy,name="create_toy"),
path('list_toy/',views.list_toy,name="list_toy"),
# path('update_toy/<int:id>/',views.update_toy,name="update_toy"),
path('delete_toy/<int:id>/',views.delete_toy,name="delete_toy"),

path('logout_view/', views.logout_view, name='logout_view'),

# path('create_toyimage/',views.create_toyimage,name="create_toyimage"),
# path('list_toyimage/',views.list_toyimage,name="list_toyimage"),

path('create_damagereport/',views.create_damagereport,name ="create_damagereport"),
path('list_damagereports/',views.list_damagereports,name ="list_damagereports"),
path('update_damagereport/<int:id>/',views.update_damagereport,name ="update_damagereport"),
path('delete_damagereport/<int:id>/',views.delete_damagereport,name ="delete_damagereport"),


path('create_banner/',views.create_banner,name="create_banner"),
path('list_banner/',views.list_banner,name="list_banner"),
path('update_banner/<int:id>/',views.update_banner,name="update_banner"),
path('delete_banner/<int:id>/',views.delete_banner,name="delete_banner"),

path('create_contactmessage/',views.create_contactmessage,name="create_contactmessage"),
path('list_contactmessage/',views.list_contactmessage,name="list_contactmessage"),
path('update_contactmessage/<int:id>/',views.update_contactmessage,name="update_contactmessage"),
path('delete_contactmessage/<int:id>/',views.delete_contactmessage,name="delete_contactmessage"),

path('create_coupon/',views.create_coupon,name="create_coupon"),
path('list_coupon/',views.list_coupon,name="list_coupon"),
path('update_coupon/<int:id>/',views.update_coupon,name="update_coupon"),
path('delete_coupon/<int:id>/',views.delete_coupon,name="delete_coupon"),

path('create_siteSettings/',views.create_siteSettings,name="create_siteSettings"),
path('list_siteSettings/',views.list_siteSettings,name="list_siteSettings"),
path('update_siteSettings/<int:id>/',views.update_siteSettings,name="update_siteSettings"),
path('delete_siteSettings/<int:id>/',views.delete_siteSettings,name="delete_siteSettings"),

path('rental_tracking/', views.rental_tracking_list_view, name="rental_tracking_list_view"),
path('update_rental_status/<int:rental_id>/', views.update_rental_status_view, name="update_rental_status_view"),

 
    
]