import requests
from random import randint

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import Boat, Notification, Fine, Owner, RemoveRequest
from .forms import UserForm, BoatForm

# TODO: add admin check everywhere


def send_sms(number, message):
    link = f"https://cdn.osg.uz/sms/?phone={number}&id=2342&message={message}"
    requests.get(link)


class RegisterBoat(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_inspector:
                return redirect("main:inspector")

            if request.user.is_superuser:
                return HttpResponseRedirect("/admin")

            if request.user.activated is not True:
                return redirect("main:activate_account")

            form = BoatForm()
            unwatched_notifications_count = len(Notification.objects.filter(owner=request.user, watched=False))

            context = {
                "user": request.user,
                "form": form,
                "notifications_count": unwatched_notifications_count,
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

                messages.add_message(request, messages.SUCCESS, "Ваше заявление принято и находится в очереди")
                return redirect("main:index")

            else:
                return redirect("main:index")

        return redirect("main:login")


def logout_user(request):
    logout(request)
    return redirect("main:login")


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

    if request.user.is_superuser:
        return redirect("main:index")

    if not request.user.activated:
        return redirect("main:activate_account")

    notifications = list(Notification.objects.filter(owner=request.user)).copy()
    unwatched_notifications = Notification.objects.filter(owner=request.user, watched=False)

    context = {
        "notifications": notifications,
        "notifications_count": len(unwatched_notifications),
    }

    for notification in unwatched_notifications:
        notification.watched = True
        notification.save()

    return render(request, "main/user_requests.html", context)


def user_boats(request):
    if not request.user.is_authenticated:
        return redirect("main:login")

    if request.user.is_superuser:
        return redirect("main:index")

    if not request.user.activated:
        return redirect("main:activate_account")

    unwatched_notifications_count = len(Notification.objects.filter(owner=request.user, watched=False))
    boats = Boat.objects.filter(owner=request.user)

    context = {
        "boats": boats,
        "notifications_count": unwatched_notifications_count
    }

    return render(request, "main/user_boats.html", context)


def make_remove_boat_request(request, pk):
    if not request.user.is_authenticated:
        return redirect("main:login")

    if request.user.is_superuser:
        return redirect("main:index")

    if not request.user.activated:
        return redirect("main:activate_account")

    boat = get_object_or_404(Boat, owner=request.user, pk=pk)

    if not RemoveRequest.objects.filter(boat=boat):
        remove_request = RemoveRequest(boat=boat, reason="broke")
        remove_request.save()

        messages.add_message(request, messages.SUCCESS, "Ваше заявление на снятие судна с учета отправлено!")

    else:
        messages.add_message(request, messages.WARNING, "Ваше заявление на снятие судна с учета уже отправлено!")

    return redirect("main:boats")


def user_fines(request):
    if not request.user.is_authenticated:
        return redirect("main:login")

    if request.user.is_superuser:
        return redirect("main:index")

    if not request.user.activated:
        return redirect("main:activate_account")

    unwatched_notifications_count = len(Notification.objects.filter(owner=request.user, watched=False))
    fines = Fine.objects.filter(owner=request.user)

    context = {
        "fines": fines,
        "notifications_count": unwatched_notifications_count,
    }

    return render(request, "main/user_fines.html", context)


def inspector_page(request):
    if not request.user.is_authenticated:
        return redirect("main:login")

    if request.user.is_superuser:
        return redirect("main:index")

    if not request.user.is_inspector:
        return redirect("main:index")

    waiting_requests = Boat.objects.filter(status="wait").order_by("-pk")
    print(waiting_requests)

    context = {
        "requests": waiting_requests
    }

    return render(request, "main/inspector.html", context)


def inspecting_requests(request):
    if not request.user.is_authenticated:
        return redirect("main:login")

    if request.user.is_superuser:
        return redirect("main:index")

    if not request.user.is_inspector:
        return redirect("main:index")

    inspecting_boat_requests = Boat.objects.filter(status="looking").order_by("-pk")

    context = {
        "requests": inspecting_boat_requests,
    }

    return render(request, "main/inspector_inspecting_requests.html", context)


def remove_requests(request):
    if not request.user.is_authenticated:
        return redirect("main:login")

    if request.user.is_superuser:
        return redirect("main:index")

    if not request.user.is_inspector:
        return redirect("")

    requests = RemoveRequest.objects.all()

    context = {
        "requests": requests
    }

    return render(request, "main/inspector_remove_requests.html", context)


def add_request_to_looking(request, pk):
    if not request.user.is_authenticated:
        return redirect("main:login")

    if request.user.is_superuser:
        return redirect("main:index")

    if not request.user.is_inspector:
        return redirect("main:index")

    # TODO: refactor this code: every time we change status of a boat we gotta send a notification
    # TODO: so we can just write a function what will change status and send notifications to the user
    boat = get_object_or_404(Boat, pk=pk)

    if boat.status is not "looking":
        boat.status = "looking"
        boat.save()

        notification = Notification(owner=boat.owner, boat=boat, status=boat.status)
        notification.save()

    return redirect("main:inspector")


def reactivate(request):
    if not request.user.is_authenticated:
        return redirect("main:login")

    request.user.activation_code = randint(1000, 9999)
    request.user.save()

    send_sms(request.user.phone_number, message=str(request.user.activation_code))

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

            send_sms(request.user.phone_number, message=str(request.user.activation_code))

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
