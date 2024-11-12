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
   path('description/<str:pk>/', views.productDescription, name='product-description'),
   path('image/<str:pk>/', views.image_view, name='image-view'),
   path('profile/', views.profile, name='profile'),

   #urls for the cart system

   path('list/', views.product_list, name='product-list' ),
   path('details/', views.cart_detail, name='cart-detail'),
   path('add/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
   path('remove/<int:item_id>/', views.remove_from_cart, name='remove-from-cart'),

#urls for email related functions

path('activate/<uidb64>/<token>', views.activate, name='activate'),
]
