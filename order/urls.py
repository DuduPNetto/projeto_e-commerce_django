from django.urls import path

from order import views

app_name = 'order'

urlpatterns = [
    path('', views.Pay.as_view(), name="pay"),
    path('save/', views.SaveOrder.as_view(), name="save"),
    path('detail/', views.Detail.as_view(), name="detail"),
]
