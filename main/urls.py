from django.urls import path

from . import views


app_name = "main"

urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.Login.as_view(), name="login"),
    path('signup', views.SignUp.as_view(), name="signup"),
    path('logout', views.logout_user, name="logout"),
    path('register', views.RegistrateBoat.as_view(), name="register"),
]