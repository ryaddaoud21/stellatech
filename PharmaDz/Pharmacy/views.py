from django.contrib.auth.forms import UserCreationForm ,PasswordChangeForm
from Store.models import Catalogue , Product ,Brand,Order ,OrderItem,Wish,WishItem,Review,Images,MEMORY
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from .filters import ProductFilter
from django.http import JsonResponse
import json
from django.contrib.auth.forms import AuthenticationForm
from .forms import AddReviewForm
from django.contrib import messages
from .forms import CustomerForm

def is_valid_queryparam(param):
    return param != '' and param is not None


def filter(request):
    qs = Product.objects.all()
    catalogues = Catalogue.objects.all()
    brands = Brand.objects.all()
    brand = request.GET.get('brand')
    price__gt = request.GET.get('price__gt')
    price__lt = request.GET.get('price__lt')
    is_promo = request.GET.get('is_promo')
    is_garanted = request.GET.get('is_garanted')
    memory = request.GET.get('memory')
    system = request.GET.get('System')
    camera = request.GET.get('camera')



    if is_valid_queryparam(brand) and brand != 'Choose...':
        qs = qs.filter(brand__name=brand)

    if is_valid_queryparam(price__gt):
        qs = qs.filter(price__gt=price__gt)

    if is_valid_queryparam(price__lt):
        qs = qs.filter(price__lt=price__lt)

    if is_valid_queryparam(memory):
        qs = qs.filter(Memory=memory)

    if is_valid_queryparam(system):
        qs = qs.filter(System=system)


    if is_valid_queryparam(camera):
        if camera=='up to 2.9 MP' :
             qs = qs.filter(Cam__lt=2.9)
        elif camera=='3 to 4.9 MP':
            qs = qs.filter(Cam__lt=4.9)
            qs = qs.filter(Cam__gt=3)
        elif camera=='5 to 7.9 MP':
            qs = qs.filter(Cam__lt=7.9)
            qs = qs.filter(Cam__gt=5)

        elif camera=='8 to 12.9 MP':
            qs = qs.filter(Cam__lt=12.9)
            qs = qs.filter(Cam__gt=8)

        elif camera=='13 to 19.9 MP':
            qs = qs.filter(Cam__lt=19.9)
            qs = qs.filter(Cam__gt=13)

        elif camera=='20 MP and above':
            qs = qs.filter(Cam__gt=20)

    if is_garanted == 'on':
        qs = qs.filter(is_garanted=True)

    if is_promo == 'on':
        qs = qs.filter(is_promo=True)

    return qs



def homepage(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=True)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

        '''-------------------------------------------------'''
        wish, created = Wish.objects.get_or_create(customer=customer, complete=True)
        items2= wish.wishitem_set.all()
        wishItems = wish.get_wish_items


    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = 0
        '''------------------------------------------------'''
        items2 = []
        wish = {'get_wish_total': 0, 'get_wish_items': 0}
        wishItems = 0




    catalogues = Catalogue.objects.all()
    brands =Brand.objects.all()
    products =Product.objects.all()
    filter = ProductFilter(request.GET, queryset=products)
    products = filter.qs
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 6)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    reviews =Review.objects.all()



    context = {'reviews':reviews,'catalogues': catalogues , 'items2': items2 ,'brands': brands , 'products':products ,'wish': wish,'filtre': filter , 'items': items , 'order': order ,'cartItems':cartItems ,'wishItems':wishItems}
    return render(request, 'Pharmacy/index.html', context)

from .models import Customer
from .forms import CustomerForm

def edit_account(request, account_id):
    account = Customer.objects.get(pk=account_id)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=account)

        if form.is_valid():
            account = form.save(commit=False)
            account.status = request.POST.get('status')
            account.user.username = request.user.username
            account.name = request.user.username
            account.last_name = request.user.username
            account.save()

            return redirect('homepage')
    else:
        form = CustomerForm(instance=account)

    context = {'form': form ,'account':account}

    return render(request, 'Pharmacy/edit_account.html',context)

