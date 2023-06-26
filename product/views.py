from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from product import models


class ProductsList(ListView):
    model = models.Product
    template_name = 'product/list.html'
    context_object_name = 'products'
    paginate_by = 9


class Detail(DetailView):
    model = models.Product
    template_name = 'product/detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'


class AddToCart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('add to cart')


class RemoveFromCart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('remove from cart')


class Cart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('cart')


class Checkout(View):
    def get(self, *args, **kwargs):
        return HttpResponse('checkout')
