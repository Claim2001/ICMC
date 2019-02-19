from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import Owner, Boat
from .forms import UserForm, BoatForm


def index(request):
    if request.user.is_authenticated:
        if request.user.is_inspector:
            # redirect to inspector page
            return HttpResponse("Inspector!")

        boats = Boat.objects.filter(owner=request.user)

        context = {
            "user": request.user,
            "boats": boats
        }

        return render(request, "main/user.html", context)

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

        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password'])
            user.save()

            login(request, user)

            return redirect("main:index")

        messages.add_message(request, messages.INFO, "User with this email exists")
        return render(request, "main/signup.html", { "form": form })


class RegisterBoat(View):
    def get(self, request):
        if request.user.is_authenticated:
            form = BoatForm()
            return render(request, "main/register_boat.html", { "form": form })

        return redirect("main:login")

    def post(self, request):
        if request.user.is_authenticated:
            form = BoatForm(request.POST or None)
            if form.is_valid():
                boat = form.save(commit=False)
                boat.owner = request.user
                boat.save()
                
                return redirect("main:index")
        
        return redirect("main:login")