def account(request,account_id):
    profile = Customer.objects.get(pk=account_id)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=True)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        '''-------------------------------------------------'''
        wish, created = Wish.objects.get_or_create(customer=customer, complete=True)
        items2 = wish.wishitem_set.all()
        wishItems = wish.get_wish_items


    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = 0
        '''------------------------------------------------'''
        items2 = []
        wish = {'get_wish_total': 0, 'get_wish_items': 0}
        wishItems = 0

    catalogues = Catalogue.objects.all()
    categories = Catalogue.objects.all
    brands = Brand.objects.all


    context = { 'account':profile, 'catalogues': catalogues, 'categories': categories,
               'items2': items2, 'brands': brands,  'wish': wish,  'items': items,
               'order': order, 'cartItems': cartItems, 'wishItems': wishItems}
    return render(request, 'Pharmacy/account.html', context)


from django.urls import reverse_lazy
from django.views import generic
def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)


def signup(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful")
            return redirect('homepage')
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=True)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        '''-------------------------------------------------'''
        wish, created = Wish.objects.get_or_create(customer=customer, complete=True)
        items2 = wish.wishitem_set.all()
        wishItems = wish.get_wish_items


    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = 0
        '''------------------------------------------------'''
        items2 = []
        wish = {'get_wish_total': 0, 'get_wish_items': 0}
        wishItems = 0

    catalogues = Catalogue.objects.all()
    categories = Catalogue.objects.all
    brands = Brand.objects.all
    products=Product.objects.all()


    context = {  'catalogues': catalogues, 'categories': categories,
               'items2': items2, 'brands': brands,  'wish': wish,  'items': items,
               'order': order, 'cartItems': cartItems, 'wishItems': wishItems,"register_form":form,'products':products}


    return render(request, 'registration/signup.html',context)



def log_in(request):
    if request.method == 'POST':
        form1 = AuthenticationForm(request=request, data=request.POST)
        if form1.is_valid():
            username = form1.cleaned_data.get('username')
            password = form1.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                 login(request, user)
                 return redirect('dash')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form1 = AuthenticationForm()

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=True)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        '''-------------------------------------------------'''
        wish, created = Wish.objects.get_or_create(customer=customer, complete=True)
        items2 = wish.wishitem_set.all()
        wishItems = wish.get_wish_items


    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = 0
        '''------------------------------------------------'''
        items2 = []
        wish = {'get_wish_total': 0, 'get_wish_items': 0}
        wishItems = 0

    catalogues = Catalogue.objects.all()
    categories = Catalogue.objects.all
    brands = Brand.objects.all
    products=Product.objects.all()


    context = {  'catalogues': catalogues, 'categories': categories,
               'items2': items2, 'brands': brands,  'wish': wish,  'items': items,
               'order': order, 'cartItems': cartItems, 'wishItems': wishItems,"form":form1,'products':products}


    return render(request, 'registration/login.html',context)



@login_required
def productdetails(request):
    catalogues = Catalogue.objects.all()
    brands =Brand.objects.all()
    products =Product.objects.all()
    filter = ProductFilter(request.GET, queryset=products)
    products = filter.qs
    context = { 'catalogues': catalogues , 'brands': brands , 'products':products ,'filtre': filter}
    return render(request, 'Pharmacy/product.html', context)


def productpage(request):
    catalogues = Catalogue.objects.all()
    brands =Brand.objects.all()
    products =Product.objects.all()
    filter = ProductFilter(request.GET, queryset=products)
    products = filter.qs
    context = { 'catalogues': catalogues , 'brands': brands , 'products':products ,'filtre': filter}

    return render(request, 'Pharmacy/productpage.html', context)

def main(request):
    catalogues = Catalogue.objects.all()
    brands =Brand.objects.all()
    context = { 'catalogues': catalogues , 'brands': brands}
    return render(request, 'Pharmacy/Main.html', context)

def brand(request):
    brands = Brand.objects.all()
    catalogues = Catalogue.objects.all()
    context = { 'brands': brands,'catalogues': catalogues  }
    return render(request, 'Pharmacy/Brands.html', context)

def category(request):
    brands = Brand.objects.all()
    catalogues = Catalogue.objects.all()
    context = { 'catalogues': catalogues,'brands': brands}
    return render(request, 'Pharmacy/Category.html', context)


