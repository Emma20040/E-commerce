from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Product, Customer, OrderItem, ItemType
from .form import Product_creation_form
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .decorators import user_not_authenticated
from django.contrib import messages
from .form import Signup_form
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from django.contrib.auth import get_user_model

def activateEmail(request, user, to_email):
    mail_subjuct= 'confirm your email address'
    message= render_to_string('base/activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })

    email= EmailMessage(mail_subjuct, message, to=[to_email])
    if email.send:
            messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
            received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'problem sending confirmation email to {to_email}, check if you typed the email correctly')


def activate(request, uidb64, token):
    user= get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    
    except(TypeError,ValueError, OverflowError, User.DoesNotExist):
        user= None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, ' You have successfully veried your account, so you can now login into your account')
        return redirect('login')
    
    else:
        messages.error(request, 'activation link invalid')
        
    return redirect('home')

@user_not_authenticated
def signup_view(request):
    if request.method =='POST':
        form = Signup_form(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active=False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('home')
        
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
        
    else:
        form = Signup_form()
    
    context={"form":form}
    return render(request, 'base/register.html', context)



#old singup_view
'''def signup_view(request):
    if request.method == 'POST':
        form = Signup_form(request.POST)
        if form.is_valid():
            user = form.save()
            
            user= form.save()
            user.username= user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
            
        else:
            return HttpResponse('an error occured during registration')
    form = Signup_form()
    context= {'form': form}
    return render(request, 'base/register.html', context)'''


def login_view(request):
    page='login'
    if request.method=='POST':
        username= request.POST.get('Username')
        password= request.POST.get('password')
        email = request.POST.get('email')
        user = authenticate(request, username=username, password=password, email= email)
        if user is not None:
            login(request, user)
            return redirect('home')
    
        else:
            return HttpResponse('you are not yet a register user')
    form= Signup_form(request.POST)
    context= {'form':form}
    return render(request, 'base/login_signup.html', context)




def logout_view(request):
    if request.method=="POST":
        logout(request) 
        return redirect('home')

    return render(request, 'base/logout_confirmation.html')   


def profile(request):
    pass


def product_view(request):
    q= request.GET.get('q', '')
    # products=Product.objects.filter(category__name__icontains=q)
    # q = request.GET.get('q', '') if request.GET.get('q') != None else''

    products= Product.objects.filter(Q(category__name__icontains=q) |
        Q(name__icontains=q)
        )
    categorys = ItemType.objects.all()
    # products = Product.objects.all()
    context={'products':products, 'currency_symbol': '$', 'categorys': categorys}
    return render(request, 'base/home.html', context)

@login_required(login_url='login')
def creatProduct(request):
    form= Product_creation_form()
    if request.method=="POST":
        form= Product_creation_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        return HttpResponse('not valid')
        
    context= {'form':form}
    return render(request, 'base/create_product.html', context)

@login_required(login_url='login')
def updateProduct(request, pk):
    product= Product.objects.get(pk=pk)
    form = Product_creation_form( instance=product)
    if request.method== 'POST':
        form = Product_creation_form(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context={'form':form}
    return render(request, 'base/create_product.html', context)


@login_required(login_url='login')
def deleteProduct(request, pk):
    product = Product.objects.get(pk= pk)
    if request.method=="POST":
        product.delete()
        return redirect('home')
    
    context={'product':product}
    return render(request, 'base/delete.html', context)


def productDescription(request, pk):
    product= Product.objects.get(pk=pk)
    context= {'product':product}
    return render(request, 'base/description.html', context)


def image_view(request, pk):
    product= Product.objects.get(pk=pk)
    context={'product':product}
    return render(request, 'base/image.html', context)

    



# views for the cart system


def product_list(request):
    products= Product.objects.all()
    context={'products':products}
    return render(request, 'base/product_list.html', context)


@login_required(login_url='login')
def cart_detail(request):
    cart_items = OrderItem.objects.filter(user=request.user)
    total_price= sum(item.product.price * item.quantity for item in cart_items)
    
    context={'cart_items':cart_items, 'total_price':total_price}
    return render(request, 'base/cart_details.html', context)


@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = Product.objects.get(id = product_id)
    user = request.user
    item = OrderItem(user = user, product = product)
    item.save()
    return redirect('cart-detail')


    
    # cart_item = Product.objects.filter(user=request.user, product=product_id).first()

    # if cart_item:
    #     cart_item.quantity += 1
    #     cart_item.save()
    #     messages.success(request, "Item added to your cart.")
    # else:
    #     cart_item, created = OrderItem.objects.get_or_create(cart_item=cart_item, 
    #                                                   user=request.user)
    
    #     OrderItem.objects.create(user=request.user, product=product_id)
    #     messages.success(request, "Item added to your cart.")

    # return redirect("base/cart_detail.html")

'''def add_to_cart(request, product_id):
    # Fetch the product object from the database
    product = get_object_or_404(Product, id=product_id)
    
    # Retrieve the cart from the session or create a new one
    cart = request.session.get('cart', {})

    # Check if the product is already in the cart
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {
            'name': product.name,
            'price': str(product.price),
            'quantity': 1
        }
    
    # Save the updated cart in the session
    request.session['cart'] = cart
    
    
    # Optionally, show a message to the user
    messages.success(request, f"Added {product.name} to your cart!")
    
    # Redirect to the cart page or the product page
    return render(request, 'base/cart_details.html', {})  # or use 'product_detail', args=[product_id]


'''


def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(OrderItem, id=item_id)
    # cart_item = OrderItem.objects.get( id=item_id)

    # if request.method== 'POST':
    
    if cart_item.user == request.user:
         cart_item.delete()
         messages.success(request, "Item removed from your cart.")
    
    return redirect('cart-detail')


