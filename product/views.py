from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
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
        variation_id = self.request.GET.get('vid')

        if not variation_id:
            messages.error(
                self.request,
                'Invalid Product'
            )
            return redirect('product:list')

        variation = get_object_or_404(models.Variation, id=variation_id)

        if not self.request.session.get('cart'):
            self.request.session['cart'] = {}
            self.request.session.save()

        cart = self.request.session['cart']

        if variation_id in cart:
            ...
        else:
            ...

        return HttpResponse(f'{variation.product} {variation.name}')


class RemoveFromCart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('remove from cart')


class Cart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('cart')


class Checkout(View):
    def get(self, *args, **kwargs):
        return HttpResponse('checkout')
