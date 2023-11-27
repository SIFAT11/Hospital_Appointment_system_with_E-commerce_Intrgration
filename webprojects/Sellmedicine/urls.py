from django.urls import path
from .views import *

urlpatterns = [
    path('medicine/',medicine ,name='medicine'),
    path('add_to_cart/<int:id>/', add_to_cart, name='add_to_cart'),
    path('update_cart_item/<int:item_id>/', update_cart_item, name='update_cart_item'),
    path('cart/remove_from_cart/<int:id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/view_cart_items/', view_cart_items, name='view_cart_items'),
    
    
    path('creatOrder/',creatOrder, name='creatOrder'),
    path('cheak_out/',cheak_out, name='cheak_out'),
]
 