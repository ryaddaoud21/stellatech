from django.contrib import admin
from django.urls import path
from .views import *
from django.conf.urls import url


urlpatterns = [
    path('', dash ,name= 'dash'),
    path('AddUser/', adduser, name='AddUser'),
    path('Addproduct/', addproduct, name='Addproduct'),
    path('AddCatalog/', addcatalog, name='Addcatalog'),
    path('AddBrand/', addBrand, name='AddBrand'),


    path('<int:brand_id>/edit_brand/', edit_brand, name='brand_edit'),
    path('<int:order_id>/edit_order/', edit_order, name='order_edit'),

    path('<int:brand_id>/delete_brand/', delete_brand, name='brand_delete'),


    path('<int:product_id>/edit_product/', edit_product, name='product_edit'),
    path('<int:product_id>/delete_product/', delete_product, name='product_delete'),

    path('<int:catalog_id>/edit_catalog/', edit_catalog, name='catalog_edit'),
    path('<int:catalog_id>/delete_catalog/', delete_catalog, name='catalog_delete'),


    path('<int:user_id>/delete_user/', delete_user, name='user_delete'),
    path('<int:user_id>/edit_user/', edit_user, name='user_edit'),

    path('<int:product_id>/archive_catalog/', archive, name='product_archive'),
    path('<int:product_id>/archive_catalog/', desarchive, name='product_desarchive'),
    path('archive/', archivelist, name='archives'),
    path('products/', dashboard_product, name='dashboard_product'),
    path('catalogs/', dashboard_catalog, name='dashboard_catalog'),
    path('users/', dashboard_users, name='dashboard_users'),
    path('brand/', dashboard_brand, name='dashboard_brands'),

]
