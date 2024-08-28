from django.urls import path
from . import views



urlpatterns = [
   path('', views.product_view, name='home'),
   path('login/', views.login_view, name='login'),
   path('signup/', views.signup_view, name='signup'),
   path('logout/', views.logout_view, name='logout'),
   path('create/', views.creatProduct, name='create'),
   path('update/<str:pk>/', views.updateProduct, name='product-update'),
   path('delete/<str:pk>/', views.deleteProduct, name='product-delete'),
   path('description/<str:pk>/', views.productDescription, name='product-description')

]
