from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import Boat
from .forms import UserForm, BoatForm


def index(request):
    if request.user.is_authenticated:
        if request.user.is_inspector:
            return redirect("main:inspector")

        if request.user.is_superuser:
            return HttpResponseRedirect("/admin")

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


def inspector_page(request):
    if not request.user.is_authenticated:
        return redirect("main:login")

    waiting_requests = Boat.objects.filter(status="wait")

    context = {
        "requests": waiting_requests
    }

    return render(request, "main/inspector.html", context)


def boat_request(request, pk):
    if not request.user.is_authenticated:
        return redirect("main:login")

    boat_request = get_object_or_404(Boat, pk=pk)
    return render(request, "main/request.html", {"request": boat_request})


def user_boat_requests(request):
    if not request.user.is_authenticated:
        return redirect("main:login")

    boats = Boat.objects.filter(owner=request.user)
    return render(request, "main/user_requests.html", {"boats": boats})


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
        
        messages.add_message(request, messages.ERROR, "Login or password is wrong")
        return redirect("main:login")


class SignUp(View):
    def get(self, request):
        form = UserForm()
        return render(request, "main/signup.html", {"form": form})

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
        return render(request, "main/signup.html", {"form": form})


class RegisterBoat(View):
    def get(self, request):
        if request.user.is_authenticated:
            form = BoatForm()
            return render(request, "main/register_boat.html", {"form": form})

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
