from django.urls import path
from .views import *

urlpatterns = [
    path('', store, name='store'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('update_item/', update_item, name='update_item'),
    path('registration/', register_user, name='registration'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('show_post/<slug:post_slug>/', show_post, name='show_post'),
    path('show_categories/<slug:cat_slug>/', show_category, name='cats'),
    path('show_cats_list/', show_cats_list, name='show_cats_list'),
    path('add_product/', add_product, name='add_product'),
    path('search/', Search.as_view(), name='search')
]



