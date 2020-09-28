from django.shortcuts import render
from main.views import InspectorView
from .forms import BoatForm
from notification.views import UserView
from django.http import HttpResponseNotFound
import json
from .models import Boat
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404


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
            if self.request.recaptcha_is_valid:
                boat = form.save(commit=False)
                boat.owner = request.user
                boat.save()

                messages.add_message(request, messages.SUCCESS, "Ваше заявление принято и находится в очереди")
                return redirect("boat:index")
            messages.add_message(request, messages.ERROR, "Капча не выполнена или была выполнена неправильно")
            return redirect("boat:index")
        messages.add_message(request, messages.WARNING, "Произошла какая-то ошибка")
        return redirect("boat:index")


class EditRequest(UserView):
    def get(self, request, pk):
        boat = get_object_or_404(Boat, owner=request.user, pk=pk)

        if boat.status == "looking":
            messages.add_message(request, messages.WARNING, "Вы не можете изменять заявления, которые находятся на "
                                                            "рассмотрении")
            return redirect("notification:boat_requests")

        form = BoatForm(instance=boat)
        context = self.get_context_with_extra_data({"form": form})

        return render(request, "main/boat_form.html", context)

    def post(self, request, pk):
        boat = get_object_or_404(Boat, owner=request.user, pk=pk)
        form = BoatForm(request.POST, request.FILES, instance=boat)

        if form.is_valid():
            if self.request.recaptcha_is_valid:
                edited_boat = form.save(commit=False)
                edited_boat.change_status("wait")
                edited_boat.save()

                messages.add_message(request, messages.SUCCESS, "Ваше заявление принято и повторно отправлено!")
            messages.add_message(request, messages.ERROR, "Капча неверна или была заполнена неправильно")
            return redirect("notification:boat_requests")
        else:
            messages.add_message(request, messages.ERROR, "Что-то пошло не так")

        return redirect("notification:boat_requests")


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


class FinalBoatCheck(InspectorView):
    def get(self, request, pk):
        boat = get_object_or_404(Boat, pk=pk)

        if boat.status != "inspector_check":
            messages.add_message(request, messages.WARNING, "Судно еще не прошло оплату")
            return redirect("main:inspector_boats")

        form = BoatForm(instance=boat)

        context = self.get_context_with_extra_data({"form": form})
        return render(request, "main/inspector_final_boat_check.html", context)

    def post(self, request, pk):
        boat = get_object_or_404(Boat, pk=pk)

        print(request.POST)

        if boat.status != "inspector_check":
            messages.add_message(request, messages.WARNING, "Судно еще не прошло оплату")
            return redirect("main:inspector_boats")

        form = BoatForm(request.POST, instance=boat)

        if form.is_valid():
            boat = form.save(commit=False)
            boat.change_status("accepted")
            boat.save()

            messages.add_message(request, messages.SUCCESS, "Судно успешно зарегестрировано в системе")
            return redirect("main:inspector_boats")

        messages.add_message(request, messages.ERROR, "Некоторые поля заполнены неверно")
        return redirect("boat:final_boat_check", pk=pk)


class InspectorBoat(InspectorView):
    def get(self, request, pk):
        boat = get_object_or_404(Boat, pk=pk)
        form = BoatForm(instance=boat)

        context = self.get_context_with_extra_data({"form": form})

        return render(request, "main/inspector_boat.html", context)