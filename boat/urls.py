from django.urls import path
from main.decorators import check_recaptcha
from . import views
app_name = "boat"


urlpatterns = [
    path('', check_recaptcha(views.RegisterBoat.as_view()), name="index"),
    path('register/', views.RegisterBoat.as_view(), name="register"),
    path('requests/<int:pk>/edit/', check_recaptcha(views.EditRequest.as_view()), name="edit_request"),
    path('requests/<int:pk>/', views.RegistrationRequest.as_view(), name="register_request"),
    path('inspector/requests/<int:pk>/finalcheck/', views.FinalBoatCheck.as_view(), name="final_boat_check"),
    path('inspector/boats/<int:pk>/', views.InspectorBoat.as_view(), name="inspector_boat"),

]