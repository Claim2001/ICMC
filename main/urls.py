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
    path('inspector/', views.inspector_page, name="inspector"),
    path('requests/<int:pk>/', views.RegistrationRequest.as_view(), name="register_request"),
    path('requests/<int:pk>/remove/', views.make_remove_boat_request, name="remove_boat"),
    path('requests/<int:pk>/edit/', views.EditRequest.as_view(), name="edit_request"),
    path('requests/<int:pk>/techCheck/', views. FirstTechCheck.as_view(), name="tech_check"),
    path('requests/<int:pk>/yearTechCheck/', views.YearTechCheck.as_view(), name="year_tech_check"),
    path('requests/', views.user_boat_requests, name="boat_requests"),
    path('ships/', views.user_boats, name="boats"),
    path('fines/', views.user_fines, name="fines"),
    path('activate/', views.ActivateAccount.as_view(), name="activate_account"),
    path('reactivate/', views.reactivate, name="reactivate"),
    path('inspector/request/<int:pk>/looking/', views.add_request_to_looking, name="add_looking_request"),
    path('inspector/inspectingRequests/', views.inspecting_requests, name="inspecting_requests"),
    path('inspector/removeRequests/', views.remove_requests, name="remove_requests"),
]
