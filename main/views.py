import json
import requests
from random import randint

from django.http import HttpResponseNotFound
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import Boat, Notification, Fine, Owner, RemoveRequest
from .forms import UserForm, BoatForm


def send_sms(number, message):
    link = f"https://cdn.osg.uz/sms/?phone={number}&id=2342&message={message}"
    requests.get(link)


# User views
class UserMixin(AccessMixin):
    def handle_not_authenticated(self):
        return redirect("main:login")

    def handle_user_inspector(self):
        return redirect("main:inspector")

    def handle_not_activated(self):
        return redirect("main:activate_account")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_not_authenticated()

        if request.user.is_inspector:
            return self.handle_user_inspector()

        if not request.user.activated:
            return self.handle_not_activated()

        return super(UserMixin, self).dispatch(request, *args, **kwargs)


class UserView(UserMixin, View):
    login_url = "/login"

    def get_context_with_extra_data(self, context):
        unwatched_notifications_count = Notification.objects.filter(watched=False, owner=self.request.user).count()
        context["notifications_count"] = unwatched_notifications_count

        return context


class RegisterBoat(UserView):
    def get(self, request):
        form = BoatForm()

        print(request.user.activated)

        context = {
            "user": request.user,
            "form": form,
        }

        context = self.get_context_with_extra_data(context)

        return render(request, "main/boat_form.html", context)

    def post(self, request):
        form = BoatForm(request.POST, request.FILES)
        if form.is_valid():
            boat = form.save(commit=False)
            boat.owner = request.user
            boat.save()

            messages.add_message(request, messages.SUCCESS, "Ваше заявление принято и находится в очереди")
            return redirect("main:index")

        else:
            return redirect("main:index")


class UserBoatRequests(UserView):
    def get(self, request):
        notifications = list(Notification.objects.filter(owner=request.user).order_by("-pk")).copy()
        unwatched_notifications = Notification.objects.filter(owner=request.user, watched=False)

        context = self.get_context_with_extra_data({"notifications": notifications})

        for notification in unwatched_notifications:
            notification.watched = True
            notification.save()

        return render(request, "main/user_requests.html", context)


class UserBoats(UserView):
    def get(self, request):
        boats = Boat.objects.filter(owner=request.user)
        context = self.get_context_with_extra_data({"boats": boats})

        return render(request, "main/user_boats.html", context)


class UserFines(UserView):
    def get(self, request):
        fines = Fine.objects.filter(owner=request.user)
        context = self.get_context_with_extra_data({"fines": fines})

        return render(request, "main/user_fines.html", context)


class BoatRemoveRequest(UserView):
    def get(self, request, pk):
        return HttpResponseNotFound()

    def post(self, request, pk):
        boat = get_object_or_404(Boat, owner=request.user, pk=pk)

        if not RemoveRequest.objects.filter(boat=boat):
            reason = request.POST["reason"]
            ticket = request.FILES.get("ticket")

            remove_request = RemoveRequest(boat=boat, reason=reason, ticket=ticket)
            remove_request.save()

            messages.add_message(request, messages.SUCCESS, "Ваше заявление на снятие судна с учета отправлено!")

        else:
            messages.add_message(request, messages.WARNING, "Ваше заявление на снятие судна с учета уже отправлено!")

        return redirect("main:boats")


def logout_user(request):
    logout(request)
    return redirect("main:login")


class TechCheckView(UserView):
    title = ""

    def get(self, request, pk):
        if not request.user.is_authenticated:
            return redirect("main:login")

        if request.user.is_inspector:
            return redirect("main:inspector")

        boat = get_object_or_404(Boat, pk=pk)

        context = {
            "boat": boat,
            "title": self.title
        }

        context = self.get_context_with_extra_data(context)

        return render(request, "main/tech_check_template.html", context)


class FirstTechCheck(TechCheckView):
    title = "Первичный техосмотр"

    def post(self, request):
        return redirect("main:boats")


class YearTechCheck(TechCheckView):
    title = "Ежегодный техосмотр"

    def post(self, request):
        return redirect("main:boats")


class EditRequest(UserView):
    def get(self, request, pk):
        boat = get_object_or_404(Boat, owner=request.user, pk=pk)

        if boat.status == "looking":
            messages.add_message(request, messages.WARNING, "Вы не можете изменять заявления, которые находятся на "
                                                            "рассмотрении")
            return redirect("main:boat_requests")

        form = BoatForm(instance=boat)
        context = self.get_context_with_extra_data({"form": form})

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
class InspectorMixin(UserMixin):
    def handle_basic_user(self):
        return redirect("main:index")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_not_authenticated()

        if not request.user.is_inspector:
            return self.handle_basic_user()

        return super(AccessMixin, self).dispatch(request, *args, **kwargs)


class InspectorView(InspectorMixin, View):
    def get_context_with_extra_data(self, context):
        context['waiting_requests'] = Boat.objects.filter(status="wait").count()
        # TODO: add tech check requests
        # TODO: add remove requests
        return context


class Inspector(InspectorView):
    def get(self, request):
        waiting_requests = Boat.objects.filter(status="wait").order_by("-pk")
        context = self.get_context_with_extra_data({"requests": waiting_requests})

        return render(request, "main/inspector.html", context)


class InspectingRequests(InspectorView):
    def get(self, request):
        inspecting_boat_requests = Boat.objects.filter(status="looking").order_by("-pk")
        context = self.get_context_with_extra_data({"requests": inspecting_boat_requests})

        return render(request, "main/inspector_inspecting_requests.html", context)


class RequestRemove(InspectorView):
    def get(self, request):
        remove_boat_request = RemoveRequest.objects.all()
        context = self.get_context_with_extra_data({"requests": remove_boat_request})

        return render(request, "main/inspector_remove_requests.html", context)


class AddRequestsToLooking(InspectorView):
    def post(self, request):
        waiting_requests_ids = request.POST.getlist("request")

        for request_id in waiting_requests_ids:
            boat = Boat.objects.get(id=request_id)
            boat.change_status("looking")

        if waiting_requests_ids:
            messages.add_message(request, messages.SUCCESS, "Добавлено в 'рассматриваемые'")

        return redirect("main:inspector")


class RegistrationRequest(InspectorView):
    def get(self, request, pk):
        boat = get_object_or_404(Boat, pk=pk)
        form = BoatForm(instance=boat)

        context = self.get_context_with_extra_data({"form": form})

        return render(request, "main/registration_request.html", context)

    def post(self, request, pk):
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


class UserEdit(LoginRequiredMixin, View):
    template_name = "main/edit_user.html"

    def get(self, request):
        if request.user.activated:
            return redirect("main:index")

        form = UserForm(instance=request.user)

        context = {
            "form": form
        }

        return render(request, self.template_name, context)

    def post(self, request):
        if request.user.activated:
            return redirect("main:index")

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
