from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth import authenticate, login

from .models import Owner


def index(request):
    if request.user.is_authenticated:
        if request.user.is_inspector:
            # redirect to inpector page
            return HttpResponse("Inspector!")

        # redirect to user page
        return HttpResponse("Authenticated user!")

    return redirect("main:login")


class Login(View):
    def get(self, request):
        return render(request, "main/login.html", {})

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']

        user = Owner.objects.get(email=email)
        user_authenticated = authenticate(username=user.username, password=password)
        
        if user_authenticated is not None:
            login(request, user_authenticated)
            return redirect("main:index")
        
        return redirect("main:login")
