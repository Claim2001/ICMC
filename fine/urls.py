from django.urls import path
from . import views
app_name = "fine"


urlpatterns = [
    path('inspector/addFine/', views.AddFine.as_view(), name="add_fine"),
    path('inspector/finePayment/<int:pk>/accept/', views.AcceptFinePayment.as_view(), name="accept_fine"),
    path('inspector/finePayment/<int:pk>/reject/', views.RejectFinePayment.as_view(), name="reject_fine"),

]