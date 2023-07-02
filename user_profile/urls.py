from django.urls import path

from user_profile import views

app_name = 'user_profile'

urlpatterns = [
    path('', views.Create.as_view(), name="create"),
    path('login/', views.Login.as_view(), name="login"),
    path('logout/', views.Logout.as_view(), name="logout"),
]
