from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView
from .forms import *
from .models import *
from django.http import JsonResponse, HttpResponse
import json

from .utils import DataMixin


# Create your views here.


def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    context = {
        'products': products,
        'cartItems': cartItems,
    }
    return render(request, 'store/store.html', context=context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {
            'get_cart_total': 0,
            'get_cart_items': 0
        }
        cartItems = order['get_cart_items']

    context = {'items': items,
               'order': order,
               'cartItems': cartItems
               }
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {
            'get_cart_total': 0,
            'get_cart_items': 0
        }
    context = {'items': items,
               'order': order}
    return render(request, 'store/checkout.html', context)


def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added!', safe=False)


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'store/register.html'
    success_url = reverse_lazy('store')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="NameSite")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('store')


class LoginUser(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'store/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="NameSite")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('store')


def logout_user(request):
    logout(request)
    return redirect('store')


def show_post(request, post_slug):
    product = get_object_or_404(Product, slug=post_slug)
    context = {
        'product': product
    }
    return render(request, 'store/show_post.html', context=context)


def show_category(request, cat_slug):
    products = Product.objects.filter(cat__slug= cat_slug)

    context = {
        'title': 'Отображение по рубрикам',
        'products': products,
        }

    return render(request, 'store/store.html', context=context)


def show_cats_list(request):
    cats = Category.objects.all()
    context = {'cats': cats}
    return render(request, 'store/show_cats_list.html', context=context)


# class ProductCategories(DataMixin, ListView):
#     model = Product
#     template_name = 'store/main.html'
#     context_object_name = 'products'
#     allow_empty = False
#
#     def get_queryset(self):
#         return Product.objects.filter(cat__slug=self.kwargs['cat_slug'])
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title=" NameSite")
#         return dict(list(context.items()) + list(c_def.items()))


