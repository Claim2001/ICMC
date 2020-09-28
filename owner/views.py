from django.shortcuts import render
from .forms import UserForm
from django.shortcuts import render, redirect, get_object_or_404
from random import randint
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from main.helpers import send_sms
from .models import Owner
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


class SignUp(View):
    template_name = "main/signup.html"

    def get(self, request):
        form = UserForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = UserForm(request.POST)
        display_type = request.POST.get("display_type", None)
        if form.is_valid() and display_type in ["public_offer"]:
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

        if not display_type in ["public_offer"]:
            messages.add_message(request, messages.ERROR, "Публичная оферта не была соглашена вами")
            return render(request, self.template_name, {"form": form})

        messages.add_message(request, messages.ERROR, "Произошла какая-то ошибка")
        return render(request, self.template_name, {"form": form})


class UserEdit(LoginRequiredMixin, View):
    template_name = "main/edit_user.html"

    def get(self, request):
        if request.user.activated:
            return redirect("boat:index")

        form = UserForm(instance=request.user)

        context = {
            "form": form
        }

        return render(request, self.template_name, context)

    def post(self, request):
        if request.user.activated:
            return redirect("boat:index")

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