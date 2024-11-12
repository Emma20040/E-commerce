from django.conf import settings
from django.core.mail import send_mail
from .models import Product, Profile
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms 


class Product_creation_form(ModelForm):
    class Meta:
        model=Product
        fields=['name', 'description', 'image', 'price', 'category']


class Signup_form(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')
    first_name= forms.CharField(max_length=100)
    last_name= forms.CharField(max_length=100)
    
    class Meta:
        model= User
        fields=['username','first_name', 'last_name', 'email', 'password1', 'password2']

def save(self, commit=True):
        user = super(Signup_form, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class Update_user_form(forms.ModelForm):
     username= forms.CharField(max_length=100,
                               required= True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
     email= forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
     first_name= forms.CharField(max_length=100,
                                 required=True,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
     
     last_name= forms.CharField(max_length=100,
                                 required=True,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))

  
     class Meta:
          model= User
          fields= ['username', 'email', 'first_name', 'last_name']


class UpdateProfile_form(forms.ModelForm):
     image= forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
     boi= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

     class Meta:
          model= Profile
          fields=['image', 'boi']

