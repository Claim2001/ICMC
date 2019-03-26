import json
import requests
from random import randint

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import Boat, Notification, Fine, Owner, RemoveRequest
from .forms import UserForm, BoatForm


def send_sms(number, message):
    link = f"https://cdn.osg.uz/sms/?phone={number}&id=2342&message={message}"
    requests.get(link)


# User views

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

            return render(request, "main/boat_form.html", context)

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


def user_boat_requests(request):
    if not request.user.is_authenticated:
        return redirect("main:login")

    if request.user.is_superuser:
        return redirect("main:index")

    if not request.user.activated:
        return redirect("main:activate_account")

    notifications = list(Notification.objects.filter(owner=request.user).order_by("-pk")).copy()
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


def logout_user(request):
    logout(request)
    return redirect("main:login")


class TechCheckView(View):
    title = ""

    def get(self, request, pk):
        if not request.user.is_authenticated:
            return redirect("main:login")

        if request.user.is_inspector:
            return redirect("main:inspector")

        boat = get_object_or_404(Boat, pk=pk)
        unwatched_notifications_count = len(Notification.objects.filter(owner=request.user, watched=False))

        context = {
            "boat": boat,
            "notifications_count": unwatched_notifications_count,
            "title": self.title
        }

        return render(request, "main/tech_check_template.html", context)


class FirstTechCheck(TechCheckView):
    title = "Первичный техосмотр"

    def post(self, request):
        return redirect("main:boats")


class YearTechCheck(TechCheckView):
    title = "Ежегодный техосмотр"

    def post(self, request):
        return redirect("main:boats")


class EditRequest(LoginRequiredMixin, View):
    login_url = "main:login"

    def get(self, request, pk):
        boat = get_object_or_404(Boat, owner=request.user, pk=pk)

        if boat.status == "looking":
            messages.add_message(request, messages.WARNING, "Вы не можете изменять заявления, которые находятся на "
                                                            "рассмотрении")
            return redirect("main:boat_requests")

        form = BoatForm(instance=boat)

        notification_count = Notification.objects.filter(owner=request.user, watched=False)

        context = {
            "notifications_count": notification_count,
            "form": form,
        }

        return render(request, "main/boat_form.html", context)

    def post(self, request, pk):
        boat = get_object_or_404(Boat, owner=request.user, pk=pk)
        form = BoatForm(request.POST, request.FILES, instance=boat)

        if form.is_valid():
            edited_boat = form.save(commit=False)
            edited_boat.change_status("wait")
            edited_boat.save()

            messages.add_message(request, messages.SUCCESS, "Ваше заявление принято и повторно отправлено!")
        else:
            messages.add_message(request, messages.ERROR, "Что-то пошло не так")

        return redirect("main:boat_requests")


# Inspector views

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

    remove_boat_request = RemoveRequest.objects.all()

    context = {
        "requests": remove_boat_request
    }

    return render(request, "main/inspector_remove_requests.html", context)


def add_request_to_looking(request, pk):
    if not request.user.is_authenticated:
        return redirect("main:login")

    if request.user.is_superuser:
        return redirect("main:index")

    if not request.user.is_inspector:
        return redirect("main:index")

    boat = get_object_or_404(Boat, pk=pk)
    boat.change_status("looking")

    messages.add_message(request, messages.SUCCESS, "Добавлено в 'рассматриваемые'")
    return redirect("main:inspector")


class RegistrationRequest(View):
    def get(self, request, pk):
        if not request.user.is_authenticated:
            return redirect("main:login")

        if not request.user.is_inspector:
            return redirect("main:index")

        boat = get_object_or_404(Boat, pk=pk)
        form = BoatForm(instance=boat)

        return render(request, "main/registration_request.html", {"form": form})

    def post(self, request, pk):
        if not request.user.is_authenticated:
            return redirect("main:login")

        if not request.user.is_inspector:
            return redirect("main:index")

        incorrect_fields = request.POST.getlist("incorrect_fields")
        incorrect_fields_json = json.dumps(incorrect_fields)

        boat = get_object_or_404(Boat, pk=pk)
        boat.incorrect_fields = incorrect_fields_json
        boat.save()

        status = "payment"

        if incorrect_fields:
            status = "rejected"

        boat.change_status(status)

        return redirect("main:inspecting_requests")


# Login, signup and etc.

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

        messages.add_message(request, messages.ERROR, "Неверный email или пароль")
        return render(request, "main/login.html", {"email": email})


class SignUp(View):
    template_name = "main/signup.html"

    def get(self, request):
        form = UserForm()
        return render(request, self.template_name, {"form": form})

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
            messages.add_message(request, messages.ERROR, "User with this email exists")
            return render(request, self.template_name, {"form": form})

        user_with_same_number = Owner.objects.filter(phone_number=request.POST['phone_number'])
        if user_with_same_number:
            messages.add_message(request, messages.ERROR, "User with this phone number exists")
            return render(request, self.template_name, {"form": form})

        messages.add_message(request, messages.ERROR, "Some error")
        return render(request, self.template_name, {"form": form})


class UserEdit(View):
    template_name = "main/edit_user.html"

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("main:login")

        if request.user.activated:
            return redirect("main:index")

        form = UserForm(instance=request.user)

        context = {
            "form": form
        }

        return render(request, self.template_name, context)

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect("main:login")

        form = UserForm(request.POST, instance=request.user)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.activation_code = randint(1000, 9999)
            user.save()

            login(request, user)

            send_sms(request.user.phone_number, message=str(request.user.activation_code))

            return redirect("main:activate_account")

        user_with_same_email = Owner.objects.filter(email=request.POST['email'])
        if user_with_same_email is not request.user:
            messages.add_message(request, messages.ERROR, "User with this email exists")
            return render(request, self.template_name, {"form": form})

        user_with_same_number = Owner.objects.filter(phone_number=request.POST['phone_number'])
        if user_with_same_number is not request.user:
            messages.add_message(request, messages.ERROR, "User with this phone number exists")
            return render(request, self.template_name, {"form": form})

        messages.add_message(request, messages.ERROR, "Some error")
        return render(request, self.template_name, {"form": form})


class ActivateAccount(View):
    def get(self, request):
        if request.user.is_authenticated and not request.user.activated:
            if request.user.is_inspector:
                return redirect("main:inspector")

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


def reactivate(request):
    if not request.user.is_authenticated:
        return redirect("main:login")

    request.user.activation_code = randint(1000, 9999)
    request.user.save()

    send_sms(request.user.phone_number, message=str(request.user.activation_code))

    return redirect("main:activate_account")
