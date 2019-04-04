from django.urls import path

from . import views


app_name = "main"

urlpatterns = [
    path('', views.RegisterBoat.as_view(), name="index"),
    path('login/', views.Login.as_view(), name="login"),
    path('signup/', views.SignUp.as_view(), name="signup"),
    path('edit/', views.UserEdit.as_view(), name="user_edit"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.RegisterBoat.as_view(), name="register"),
    path('inspector/', views.Inspector.as_view(), name="inspector"),
    path('requests/<int:pk>/', views.RegistrationRequest.as_view(), name="register_request"),
    path('requests/<int:pk>/remove/', views.BoatRemoveRequest.as_view(), name="remove_boat"),
    path('requests/<int:pk>/edit/', views.EditRequest.as_view(), name="edit_request"),
    path('requests/<int:pk>/techCheck/', views.FirstTechCheck.as_view(), name="tech_check"),
    path('requests/<int:pk>/yearTechCheck/', views.YearTechCheck.as_view(), name="year_tech_check"),
    path('requests/<int:pk>/pay/', views.PayRequest.as_view(), name="request_pay"),
    path('requests/', views.UserBoatRequests.as_view(), name="boat_requests"),
    path('ships/', views.UserBoats.as_view(), name="boats"),
    path('fines/', views.UserFines.as_view(), name="fines"),
    path('activate/', views.ActivateAccount.as_view(), name="activate_account"),
    path('reactivate/', views.reactivate, name="reactivate"),
    path('inspector/request/looking/', views.AddRequestsToLooking.as_view(), name="add_looking_request"),
    path('inspector/inspectingRequests/', views.InspectingRequests.as_view(), name="inspecting_requests"),
    path('inspector/removeRequests/', views.RequestRemove.as_view(), name="remove_requests"),
    path('inspector/payments/', views.PaymentRequests.as_view(), name="payment_requests"),
    path('inspector/payments/<int:pk>/accept/', views.AcceptPayment.as_view(), name="accept_payment"),
    path('inspector/payments/<int:pk>/reject/', views.RejectPayment.as_view(), name="reject_payment"),
]
