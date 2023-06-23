from django.urls import path

from product import views

app_name = 'product'

urlpatterns = [
    path('', views.ProductsList.as_view(), name="list"),
    path('<slug>', views.Detail.as_view(), name="detail"),
    path('add/', views.AddToCart.as_view(), name="add"),
    path('remove/', views.RemoveFromCart.as_view(), name="remove"),
    path('cart/', views.Cart.as_view(), name="cart"),
    path('checkout/', views.Checkout.as_view(), name="checkout")
]