from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import NewUserForm


def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=True)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems =['get_cart_items']
    products = Product.objects.all()
    catalogues = Catalogue.objects.all()
    brands = Brand.objects.all()
    filter = ProductFilter(request.GET, queryset=products)
    products = filter.qs
    context = {'products':products, 'catalogues': catalogues, 'filter':filter , 'brands':brands,'items':items,'order': order,'cartItems':cartItems}
    return render(request,'Pharmacy/Store.html',context)

from .forms import  UserForm,ProfileForm

from django.contrib.auth import login, authenticate





@login_required
def change_password(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=True)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        '''-------------------------------------------------'''
        wish, created = Wish.objects.get_or_create(customer=customer, complete=True)
        items2 = wish.wishitem_set.all()
        wishItems = wish.get_wish_items


    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = 0
        '''------------------------------------------------'''
        items2 = []
        wish = {'get_wish_total': 0, 'get_wish_items': 0}
        wishItems = 0



    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request,('Your password was successfully updated!'))
            return redirect('account')
        else:
            messages.error(request,('Please correct the error below.'))
    else:
        form = PasswordChangeForm(request.user)
    context = {'form': form,'items2': items2, 'wish': wish, 'filter': filter, 'wishItems': wishItems, 'items': items,
                   'order': order, 'cartItems': cartItems}

    return render(request, 'Pharmacy/Change_password.html', context)

def password_reset_request(request):
        if request.method == "POST":
            password_reset_form = PasswordResetForm(request.POST)
            if password_reset_form.is_valid():
                data = password_reset_form.cleaned_data['email']
                associated_users = User.objects.filter(Q(email=data))
                if associated_users.exists():
                    for user in associated_users:
                        subject = "Password Reset Requested"
                        email_template_name = "Pharmacy/password_reset_email.txt"
                        c = {
                            "email": user.email,
                            'domain': '127.0.0.1:8000',
                            'site_name': 'Website',
                            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                            "user": user,
                            'token': default_token_generator.make_token(user),
                            'protocol': 'http',
                        }
                        email = render_to_string(email_template_name, c)
                        try:
                            send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                        except BadHeaderError:
                            return HttpResponse('Invalid header found.')
                        messages.success(request,'A message with reset password instructions has been sent to your inbox.')

                        return redirect('password_reset_done')
                messages.error(request, 'An invalid email has been entered.')
        password_reset_form = PasswordResetForm()
        return render(request=request, template_name="Pharmacy/Password_reset_form.html",context={"password_reset_form": password_reset_form})

def productbycatalog(request,catalogue_id):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=True)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        '''-------------------------------------------------'''
        wish, created = Wish.objects.get_or_create(customer=customer, complete=True)
        items2 = wish.wishitem_set.all()
        wishItems = wish.get_wish_items


    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = 0
        '''------------------------------------------------'''
        items2 = []
        wish = {'get_wish_total': 0, 'get_wish_items': 0}
        wishItems = 0

    Cata = Catalogue.objects.get(pk=catalogue_id)
    catalogues = Catalogue.objects.all()
    products = Cata.catalog.all()
    filter = ProductFilter(request.GET, queryset=products)
    products = filter.qs
    categories = Catalogue.objects.all
    brands = Brand.objects.all
    page = request.GET.get('page', 1)
    total_prod = Catalogue.objects.filter(pk=catalogue_id).count()


    paginator = Paginator(products, 9)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context = {'Cata':Cata,'total_prod':total_prod, 'products': products , 'catalogues': catalogues,'categories': categories , 'items2': items2 ,'brands': brands , 'products':products ,'wish': wish,'filtre': filter , 'items': items , 'order': order ,'cartItems':cartItems ,'wishItems':wishItems}
    return render(request, 'Pharmacy/Store.html', context)

