from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Customer, OrderItem, ItemType
from .form import Product_creation_form
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
     



def login_view(request):
    
    page='login'
    if request.method=='POST':
        username= request.POST.get('Username')
        password= request.POST.get('password')
        email= request.POST.get('email')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    
        else:
            return HttpResponse('you are not yet a register user')
    form= UserCreationForm(request.POST)
    context= {'form':form}
    return render(request, 'base/login_signup.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # if form.is_valid():
            # user= form.save(commit=False)
            user.username= user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
            # username = form.cleaned_data.get('username')
            # password = form.cleaned_data.get('password1')
            # user = authenticate(username=username, password=password) 
            # if user is not None:
            #     login(request, user)  
                # return redirect('home')  
        else:
            return HttpResponse('an error occured during registration')
    form = UserCreationForm()
    context= {'form': form}
    return render(request, 'base/register.html', context)


def logout_view(request):
    if request.method=="POST":
        logout(request) 
        return redirect('home')

    return render(request, 'base/logout_confirmation.html')    


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
    




# Create your views here.
