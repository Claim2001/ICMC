import json
from random import randint
from django.http import HttpResponseNotFound
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Value as V
from django.db.models.functions import Concat
from django.conf.urls import url
from . import models
from .models import Boat, Fine, RemoveRequest, TechCheckRequest, PaymentRequest, FinePaymentRequest
from .helpers import send_sms
from owner.models import Owner


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


def logout_user(request):
    logout(request)
    return redirect("main:login")


# Inspector views
class InspectorMixin(UserMixin):
    def handle_basic_user(self):
        return redirect("boat:index")

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
        boats += list(boats_copy.filter(status="accepted", owner_id=owner.id))

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


class AllBoats(InspectorView):
    def get(self, request):
        full_name = request.GET.get("full_name", "")
        imo = request.GET.get("imo", "")
        engine_number = request.GET.get("engine_number", "")

        if full_name or imo or engine_number:
            boats = Boat.objects.filter(
                status="accepted",
                imo__icontains=imo,
                engine_number__icontains=engine_number
            )

            if request.GET.get("full_name"):
                boats = search_boat_by_owner(full_name, boats)
        else:
            boats = Boat.objects.filter(status="accepted").order_by("-id")[:20]

        context = self.get_context_with_extra_data({
            "boats": boats,
            "full_name": full_name,
            "imo": imo,
            "engine_number": engine_number
        })

        return render(request, "main/inspector_all_boats.html", context)


class Login(View):
    def get(self, request):
        return render(request, "main/login.html", {})

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']

        authenticated_user = authenticate(username=email, password=password)

        if authenticated_user:
            login(request, authenticated_user)
            return redirect("boat:index")

        messages.add_message(request, messages.ERROR, "Неверный эл. адрес или пароль")
        return render(request, "main/login.html", {"email": email})


class Public_offer(View):
    def get(self, request):
        return render(request, "main/offer.html")


class ActivateAccount(View):
    def get(self, request):
        if request.user.is_authenticated and not request.user.activated:
            if request.user.is_inspector:
                return redirect("main:inspector")

            return render(request, "main/activation.html", {})

        return redirect("boat:index")

    def post(self, request):
        if request.user.is_authenticated:
            if request.POST['activation_code'].isdigit():
                user_code = int(request.POST['activation_code'])
                if request.user.activation_code == user_code:
                    if self.request.recaptcha_is_valid:
                        user = Owner.objects.get(email=request.user.email)
                        user.activated = True
                        user.save()

                        return redirect("boat:index")
                    messages.add_message(request, messages.ERROR, "Неверная капча")
                    return render(request, "main/activation.html", {})
                messages.add_message(request, messages.ERROR, "Неверный код")
                return render(request, "main/activation.html", {})
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