def productbybrand(request,brand_id):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=True)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        '''-------------------------------------------------'''
        wish, created = Wish.objects.get_or_create(customer=customer, complete=True)
        items2 = wish.wishitem_set.all()
        wishItems = wish.get_wish_items


    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = 0
        '''------------------------------------------------'''
        items2 = []
        wish = {'get_wish_total': 0, 'get_wish_items': 0}
        wishItems = 0

    mark = Brand.objects.get(pk=brand_id)
    catalogues = Catalogue.objects.all()
    products = mark.brand.all()
    filter = ProductFilter(request.GET, queryset=products)
    products = filter.qs
    brand = Brand.objects.get(pk=brand_id)
    brandtotal = Brand.objects.filter(pk=brand_id).count()
    page = request.GET.get('page', 1)
    total_prod = Brand.objects.filter(pk=brand_id).count()

    paginator = Paginator(products, 9)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context = {'total_prod':total_prod,'products': products, 'catalogues': catalogues ,'filter': filter ,'brand': brand ,'brandtotal':brandtotal, 'catalogues': catalogues, 'items2': items2  , 'products':products ,'wish': wish,'filtre': filter , 'items': items , 'order': order ,'cartItems':cartItems ,'wishItems':wishItems}
    return render(request, 'Pharmacy/Storebybrand.html', context)

@login_required
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        wish, created = Wish.objects.get_or_create(customer=customer, complete=True)
        items2 = wish.wishitem_set.all()
        wishItems = wish.get_wish_items


    else:

        '''------------------------------------------------'''
        items2 = []
        wish = {'get_wish_total': 0, 'get_wish_items': 0}
        wishItems = 0

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=True)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = ['get_cart_items']

    products = Product.objects.all()
    catalogues = Catalogue.objects.all()
    brands = Brand.objects.all()
    context = {'items': items, 'products': products, 'catalogues': catalogues, 'order': order, 'filter': filter,
               'brands': brands, 'catalogues': catalogues, 'items2': items2, 'products': products, 'wish': wish,
               'filtre': filter, 'items': items, 'order': order, 'cartItems': cartItems, 'wishItems': wishItems}

    return render(request, 'Pharmacy/Cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        wish, created = Wish.objects.get_or_create(customer=customer, complete=True)
        items2 = wish.wishitem_set.all()
        wishItems = wish.get_wish_items


    else:

        '''------------------------------------------------'''
        items2 = []
        wish = {'get_wish_total': 0, 'get_wish_items': 0}
        wishItems = 0

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=True)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0 , 'get_cart_items':0}
        cartItems = ['get_cart_items']

    products = Product.objects.all()
    catalogues = Catalogue.objects.all()
    brands = Brand.objects.all()
    context = {'items': items,'products': products, 'catalogues': catalogues ,'order':order,'filter': filter ,'brands': brands , 'catalogues': catalogues, 'items2': items2  , 'products':products ,'wish': wish,'filtre': filter , 'items': items , 'order': order ,'cartItems':cartItems ,'wishItems':wishItems}

    return render(request,'Pharmacy/Checkout.html',context)

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def updateItem(request):
    data = json.loads(request.body)
    productId= data['productId']
    action= data['action']
    print('Action:',action)
    print('productId:',productId)
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order,created = Order.objects.get_or_create(customer=customer,complete=True)
    orderItem,created=OrderItem.objects.get_or_create(order=order,product=product)
    if action=='add':
        orderItem.quantity =(orderItem.quantity+1)
    elif action=='remove':
        orderItem.quantity=(orderItem.quantity-1)
    orderItem.save()
    if orderItem.quantity<=0 or action=='delete' :
        orderItem.delete()
    return JsonResponse('Item was added ', safe=False)


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def updateWish(request):
    data = json.loads(request.body)
    productId= data['productId']
    action= data['action']
    print('Action:',action)
    print('productId:',productId)
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    wish,created = Wish.objects.get_or_create(customer=customer,complete=True)
    wishItem,created=WishItem.objects.get_or_create(wish=wish,product=product)

    if action=='add-wish':
        wishItem.quantity =(wishItem.quantity+1)
    elif action=='remove-wish':
        wishItem.quantity=(wishItem.quantity-1)
    wishItem.save()
    if wishItem.quantity<=0 or action=='delete-wish' :
        wishItem.delete()
    return JsonResponse('Item2 was added ', safe=False)





