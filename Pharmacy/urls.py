from django.conf.urls import url
from django.urls import path,include
from .views import *
from django.contrib.auth.views import  LogoutView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('home/' ,main, name='main'),
    path('store/', store ,name='store'),
    path('product_details/', productdetails ,name='productdetails'),

    path('',homepage ,name='homepage'),
    path('storepage/',productpage ,name='storepage'),
    path('categorypage/',category_page ,name='categorypage'),
    path('bestdeal/',bestdeal_page ,name='bestdealpage'),
    path('topselling/',topselling_page ,name='topsellingpage'),
    path('brands/',brands_page ,name='brandspage'),


    path('logout/', LogoutView.as_view(), name='logout'),
    url(r'^login/$', log_in, name='login'),
    url(r'^signup/$', signup, name='signup'),
    path('quick/', quick, name='quick'),




    path('<int:product_id>/Product/', Product_Detail, name='product_details'),


    url(r'^password/$',change_password, name='change_password'),
    url('^', include('django.contrib.auth.urls')),



    url('^catalog(?P<catalogue_id>\d+)$', productbycatalog, name='ProductItem'),
    url('^brand(?P<brand_id>\d+)$', productbybrand, name='Productbrand'),
    url('^brand(?P<brand_id>\d+)$', productbybrand, name='Productbrand'),
    path('Brands/',brand,name='brands'),
    path('category/', category, name='category'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),

    path('update_item/', updateItem, name='update_item'),
    path('update_wish/', updateWish, name='update_wish'),
    path('<int:account_id>/edit/', edit_account, name='edit_account'),

    path('Profile/', profile, name='profile'),


    path('<int:account_id>/UserAccount/', account, name='account'),
    url(r'^ajax/validate_username/$', validate_username, name='validate_username'),

]

