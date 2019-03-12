import requests
from random import randint

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import Boat, Notification, Fine, Owner
from .forms import UserForm, BoatForm


def send_sms(number, message):
    link = f"https://cdn.osg.uz/sms/?phone={number}&id=2342&message={message}"
    requests.get(link)


class IndexView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_inspector:
                return redirect("main:inspector")

            if request.user.is_superuser:
                return HttpResponseRedirect("/admin")

            if request.user.activated is not True:
                return redirect("main:activate_account")

            form = BoatForm()

            context = {
                "user": request.user,
                "form": form
            }

            return render(request, "main/register_boat.html", context)

        return redirect("main:login")

    def post(self, request):
        if request.user.is_authenticated:
            form = BoatForm(request.POST, request.FILES)
            if form.is_valid():
                boat = form.save(commit=False)
                boat.owner = request.user
                boat.save()

                return redirect("main:boats")

            else:
                return redirect("main:index")

        return redirect("main:login")


def logout_user(request):
    logout(request)
    return redirect("main:login")


def inspector_page(request):
    if not request.user.is_authenticated:
        return redirect("main:login")

    if not request.user.is_inspector:
        return redirect("main:index")

    waiting_requests = Boat.objects.filter(status="wait")

    context = {
        "requests": waiting_requests
    }

    return render(request, "main/inspector.html", context)


def boat_request(request, pk):
    if not request.user.is_authenticated:
        return redirect("main:login")

    boat = get_object_or_404(Boat, pk=pk)

    if request.user.is_inspector:
        notification = Notification(owner=boat.owner, boat=boat, status=boat.status)
        notification.save()

        return render(request, "main/inspector_request.html", {"boat": boat})

    if not request.user.activated:
        return redirect("main:activate_account")

    return render(request, "main/request.html", {"request": boat})


def user_boat_requests(request):
    if not request.user.is_authenticated:
        return redirect("main:login")

    if not request.user.activated:
        return redirect("main:activate_account")

    notifications = Notification.objects.filter(owner=request.user)
    return render(request, "main/user_requests.html", {"notifications": notifications})


def user_boats(request):
    if not request.user.is_authenticated:
        return redirect("main:login")

    if not request.user.activated:
        return redirect("main:activate_account")

    boats = Boat.objects.filter(owner=request.user)
    return render(request, "main/user_boats.html", {"boats": boats})


def user_fines(request):
    if not request.user.is_authenticated:
        return redirect("main:login")

    if not request.user.activated:
        return redirect("main:activate_account")

    fines = Fine.objects.filter(owner=request.user)
    return render(request, "main/user_fines.html", {"fines": fines})


def reactivate(request):
    if not request.user.is_authenticated:
        return redirect("main:login")

    request.user.activation_code = randint(1000, 9999)
    request.user.save()

    send_sms(request.user.phone_number, str(request.user.activation_code))

    return redirect("main:activate_account")


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
            user.activation_code = randint(1000, 9999)
            user.save()

            login(request, user)

            send_sms(request.user.phone_number, str(request.user.activation_code))

            return redirect("main:activate_account")

        user_with_same_email = Owner.objects.filter(email=request.POST['email'])
        if user_with_same_email:
            messages.add_message(request, messages.INFO, "User with this email exists")
            return render(request, "main/signup.html", {"form": form})

        user_with_same_number = Owner.objects.filter(phone_number=request.POST['phone_number'])
        if user_with_same_number:
            messages.add_message(request, messages.INFO, "User with this phone number exists")
            return render(request, "main/signup.html", {"form": form})

        messages.add_message(request, messages.INFO, "Some error")
        return render(request, "main/signup.html", {"form": form})


class ActivateAccount(View):
    def get(self, request):
        if request.user.is_authenticated and not request.user.activated:
            return render(request, "main/activation.html", {})
        return redirect("main:index")

    def post(self, request):
        if request.user.is_authenticated:
            user_code = int(request.POST['activation_code'])

            if request.user.activation_code == user_code:
                user = Owner.objects.get(email=request.user.email)
                user.activated = True
                user.save()

                return redirect("main:index")

            messages.add_message(request, messages.ERROR, "Wrong code")
            return render(request, "main/activation.html", {})

        return redirect("main:login")


class RegisterBoat(View):
    def get(self, request):
        if not request.user.activated:
            return redirect("main:activate_account")

        if request.user.is_authenticated:
            return render(request, "main/register_boat.html", {})

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
