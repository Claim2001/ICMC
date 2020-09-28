from django.urls import path
from . import views
app_name = "notification"


urlpatterns = [
    path('requests/', views.UserBoatRequests.as_view(), name="boat_requests"),
    path('requests/<int:pk>/remove/', views.BoatRemoveRequest.as_view(), name="remove_boat"),
    path('ships/', views.UserBoats.as_view(), name="boats"),
    path('fines/', views.UserFines.as_view(), name="fines"),
    path('requests/<int:pk>/techCheck/', views.FirstTechCheck.as_view(), name="tech_check"),
    path('requests/<int:pk>/yearTechCheck/', views.YearTechCheck.as_view(), name="year_tech_check"),
    path('requests/<int:pk>/techCheck/', views.FirstTechCheck.as_view(), name="first_tech_check"),
    path('requests/<int:pk>/pay/', views.PayRequest.as_view(), name="request_pay"),
    path('fines/<int:pk>/pay/', views.PayFine.as_view(), name="fine_pay"),

]