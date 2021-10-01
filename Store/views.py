from django.shortcuts import render ,redirect
from .models import *
from Pharmacy.models import Userprofile,User,Customer
from Pharmacy.forms import ProfileForm, UserForm
from .forms import AddProductForm ,AddCatalogForm ,AddBrandForm,OrderForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count





@login_required
def dash(request):
    print(request.user.first_name)
    if (request.user.first_name != "admin" and  not (request.user.is_superuser)):
        return redirect('homepage')



    users = Userprofile.objects.all()
    customers = Customer.objects.all()
    orderitems = OrderItem.objects.all()

    products = Product.objects.all()
    brands = Brand.objects.all()
    categories = Catalogue.objects.all()
    total_products = Product.objects.count()
    total_users = Userprofile.objects.count()
    total_catalogues = Catalogue.objects.count()
    total_brands = Brand.objects.count()
    total_customers = Customer.objects.count()
    labels = []
    data = []

    queryset = OrderItem.objects.order_by('-quantity')[:5]
    for oi in queryset:
        labels.append(oi.product.name)
        data.append(oi.quantity)

    context = {'orderitems': orderitems, 'total_customers': total_customers, 'customers': customers,
               'categories': categories, 'products': products, 'users': users, 'brands': brands,
               'total_users': total_users, 'total_products': total_products, 'total_brands': total_brands,
               'total_catalogues': total_catalogues, 'labels': labels,
        'data': data,}
    return render(request, 'Store/dash.html', context)


@login_required
def addproduct(request):
    if request.method =='POST' :
        form = AddProductForm(request.POST,request.FILES )
        if form.is_valid():
            form.save()
            return redirect('dash')
    else:
        form = AddProductForm()

    users = User.objects.all()
    customers = Customer.objects.all()
    products = Product.objects.all()
    brands = Brand.objects.all()
    categories = Catalogue.objects.all()


    context = {'customers':customers, 'categories':categories, 'products':products,'users':users,'brands':brands,'form':form}

    return render(request,'Store/Add_Product.html', context)

@login_required
def addBrand(request):
    if request.method =='POST' :
        form = AddBrandForm(request.POST,request.FILES )
        if form.is_valid():
            form.save()
            return redirect('dash')
    else:
        form = AddBrandForm()
    return render(request,'Store/Add_Brand.html', {'form': form })

@login_required
def addcatalog(request):
    if request.method =='POST' :
        form = AddCatalogForm(request.POST,request.FILES )
        cata = form.save(commit=False)
        cata.by =request.user
        cata.save()
        if form.is_valid():
            form.save()
            return redirect('dash')
    else:
        form = AddCatalogForm()
    return render(request,'Store/Add_Catalogue.html', {'form': form })
@login_required
def adduser(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        print(user_form)
        # print(profile_form)
        if user_form.is_valid() and profile_form.is_valid():
            NAME = request.POST['username']
            PASS = request.POST['password2']
            MAIL = request.POST['Email']

            user = User.objects.create_user(NAME, MAIL, PASS)
            user.first_name = "admin"
            user.save()

            '''
            user_form.first_name = "admin"
            user = user_form.save()
            user.first_name = "admin"
            profile_formfirst_name = "admin"
            profile = profile_form.save(commit=False)
            profile.user = user
            #profile.first_name = "admin"
            profile.save()
            '''
            return redirect('dash')
    else:
        user_form = UserForm
        profile_form = ProfileForm
    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'Store/Add_User.html', context)


@login_required
def dashboard_brand(request):
    brands = Brand.objects.all()
    context = {'brands': brands}
    return render(request,'Store/Dashboard_brands.html',context)
@login_required
def dashboard_users(request):
    users = Userprofile.objects.all()
    context = {'users':users}
    return render(request,'Store/Dashboard_Users.html',context)

@login_required
def dashboard_product(request):
    products= Product.objects.all()
    context = {'products':products }
    return render(request,'Store/Dashboard_product.html',context)
@login_required
def dashboard_catalog(request):
    catalogues= Catalogue.objects.all()
    context = {'catalogues':catalogues}
    return render(request,'Store/Dashboard_catalog.html',context)






from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance,name=instance.username,email=instance.email,)


