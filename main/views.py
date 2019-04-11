import json
import requests
from random import randint

from django.http import HttpResponseNotFound
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Value as V
from django.db.models.functions import Concat

from . import models
from .models import Boat, Notification, Fine, Owner, RemoveRequest, TechCheckRequest, PaymentRequest, FinePaymentRequest
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

    def handle_user_admin(self):
        return redirect("/admin")

    def handle_not_activated(self):
        return redirect("main:activate_account")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_not_authenticated()

        if request.user.is_inspector:
            return self.handle_user_inspector()

        if request.user.is_superuser:
            return self.handle_user_admin()

        if not request.user.activated:
            return self.handle_not_activated()

        return super(UserMixin, self).dispatch(request, *args, **kwargs)


class UserView(UserMixin, View):
    login_url = "/login"

    def get_context_with_extra_data(self, context):
        context["notifications_count"] = Notification.objects.filter(watched=False, owner=self.request.user).count()
        context["fines_count"] = Fine.objects.filter(owner=self.request.user, payed=False, inspecting=False).count()

        return context


class RegisterBoat(UserView):
    def get(self, request):
        form = BoatForm()

        context = {
            "user": request.user,
            "form": form
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

        messages.add_message(request, messages.WARNING, "Произошла какая-то ошибка")
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
        boats = Boat.objects.filter(owner=request.user, status="accepted")
        context = self.get_context_with_extra_data({"boats": boats})

        return render(request, "main/user_boats.html", context)


class UserFines(UserView):
    def get(self, request):
        fines = Fine.objects.filter(owner=request.user, payed=False, inspecting=False)
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
    type = ""

    def post(self, request, pk):
        boat = get_object_or_404(Boat, pk=pk)

        if boat.status != "accepted":
            messages.add_message(request, messages.WARNING, "Судно еще не зарегистрировано в системе")
            return redirect("main:boats")

        if TechCheckRequest.objects.filter(boat=boat, check_type=self.type, inspecting=True):
            messages.add_message(request, messages.WARNING, "Заявление на техосмотр уже находится в очереди")
            return redirect("main:boats")

        tech_check_request = TechCheckRequest(owner=boat.owner, boat=boat, check_scan=request.FILES['checkScan'],
                                              check_type=self.type)
        tech_check_request.save()

        messages.add_message(request, messages.SUCCESS, "Заявление на техосмотр принято и находится в очереди")
        return redirect("main:boats")


class FirstTechCheck(TechCheckView):
    type = "first"


class YearTechCheck(TechCheckView):
    type = "year"


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


class PayRequest(UserView):
    def post(self, request, pk):
        boat = get_object_or_404(Boat, pk=pk)

        if boat.status != "payment":
            message = "Запрос уже отправлен"

            if PaymentRequest.objects.filter(boat=boat, payed=True):
                message = "Заявление уже оплачено"

            if boat.status == "wait" or boat.status == "look":
                message = "Заявление еще не прошло проверку"

            messages.add_message(request, messages.WARNING, message)
            return redirect("main:boat_requests")

        pay_request = PaymentRequest(boat=boat, owner=boat.owner, check_scan=request.FILES['checkScan'])
        boat.change_status("payment_check")
        pay_request.save()

        messages.add_message(request, messages.SUCCESS, "Запрос отправлен и ожидает проверки")
        return redirect("main:boat_requests")


class PayFine(UserView):
    def post(self, request, pk):
        fine = get_object_or_404(Fine, pk=pk)

        if fine.payed:
            messages.add_message(request, messages.WARNING, "Штраф уже оплачен")
            return redirect("main:fines")

        check_scan = request.FILES.get("checkScan")
        if not check_scan:
            messages.add_message(request, messages.WARNING, "Необходим скан чека!")
            return redirect("main:fines")

        if fine.inspecting:
            messages.add_message(request, messages.WARNING, "Оплата находится на проверке!")
            return redirect("main:fines")

        fine.inspecting = True
        fine.save()

        FinePaymentRequest(fine=fine, check_scan=check_scan).save()

        messages.add_message(request, messages.SUCCESS, "Оплата отправлена на проверку!")
        return redirect("main:fines")


# Inspector views
class InspectorMixin(UserMixin):
    def handle_basic_user(self):
        return redirect("main:index")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_not_authenticated()

        if not request.user.is_inspector:
            return self.handle_basic_user()

        if request.user.is_superuser:
            return self.handle_user_admin()

        return super(AccessMixin, self).dispatch(request, *args, **kwargs)


class InspectorView(InspectorMixin, View):
    def get_context_with_extra_data(self, context):
        fines_payments = FinePaymentRequest.objects.filter(payed=False, inspecting=True).count()
        registration_payments = PaymentRequest.objects.filter(payed=False, rejected=False).count()
        tech_check_payments = TechCheckRequest.objects.filter(payed=False, inspecting=True).count()

        context['waiting_requests_count'] = Boat.objects.filter(status="wait").count()
        context['payment_requests_count'] = fines_payments + registration_payments + tech_check_payments
        context['remove_requests_count'] = RemoveRequest.objects.all().count()

        return context


def search_boat_by_owner(full_name, filtered_boats):
    owners = Owner.objects.annotate(full_name=Concat("first_name", V(" "), "last_name")). \
        filter(full_name__icontains=full_name)

    boats_copy = filtered_boats.all()
    boats = []

    for owner in owners:
        boats += list(boats_copy.filter(owner_id=owner.id))

    return boats


class Inspector(InspectorView):
    def get(self, request):
        waiting_requests = Boat.objects.filter(status="wait").order_by("-pk")
        context = self.get_context_with_extra_data({"requests": waiting_requests})

        return render(request, "main/inspector.html", context)


class InspectingRequests(InspectorView):
    def get(self, request):
        inspecting_boat_requests = Boat.objects.filter(status="look").order_by("-pk")
        context = self.get_context_with_extra_data({"requests": inspecting_boat_requests})

        return render(request, "main/inspector_inspecting_requests.html", context)


class RequestRemove(InspectorView):
    def get(self, request):
        remove_boat_request = RemoveRequest.objects.all()
        context = self.get_context_with_extra_data({"requests": remove_boat_request})

        return render(request, "main/inspector_remove_requests.html", context)


class AcceptRemoveRequest(InspectorView):
    def get(self, request, pk):
        remove_request = get_object_or_404(RemoveRequest, pk=pk)

        Notification(owner=remove_request.owner,
                     status=models.REMOVE_REQUEST_ACCEPTED,
                     extra_data=remove_request.boat.name).save()

        remove_request.boat.delete()

        messages.add_message(request, messages.SUCCESS, "Судно успешно снято с учета и удалено с системы!")
        return redirect("main:remove_requests")


class AddRequestsToLooking(InspectorView):
    def post(self, request):
        waiting_requests_ids = request.POST.getlist("request")

        for request_id in waiting_requests_ids:
            boat = Boat.objects.get(id=request_id)
            boat.change_status("look")

        if waiting_requests_ids:
            messages.add_message(request, messages.SUCCESS, "Добавлено в 'рассматриваемые'")

        return redirect("main:inspector")


class RegistrationRequest(InspectorView):
    def get(self, request, pk):
        boat = get_object_or_404(Boat, pk=pk)
        if boat.status != "look":
            messages.add_message(request, messages.WARNING, "Заявление не находится на рассмотрении")
            return redirect("main:inspector")

        form = BoatForm(instance=boat)

        context = self.get_context_with_extra_data({"form": form})

        return render(request, "main/registration_request.html", context)

    def post(self, request, pk):
        incorrect_fields = request.POST.getlist("incorrect_fields")
        incorrect_fields_json = json.dumps(incorrect_fields)

        boat = get_object_or_404(Boat, pk=pk)
        if boat.status != "look":
            messages.add_message(request, messages.WARNING, "Заявление не находится на рассмотрении")
            return redirect("main:inspector")

        boat.incorrect_fields = incorrect_fields_json
        boat.save()

        status = "payment"

        if incorrect_fields:
            status = "rejected"

        boat.change_status(status)

        return redirect("main:inspecting_requests")


class PaymentRequests(InspectorView):
    def get(self, request):
        payments = PaymentRequest.objects.filter(payed=False, rejected=False)
        fine_payments = FinePaymentRequest.objects.filter(inspecting=True, payed=False)
        tech_check_payments = TechCheckRequest.objects.filter(payed=False, inspecting=True)

        context = self.get_context_with_extra_data({
            "payments": payments,
            "fine_payments": fine_payments,
            "tech_check_payments": tech_check_payments
        })

        return render(request, "main/inspector_payments.html", context)


class AcceptPayment(InspectorView):
    def post(self, request, pk):
        payment = get_object_or_404(PaymentRequest, pk=pk)
        payment.payed = True
        payment.save()

        payment.boat.change_status("inspector_check")
        notification = Notification(owner=payment.owner, boat=payment.boat, status="inspector_check")
        notification.extra_data = request.POST["address"]
        notification.save()

        messages.add_message(request, messages.SUCCESS, "Оплата принята и пользователь уведомлен!")
        return redirect("main:payment_requests")


class RejectPayment(InspectorView):
    def get(self, request, pk):
        payment = get_object_or_404(PaymentRequest, pk=pk)
        payment.rejected = True
        payment.save()

        payment.boat.change_status("payment_rejected")

        messages.add_message(request, messages.SUCCESS, "Оплата отклонена и пользователь уведомлен!")
        return redirect("main:payment_requests")


class PayedRequests(InspectorView):
    def get(self, request):
        full_name = request.GET.get("full_name", "")
        imo = request.GET.get("imo", "")
        engine_number = request.GET.get("engine_number", "")

        boats = Boat.objects.filter(
            status="inspector_check",
            imo__icontains=imo,
            engine_number__icontains=engine_number
        )

        if request.GET.get("full_name"):
            boats = search_boat_by_owner(full_name, boats)

        context = self.get_context_with_extra_data({
            "requests": boats,
            "full_name": full_name,
            "imo": imo,
            "engine_number": engine_number
        })

        return render(request, "main/inspector_payed_requests.html", context)


class FinalBoatCheck(InspectorView):
    def get(self, request, pk):
        boat = get_object_or_404(Boat, pk=pk)

        if boat.status != "inspector_check":
            messages.add_message(request, messages.WARNING, "Судно еще не прошло оплату")
            return redirect("main:payed_requests")

        form = BoatForm(instance=boat)

        context = self.get_context_with_extra_data({"form": form})
        return render(request, "main/inspector_final_boat_check.html", context)

    def post(self, request, pk):
        boat = get_object_or_404(Boat, pk=pk)

        print(request.POST)

        if boat.status != "inspector_check":
            messages.add_message(request, messages.WARNING, "Судно еще не прошло оплату")
            return redirect("main:payed_requests")

        form = BoatForm(request.POST, instance=boat)

        if form.is_valid():
            boat = form.save(commit=False)
            boat.change_status("accepted")
            boat.save()

            messages.add_message(request, messages.SUCCESS, "Судно успешно зарегестрировано в системе")
            return redirect("main:payed_requests")

        messages.add_message(request, messages.ERROR, "Некоторые поля заполнены неверно")
        return redirect("main:final_boat_check", pk=pk)


class AcceptBoat(InspectorView):
    def get(self, request, pk):
        boat = get_object_or_404(Boat, pk=pk)

        if boat.status != "inspector_check":
            messages.add_message(request, messages.WARNING, "Судно еще не прошло оплату")
            return redirect("main:inspector")

        boat.status = "accepted"
        boat.save()

        messages.add_message(request, messages.SUCCESS, "Судно успешно зарегестрировано в системе!")
        return redirect("main:payed_requests")


class AddFine(InspectorView):
    def get(self, request):
        full_name = request.GET.get("full_name", "")
        imo = request.GET.get("imo", "")
        engine_number = request.GET.get("engine_number", "")

        boats = []
        if full_name or imo or engine_number:
            boats = Boat.objects.filter(
                status="accepted",
                imo__icontains=imo,
                engine_number__icontains=engine_number
            )

            if request.GET.get("full_name"):
                boats = search_boat_by_owner(full_name, boats)

        context = self.get_context_with_extra_data({
            "boats": boats,
            "full_name": full_name,
            "imo": imo,
            "engine_number": engine_number
        })

        return render(request, "main/inspector_add_fine.html", context)

    def post(self, request):
        boat = get_object_or_404(Boat, pk=request.POST['boat_id'])
        if boat.status != "accepted":
            return HttpResponseNotFound("not found")

        Fine(
            owner=boat.owner,
            boat=boat,
            reason=request.POST.get("reason"),
            amount=request.POST.get("amount")
        ).save()

        context = self.get_context_with_extra_data({})

        messages.add_message(request, messages.SUCCESS, "Нарушение зарегистрировано и отправлено пользователю")
        return render(request, "main/inspector_add_fine.html", context)


class AcceptFinePayment(InspectorView):
    def get(self, request, pk):
        fine_payment = get_object_or_404(FinePaymentRequest, pk=pk)
        if fine_payment.payed:
            messages.add_message(request, messages.SUCCESS, "Нарушение уже оплачено")
            return redirect("main:payment_requests")

        fine_payment.payed = True
        fine_payment.inspecting = False
        fine_payment.save()

        fine_payment.fine.payed = True
        fine_payment.fine.inspecting = False
        fine_payment.fine.save()

        messages.add_message(request, messages.SUCCESS, "Оплата принята!")
        return redirect("main:payment_requests")


class RejectFinePayment(InspectorView):
    def get(self, request, pk):
        fine_payment = get_object_or_404(FinePaymentRequest, pk=pk)
        if fine_payment.payed:
            messages.add_message(request, messages.SUCCESS, "Нарушение уже оплачено")
            return redirect("main:payment_requests")

        fine_payment.inspecting = False
        fine_payment.save()

        fine_payment.fine.inspecting = False
        fine_payment.fine.save()

        messages.add_message(request, messages.SUCCESS, "Оплата отклонена!")
        return redirect("main:payment_requests")


class AcceptTechCheckPayment(InspectorView):
    def post(self, request, pk):
        tech_check_request = get_object_or_404(TechCheckRequest, pk=pk)
        if tech_check_request.payed:
            messages.add_message(request, messages.WARNING, "Заявление уже принято!")
            return redirect("main:payment_requests")

        tech_check_request.payed = True
        tech_check_request.inspecting = False
        tech_check_request.save()

        Notification(owner=tech_check_request.owner, boat=tech_check_request.boat,
                     status=models.TECH_CHECK_PAYMENT_ACCEPTED,
                     extra_data=request.POST['address']).save()

        messages.add_message(request, messages.SUCCESS, "Оплата принята!")
        return redirect("main:payment_requests")


class RejectTechCheckPayment(InspectorView):
    def get(self, request, pk):
        tech_check_request = get_object_or_404(TechCheckRequest, pk=pk)
        if tech_check_request.payed:
            messages.add_message(request, messages.WARNING, "Заявление уже принято!")
            return redirect("main:payment_requests")

        tech_check_request.inspecting = False
        tech_check_request.save()

        Notification(owner=tech_check_request.owner, boat=tech_check_request.boat,
                     status=models.TECH_CHECK_PAYMENT_REJECTED).save()

        messages.add_message(request, messages.SUCCESS, "Оплата отклонена!")
        return redirect("main:payment_requests")


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

        messages.add_message(request, messages.ERROR, "Неверный e-адрес или пароль")
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
            messages.add_message(request, messages.ERROR, "Пользователь с таким эл. адресом уже зарегестрирован")
            return render(request, self.template_name, {"form": form})

        user_with_same_number = Owner.objects.filter(phone_number=request.POST['phone_number'])
        if user_with_same_number:
            messages.add_message(request, messages.ERROR, "Пользователь с таким номером телефона уже зарегестрирован")
            return render(request, self.template_name, {"form": form})

        messages.add_message(request, messages.ERROR, "Произошла какая-то ошибка")
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
            messages.add_message(request, messages.ERROR, "Пользователь с таким эл. адресом уже зарегестрирован")
            return render(request, self.template_name, {"form": form})

        user_with_same_number = Owner.objects.filter(phone_number=request.POST['phone_number'])
        if user_with_same_number is not request.user:
            messages.add_message(request, messages.ERROR, "Пользователь с таким номером телефона уже зарегестрирован")
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

            messages.add_message(request, messages.ERROR, "Неверный код")
            return render(request, "main/activation.html", {})

        return redirect("main:login")


def reactivate(request):
    if not request.user.is_authenticated:
        return redirect("main:login")

    request.user.activation_code = randint(1000, 9999)
    request.user.save()

    send_sms(request.user.phone_number, message=str(request.user.activation_code))

    return redirect("main:activate_account")
