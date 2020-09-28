from django.shortcuts import render
from main.views import UserMixin
from django.views.generic import View
from .models import Notification
from main.models import Fine, RemoveRequest, TechCheckRequest
from django.http import HttpResponseNotFound
from boat.models import Boat
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages


class UserView(UserMixin, View):
    login_url = "/login"

    def get_context_with_extra_data(self, context):
        context["notifications_count"] = Notification.objects.filter(watched=False, owner=self.request.user).count()
        context["fines_count"] = Fine.objects.filter(owner=self.request.user, payed=False, inspecting=False).count()

        return context


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

            remove_request = RemoveRequest(owner=boat.owner, boat=boat, reason=reason, ticket=ticket)
            remove_request.save()

            messages.add_message(request, messages.SUCCESS, "Ваше заявление на снятие судна с учета отправлено!")

        else:
            messages.add_message(request, messages.WARNING, "Ваше заявление на снятие судна с учета уже отправлено!")

        return redirect("notification:boats")


class TechCheckView(UserView):
    type = ""

    def post(self, request, pk):
        boat = get_object_or_404(Boat, pk=pk)

        if boat.status != "accepted":
            messages.add_message(request, messages.WARNING, "Судно еще не зарегистрировано в системе")
            return redirect("notification:boats")

        if TechCheckRequest.objects.filter(boat=boat, check_type=self.type, inspecting=True):
            messages.add_message(request, messages.WARNING, "Заявление на техосмотр уже находится в очереди")
            return redirect("notification:boats")

        tech_check_request = TechCheckRequest(owner=boat.owner, boat=boat, check_scan=request.FILES['checkScan'],
                                              check_type=self.type)
        tech_check_request.save()

        messages.add_message(request, messages.SUCCESS, "Заявление на техосмотр принято и находится в очереди")
        return redirect("notification:boats")


class FirstTechCheck(TechCheckView):
    type = "first"


class YearTechCheck(TechCheckView):
    type = "year"