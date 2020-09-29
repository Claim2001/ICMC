from django.urls import path
from addrequestions.decorators import check_recaptcha
from addrequestions import views

app_name = "addrequestions"


urlpatterns = [
    path('login/', views.Login.as_view(), name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('inspector/', views.Inspector.as_view(), name="inspector"),
    path('activate/', check_recaptcha(views.ActivateAccount.as_view()), name="activate_account"),
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
    path('inspector/techCheckPayment/<int:pk>/accept/', views.AcceptTechCheckPayment.as_view(),
         name="accept_tech_check"),
    path('inspector/techCheckPayment/<int:pk>/reject/', views.RejectTechCheckPayment.as_view(),
         name="reject_tech_check"),
    path('inspector/boats/all/', views.AllBoats.as_view(), name="all_boats"),
    path('public_offer/', views.Public_offer.as_view(), name="public_offer")

]
