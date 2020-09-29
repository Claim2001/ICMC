from boat.models import Boat
from addrequestions.views import InspectorView, search_boat_by_owner
from .models import Fine, FinePaymentRequest
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages


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
            return redirect("addrequestions:payment_requests")

        fine_payment.payed = True
        fine_payment.inspecting = False
        fine_payment.save()

        fine_payment.fine.payed = True
        fine_payment.fine.inspecting = False
        fine_payment.fine.save()

        messages.add_message(request, messages.SUCCESS, "Оплата принята!")
        return redirect("addrequestions:payment_requests")


class RejectFinePayment(InspectorView):
    def get(self, request, pk):
        fine_payment = get_object_or_404(FinePaymentRequest, pk=pk)
        if fine_payment.payed:
            messages.add_message(request, messages.SUCCESS, "Нарушение уже оплачено")
            return redirect("addrequestions:payment_requests")

        fine_payment.inspecting = False
        fine_payment.save()

        fine_payment.fine.inspecting = False
        fine_payment.fine.save()

        messages.add_message(request, messages.SUCCESS, "Оплата отклонена!")
        return redirect("addrequestions:payment_requests")