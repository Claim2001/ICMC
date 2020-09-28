from django.urls import path
from . import views
app_name = "owner"


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name="signup"),
    path('edit/', views.UserEdit.as_view(), name="user_edit"),

]