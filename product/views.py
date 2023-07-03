from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from product import models
from user_profile import models as up_models


class ProductsList(ListView):
    model = models.Product
    template_name = 'product/list.html'
    context_object_name = 'products'
    paginate_by = 1
    ordering = 'id'


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
        product = variation.product

        variation_stock = variation.stock

        product_id = product.pk
        product_name = product.name
        variation_name = variation.name or ''
        unitary_price = variation.price
        promotional_unitary_price = variation.promotional_price
        quantity = 1
        slug = product.slug
        image = product.image

        if image:
            image = image.name
        else:
            image = ''

        if variation.stock < 1:
            messages.error(self.request, 'Stock Insufficient')
            return redirect('product:list')

        if not self.request.session.get('cart'):
            self.request.session['cart'] = {}
            self.request.session.save()

        cart = self.request.session['cart']

        if variation_id in cart:
            quantity_cart = cart[variation_id]['quantity']
            quantity_cart += 1

            if variation_stock < quantity_cart:
                messages.warning(
                    self.request,
                    f'Stock Insufficient for {quantity_cart}x of product {product_name}'
                )

            cart[variation_id]['quantity'] = quantity_cart
            cart[variation_id]['quantity_price'] = (
                unitary_price * quantity_cart)
            cart[variation_id]['quantity_promotional_price'] = (
                promotional_unitary_price * quantity_cart)
        else:
            cart[variation_id] = {
                'product_id': product_id,
                'product_name': product_name,
                'variation_id': variation_id,
                'variation_name': variation_name,
                'unitary_price': unitary_price,
                'promotional_unitary_price': promotional_unitary_price,
                'quantity': quantity,
                'slug': slug,
                'image': image,
            }

        self.request.session.save()

        messages.success(
            self.request, f'Product {product_name} add into the cart')

        return redirect('product:list')


class RemoveFromCart(View):
    def get(self, *args, **kwargs):
        variation_id = self.request.GET.get('vid')

        if not variation_id:
            return redirect('product:list')

        if not self.request.session.get('cart'):
            return redirect('product:list')

        if variation_id not in self.request.session['cart']:
            return redirect('product:list')

        cart = self.request.session['cart'][variation_id]

        messages.success(
            self.request,
            f'Product {cart["product_name"]} {cart["variation_name"]} removed.'
        )

        del self.request.session['cart'][variation_id]
        self.request.session.save()

        return redirect('product:cart')


class Cart(View):
    def get(self, *args, **kwargs):
        context = {
            'cart': self.request.session.get('cart', {})
        }

        return render(self.request, 'product/cart.html', context)


class Checkout(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('user_profile:create')

        profile = up_models.UserProfile.objects.filter(
            user=self.request.user).exists()

        if not profile:
            messages.error(
                self.request,
                'User has not profile.'
            )
            return redirect('user_profile:create')

        if not self.request.session.get('cart'):
            messages.error(
                self.request,
                'Empty cart.'
            )
            return redirect('product:list')

        context = {
            'user': self.request.user,
            'cart': self.request.session['cart']
        }

        return render(self.request, 'product/checkout.html', context)
