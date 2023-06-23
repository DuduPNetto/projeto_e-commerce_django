from django.urls import path

from order import views

app_name = 'order'

urlpatterns = [
    path('', views.Pay.as_view(), name="pay"),
    path('close/', views.CloseOrder.as_view(), name="close"),
    path('detail/', views.Detail.as_view(), name="detail"),
]
