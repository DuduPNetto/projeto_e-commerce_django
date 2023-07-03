from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView

from order.models import Order, OrderItem
from product import models
from utils.cart_total import cart_total_qtt, cart_totals


class DispatchLoginRequiredMixin(View):
    def dispatch(self, *args, **kwargs):

        if not self.request.user.is_authenticated:
            return redirect('user_profile:create')

        return super().dispatch(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(user=self.request.user)
        return qs


class Pay(DispatchLoginRequiredMixin, DetailView):
    template_name = 'order/pay.html'
    model = Order
    pk_url_kwarg = 'pk'
    context_object_name = 'order'


class SaveOrder(View):
    def get(self, *args, **kwargs):

        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                'Please login.'
            )
            return redirect('user_profile:create')

        if not self.request.session.get('cart'):
            messages.error(
                self.request,
                'Empty cart.'
            )
            return redirect('user_profile:create')

        cart = self.request.session.get('cart')
        cart_variations_ids = [i for i in cart]

        db_variations = list(models.Variation.objects.select_related('product')
                             .filter(id__in=cart_variations_ids))

        for variation in db_variations:
            vid = str(variation.pk)
            stock = variation.stock
            quantity_cart = cart[vid]['quantity']
            unitary_price = cart[vid]['unitary_price']
            promo_unitary_price = cart[vid]['promotional_unitary_price']

            error_msg_stock = ''

            if stock < quantity_cart:
                cart[vid]['quantity'] = stock
                cart[vid]['unitary_price'] = stock * unitary_price
                cart[vid]['promotional_unitary_price'] = stock * \
                    promo_unitary_price

                error_msg_stock = 'Insufficient stock for some products. Please verify it.'

            if error_msg_stock:
                messages.error(
                    self.request,
                    error_msg_stock
                )

                self.request.session.save()

                return redirect('product:cart')

        quantity_total_cart = cart_total_qtt(cart)
        total_value_cart = cart_totals(cart)

        order = Order(
            user=self.request.user, total=total_value_cart,
            quantity_total=quantity_total_cart, status='C'
        )

        order.save()

        OrderItem.objects.bulk_create(
            [
                OrderItem(
                    order=order,
                    product=item['product_name'],
                    product_id=item['product_id'],
                    variation=item['variation_name'],
                    variation_id=item['variation_id'],
                    price=item['unitary_price'],
                    promotional_price=item['promotional_unitary_price'],
                    quantity=item['quantity'],
                    image=item['image']
                ) for item in cart.values()
            ]
        )

        del self.request.session['cart']
        self.request.session.save()

        return redirect(
            reverse(
                'order:pay', kwargs={'pk': order.pk}
            )
        )


class Detail(DispatchLoginRequiredMixin, DetailView):
    model = Order
    context_object_name = 'order'
    template_name = 'order/detail.html'
    pk_url_kwarg = 'pk'


class ListOrder(DispatchLoginRequiredMixin, ListView):
    model = Order
    context_object_name = 'orders'
    template_name = 'order/list.html'
    paginate_by = 9
    ordering = ['-id']
