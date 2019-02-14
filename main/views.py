from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth import authenticate, login

from .models import Owner
from .forms import UserForm


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
        email = request.POST['email']
        password = request.POST['password']

        user = Owner.objects.get(email=email)
        user_authenticated = authenticate(username=user.username, password=password)
        
        if user_authenticated:
            login(request, user_authenticated)
            return redirect("main:index")
        
        return redirect("main:login")


class SignUp(View):
    def get(self, request):
        return render(request, "main/signup.html", {})

    def post(self, request):
        # wtf is this? Didn't find a better solution :(
        username = request.POST['username']
        second_name = request.POST['second_name']
        gender = request.POST['gender']
        organization_name = request.POST['organization_name']
        address = request.POST['address']
        mail_index = request.POST['mail_index']
        date_of_passport = request.POST['date_of_passport']
        inn = request.POST['inn']
        country = request.POST['country']
        city = request.POST['city']
        email = request.POST['email']
        phone_number = request.POST['phone_number']

        user = Owner(
            username=username,
            second_name=second_name,
            gender=gender,
            name_of_organization=organization_name,
            address=address,
            mail_index=mail_index,
            date_of_passport=date_of_passport,
            inn=inn,
            country=country,
            city=city,
            email=email,
            phone_number=phone_number
        )

        user.save()

        return render(request, "main/signup.html", {})