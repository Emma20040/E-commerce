from django.db import models


class ItemType(models.Model):
     name=models.CharField(max_length=200)

     def __str__(self):
          return self.name

class Product(models.Model):
    name= models.CharField(max_length=100)
    image=models.ImageField(upload_to=('static/images/'), height_field=None, width_field=None, max_length=None)
    price= models.DecimalField(max_digits=20, decimal_places=3)
    description= models.TextField(max_length=2000)
    category= models.ForeignKey(ItemType, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
    

class Customer(models.Model):
    first_name= models.CharField(max_length=100, blank=False, null=False)
    last_name= models.CharField(max_length=100, blank=False, null=False)
    email= models.EmailField()
    address= models.CharField(max_length=150)
    city= models.CharField(max_length=100)
    created= models.DateTimeField(auto_now_add=True)
    updated= models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
    

class OrderItem(models.Model):
    customer= models.ForeignKey(Customer, related_name='items', on_delete=models.CASCADE)
    product= models.ForeignKey(Product, related_name='order_item', on_delete=models.CASCADE)
    price= models.DecimalField(max_digits=20, decimal_places=3)
    quantity= models.PositiveIntegerField(default=1)


    def __str__(self):
        return f'Customer: {self.customer}: Product:{self.product} '
    
    



# Create your models here.