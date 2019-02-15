from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout

from .models import Owner
from .forms import UserForm


def index(request):
    if request.user.is_authenticated:
        if request.user.is_inspector:
            # redirect to inspector page
            return HttpResponse("Inspector!")

        # redirect to user page
        return render(request, "main/user.html", { "user": request.user })

    return redirect("main:login")


def logout_user(request):
    logout(request)
    return redirect("main:login")


class Login(View):
    def get(self, request):
        return render(request, "main/login.html", {})

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']

        authenticated_user = authenticate(username=email, password=password)
        
        if authenticated_user:
            login(request, authenticated_user)
            return redirect("main:index")
        
        return redirect("main:login")


class SignUp(View):
    def get(self, request):
        form = UserForm()
        return render(request, "main/signup.html", { "form": form })

    def post(self, request):
        form = UserForm(request.POST)

        if form.is_valid:
            user = form.save(commit=False)
            user.username = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password'])
            user.save()

            login(request, user)

            return redirect("main:index")
