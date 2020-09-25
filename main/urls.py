from django.urls import path
from .decorators import check_recaptcha
from . import views

app_name = "main"


urlpatterns = [
    path('', views.RegisterBoat.as_view(), name="index"),
    path('login/', views.Login.as_view(), name="login"),
    path('signup/', check_recaptcha(views.SignUp.as_view()), name="signup"),
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
    path('requests/<int:pk>/techCheck/', views.FirstTechCheck.as_view(), name="first_tech_check"),
    path('requests/<int:pk>/yearTechCheck/', views.YearTechCheck.as_view(), name="year_tech_check"),
    path('requests/', views.UserBoatRequests.as_view(), name="boat_requests"),
    path('ships/', views.UserBoats.as_view(), name="boats"),
    path('fines/', views.UserFines.as_view(), name="fines"),
    path('fines/<int:pk>/pay/', views.PayFine.as_view(), name="fine_pay"),
    path('activate/', views.ActivateAccount.as_view(), name="activate_account"),
    path('reactivate/', views.reactivate, name="reactivate"),
    path('inspector/request/looking/', views.AddRequestsToLooking.as_view(), name="add_looking_request"),
    path('inspector/inspectingRequests/', views.InspectingRequests.as_view(), name="inspecting_requests"),
    path('inspector/removeRequests/', views.RequestRemove.as_view(), name="remove_requests"),
    path('inspector/removeRequests/<int:pk>/accept/', views.AcceptRemoveRequest.as_view(),
         name="accept_remove_request"),
    path('inspector/payments/', views.PaymentRequests.as_view(), name="payment_requests"),
    path('inspector/payments/<int:pk>/accept/', views.AcceptPayment.as_view(), name="accept_payment"),
    path('inspector/payments/<int:pk>/reject/', views.RejectPayment.as_view(), name="reject_payment"),
    path('inspector/requests/payed/', views.PayedRequests.as_view(), name="payed_requests"),
    path('inspector/requests/<int:pk>/accept/', views.AcceptBoat.as_view(), name="accept_boat"),
    path('inspector/requests/<int:pk>/finalcheck/', views.FinalBoatCheck.as_view(), name="final_boat_check"),
    path('inspector/addFine/', views.AddFine.as_view(), name="add_fine"),
    path('inspector/finePayment/<int:pk>/accept/', views.AcceptFinePayment.as_view(), name="accept_fine"),
    path('inspector/finePayment/<int:pk>/reject/', views.RejectFinePayment.as_view(), name="reject_fine"),
    path('inspector/techCheckPayment/<int:pk>/accept/', views.AcceptTechCheckPayment.as_view(),
         name="accept_tech_check"),
    path('inspector/techCheckPayment/<int:pk>/reject/', views.RejectTechCheckPayment.as_view(),
         name="reject_tech_check"),
    path('inspector/boats/all/', views.AllBoats.as_view(), name="all_boats"),
    path('inspector/boats/<int:pk>/', views.InspectorBoat.as_view(), name="inspector_boat"),
    path('public_offer/', views.Public_offer.as_view(), name="public_offer")

]
