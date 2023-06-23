from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView


class ProductsList(ListView):
    def get(self, *args, **kwargs):
        return HttpResponse('ProductsList')


class Detail(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Detail')


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