def Product_Detail(request,product_id):
    product = Product.objects.get(pk=product_id)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=True)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        '''-------------------------------------------------'''
        wish, created = Wish.objects.get_or_create(customer=customer, complete=True)
        items2 = wish.wishitem_set.all()
        wishItems = wish.get_wish_items


    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = 0
        '''------------------------------------------------'''
        items2 = []
        wish = {'get_wish_total': 0, 'get_wish_items': 0}
        wishItems = 0

    categories = Catalogue.objects.all()
    brands = Brand.objects.all()
    products = Product.objects.all()
    filter = ProductFilter(request.GET, queryset=products)
    products = filter.qs

    if request.method == 'POST':
        RATE = request.POST['rating']
        TEXT = request.POST['text']
        print(RATE, TEXT)
        id = request.user.username
        idP = Product.objects.get(pk=product_id)
        Rev = Review(username=id, product=idP, text=TEXT, rating=RATE)
        Rev.save()
        '''
        form = AddReviewForm(request.POST, request.FILES)

        if form.is_valid():
            review = form.save(commit=False)

            #print(form)
        if review.is_valid():
            review = form.save(commit=False)
            review.username = request.user.username
            review.product = Product.objects.get(pk=product_id)

        if review.is_valid():
            review.save()
        if form.is_valid():
            form.save()
        '''
        return redirect('.')
    else:
        AddReview = AddReviewForm()

    reviews = Review.objects.all()
    images = Images.objects.all()
    page = request.GET.get('page', 1)
    paginator1 = Paginator(products, 4)
    paginator = Paginator(reviews, 3)
    try:
        reviews = paginator.page(page)
        products = paginator1.page(page)

    except PageNotAnInteger:
        reviews = paginator.page(1)
        products = paginator1.page(1)

    except EmptyPage:
        reviews = paginator.page(paginator.num_pages)
        products = paginator1.page(paginator.num_pages)






    context = {'page':page,'reviews': reviews, 'AddReview': AddReview, 'categories': categories, 'items2': items2, 'brands': brands,
               'products': products, 'wish': wish,
               'filtre': filter, 'items': items, 'product': product, 'order': order, 'cartItems': cartItems,
               'wishItems': wishItems, 'images':images,
               }
    return render(request, 'Pharmacy/product_detail.html', context)

from django.core.paginator import Paginator
def quick(request):
    return render(request,'Pharmacy/quick.html',)



def category_page(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=True)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        '''-------------------------------------------------'''
        wish, created = Wish.objects.get_or_create(customer=customer, complete=True)
        items2= wish.wishitem_set.all()
        wishItems = wish.get_wish_items


    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = 0
        '''------------------------------------------------'''
        items2 = []
        wish = {'get_wish_total': 0, 'get_wish_items': 0}
        wishItems = 0



    categories = Catalogue.objects.all()
    total_cat=Catalogue.objects.count()
    brands =Brand.objects.all()
    products =Product.objects.all()
    filter = ProductFilter(request.GET, queryset=products)
    products = filter.qs

    page_1 = request.GET.get('page', 1)
    page_2 = request.GET.get('page', 1)
    paginator = Paginator(categories, 6)
    paginator_products = Paginator(products, 5)
    try:
        categories = paginator.page(page_1)
        products = paginator_products.page(page_2)
    except PageNotAnInteger:
        categories = paginator.page(1)
        products = paginator_products.page(1)
    except EmptyPage:
        categories = paginator.page(paginator.num_pages)
        products = paginator.page(paginator_products.num_pages)

    context = { 'total_cat':total_cat ,'categories': categories , 'items2': items2 ,'brands': brands , 'products':products ,'wish': wish,'filtre': filter , 'items': items , 'order': order ,'cartItems':cartItems ,'wishItems':wishItems}

    return render(request,'Pharmacy/categorypage.html',context)



