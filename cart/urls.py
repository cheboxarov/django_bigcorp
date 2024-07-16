from django.urls import path
from .views import cart_view, cart_add

app_name = 'cart'

urlpatterns = [
    path('', cart_view, name='cart-view'),
    path('delete/', cart_view, name='delete-to-cart'),
    path('delete/', cart_view, name='update-to-cart'),
    path('add/', cart_add, name='add-to-cart'),
]