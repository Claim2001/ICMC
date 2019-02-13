from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View


def index(request):
    if request.user.is_authenticated:
        if request.user.is_inspector:
            # redirect to inpector page
            return HttpResponse("Inspector!")

        # redirect to user page
        return HttpResponse("Authenticated user!")

    return redirect("main:login")


class Login(View):
    def get(self, request):
        return render(request, "main/login.html", {})

    def post(self, request):
        return HttpResponse("soon...")