def bestdeal_page(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=True)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        '''-------------------------------------------------'''
        wish, created = Wish.objects.get_or_create(customer=customer, complete=True)
        items2 = wish.wishitem_set.all()
        wishItems = wish.get_wish_items


    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = 0
        '''------------------------------------------------'''
        items2 = []
        wish = {'get_wish_total': 0, 'get_wish_items': 0}
        wishItems = 0

    categories = Catalogue.objects.all()
    brands = Brand.objects.all()
    products = Product.objects.all()
    products = filter(request)
    page = request.GET.get('page', 1)
    total_prod = products.count()
    taille = len(products)
    paginator = Paginator(products, 9)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)




    context = {'taille':taille,'total_prod':total_prod,'categories': categories, 'items2': items2, 'brands': brands, 'products': products, 'wish': wish,
               'filtre': filter, 'items': items, 'order': order, 'cartItems': cartItems, 'wishItems': wishItems}

    return render(request,'Pharmacy/bestdealpage.html',context)

def topselling_page(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=True)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        '''-------------------------------------------------'''
        wish, created = Wish.objects.get_or_create(customer=customer, complete=True)
        items2 = wish.wishitem_set.all()
        wishItems = wish.get_wish_items


    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = 0
        '''------------------------------------------------'''
        items2 = []
        wish = {'get_wish_total': 0, 'get_wish_items': 0}
        wishItems = 0

    categories = Catalogue.objects.all()
    brands = Brand.objects.all()
    products = Product.objects.all()

    products = filter(request)
    taille = len(products)


    page = request.GET.get('page', 1)
    total_prod = Product.objects.count()

    paginator = Paginator(products, 9)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {'taille':taille,'total_prod':total_prod,'categories': categories, 'items2': items2, 'brands': brands, 'products': products, 'wish': wish,
               'filtre': filter, 'items': items, 'order': order, 'cartItems': cartItems, 'wishItems': wishItems}

    return render(request, 'Pharmacy/topselling_page.html', context)


from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def brands_page(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=True)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        '''-------------------------------------------------'''
        wish, created = Wish.objects.get_or_create(customer=customer, complete=True)
        items2 = wish.wishitem_set.all()
        wishItems = wish.get_wish_items


    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = 0
        '''------------------------------------------------'''
        items2 = []
        wish = {'get_wish_total': 0, 'get_wish_items': 0}
        wishItems = 0

    categories = Catalogue.objects.all()
    brands = Brand.objects.all()
    products = Product.objects.all()
    filter = ProductFilter(request.GET, queryset=products)
    products = filter.qs
    page_1 = request.GET.get('page', 1)
    page_2 = request.GET.get('page', 1)
    paginator = Paginator(brands, 6)
    paginator_products = Paginator(products, 5)
    try:
        brands = paginator.page(page_1)
        products = paginator_products.page(page_2)
    except PageNotAnInteger:
        brands = paginator.page(1)
        products = paginator.page(1)
    except EmptyPage:
        brands = paginator.page(paginator.num_pages)
        products = paginator.page(paginator_products.num_pages)

    total_brand= Brand.objects.count()





    context = {'total_brand':total_brand,'categories': categories, 'items2': items2, 'brands': brands, 'products': products, 'wish': wish,
               'filtre': filter, 'items': items, 'order': order, 'cartItems': cartItems, 'wishItems': wishItems ,}


    return render(request,'Pharmacy/brands_page.html',context)

from django.contrib.auth.models import User

from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def profile(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=True)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        '''-------------------------------------------------'''
        wish, created = Wish.objects.get_or_create(customer=customer, complete=True)
        items2= wish.wishitem_set.all()
        wishItems = wish.get_wish_items


    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = 0
        '''------------------------------------------------'''
        items2 = []
        wish = {'get_wish_total': 0, 'get_wish_items': 0}
        wishItems = 0




    catalogues = Catalogue.objects.all()
    brands =Brand.objects.all()
    products =Product.objects.all()
    filter = ProductFilter(request.GET, queryset=products)
    products = filter.qs
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 5)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)




    context = {'catalogues': catalogues , 'items2': items2 ,'brands': brands , 'products':products ,'wish': wish,'filtre': filter , 'items': items , 'order': order ,'cartItems':cartItems ,'wishItems':wishItems}
    return render(request, 'Pharmacy/Profile.html', context)
