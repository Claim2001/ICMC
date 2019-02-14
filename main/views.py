from django.shortcuts import render, redirect
from django.http import HttpResponse, QueryDict
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


def remove_useless_elements_from_post(post):
    """
    I wrote this function because I wanted to 
    use nice ```user = Owner(**post)``` syntax instead
    of extracting every field one by one but 
    ```request.POST``` has a bunch of elements
    that should not be passed as arguments when create
    an instance of a model
    """
    post_copy = post.copy()

    post_copy.pop("csrfmiddlewaretoken")
    post_copy.pop("password")

    qdict = QueryDict('', mutable=True)
    qdict.update(post_copy)

    return qdict


class SignUp(View):
    def get(self, request):
        return render(request, "main/signup.html", {})

    def post(self, request):
        post = remove_useless_elements_from_post(request.POST)
        user = Owner(**post)

        password = request.POST['password']
        user.set_password(password)

        user.save()

        login(request, user)

        return redirect("main:index")