@login_required
def edit_product(request, product_id):
    product = Product.objects.get(pk=product_id)
    if request.method == 'POST':
        form = AddProductForm(request.POST, instance=product)

        if form.is_valid():
            product = form.save(commit=False)
            product.status = request.POST.get('status')
            product.save()

            return redirect('dash')
    else:
        form = AddProductForm(instance=product)

    context = {'form': form ,'product':product}
    return render(request, 'Store/Dashboard_editproduct.html',context)
@login_required
def edit_brand(request, brand_id):
    brand = Brand.objects.get(pk=brand_id)
    if request.method == 'POST':
        form = AddBrandForm(request.POST, instance=brand)

        if form.is_valid():
            brand = form.save(commit=False)
            brand.status = request.POST.get('status')
            brand.save()

            return redirect('dash')
    else:
        form = AddBrandForm(instance=brand)

    context = {'form': form ,'brand':brand}
    return render(request, 'Store/Dashboard_editbrand.html',context)

from Pharmacy.forms import NewUserForm,ProfileForm


@login_required
def edit_user(request, user_id):
    user = Userprofile.objects.get(pk=user_id)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)

        if form.is_valid():
            user = form.save(commit=False)
            user.status = request.POST.get('status')
            user.save()

            return redirect('dash')
    else:
        form = ProfileForm(instance=user)

    context = {'form': form ,'user':user}
    return render(request, 'Store/Dashboard_edituser.html',context)


def edit_order(request,order_id):
    order = OrderItem.objects.get(pk=order_id)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save(commit=False)
            order.status = request.POST.get('status')
            order.save()
            return redirect('dash')
    else:
        form = OrderForm(instance=order)

    context = {'form': form, 'order': order}
    return render(request, 'Store/Dashboard_editorder.html',context)



@login_required
def delete_product(request,product_id):
    product = Product.objects.get(pk=product_id)
    if request.method =='POST':
            product.delete()
            return redirect('dash')
    context = {'product': product}
    return render(request, 'Store/Dashboard_deleteproduct.html', context)

@login_required
def delete_user(request,user_id):
    user = Userprofile.objects.get(pk=user_id)
    if request.method =='POST':
            user.delete()
            return redirect('dash')
    context = {'user': user}
    return render(request, 'Store/Dashboard_deleteuser.html', context)


@login_required
def delete_brand(request,brand_id):
    brand = Brand.objects.get(pk=brand_id)
    if request.method =='POST':
            brand.delete()
            return redirect('dash')
    context = {'brand': brand}
    return render(request, 'Store/Dashboard_deletebrand.html', context)
@login_required

def edit_catalog(request, catalog_id):
    catalog = Catalogue.objects.get(pk=catalog_id)
    if request.method == 'POST':
        form = AddCatalogForm(request.POST, instance=catalog)
        if form.is_valid():
            catalog = form.save(commit=False)
            catalog.status = request.POST.get('status')
            catalog.save()

            return redirect('dash')
    else:
        form = AddCatalogForm(instance=catalog)

    context = {'form': form ,'catalog':catalog}
    return render(request, 'Store/Dashboard_editcatalog.html',context)

@login_required
def delete_catalog(request,catalog_id):
    catalog = Catalogue.objects.get(pk=catalog_id)
    if request.method =='POST':
            catalog.delete()
            return redirect('dash')
    context = {'catalog': catalog}
    return render(request, 'Store/Dashboard_deletecatalog.html', context)

@login_required
def archive(request,product_id):
    product = Product.objects.get(pk=product_id)

    if request.method == 'POST':
        if product.is_archived :
            product.is_archived = False
            product.save()
            return redirect('dash')
        else:
            product.is_archived = True
            product.save()
            return redirect('dash')
    context = {'product': product}
    return render(request, 'Store/Dashboard_archiveproduct.html', context)

@login_required
def desarchive(request,product_id):
    product = Product.objects.get(pk=product_id)

    if request.method == 'POST':
        product.is_archived =False
        product.save()
        return redirect('dash')
    context = {'product': product}
    return render(request, 'Store/Dashboard_desarchiveproduct.html', context)

@login_required

def archivelist(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'Store/Dashboard_listarchives.html', context)
