from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import Boat, Notification, Fine
from .forms import UserForm, BoatForm


class IndexView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_inspector:
                return redirect("main:inspector")

            if request.user.is_superuser:
                return HttpResponseRedirect("/admin")

            form = BoatForm()

            context = {
                "user": request.user,
                "form": form
            }

            return render(request, "main/register_boat.html", context)

        return redirect("main:login")

    def post(self, request):
        if request.user.is_authenticated:
            form = BoatForm(request.POST, request.FILES)
            if form.is_valid():
                boat = form.save(commit=False)
                boat.owner = request.user
                boat.save()
                
                return redirect("main:boat_requests")
            
            else:
                return redirect("main:index")
        
        return redirect("main:login")


def logout_user(request):
    logout(request)
    return redirect("main:login")


def inspector_page(request):
    if not request.user.is_authenticated:
        return redirect("main:login")

    if not request.user.is_inspector:
        return redirect("main:index")

    waiting_requests = Boat.objects.filter(status="wait")

    context = {
        "requests": waiting_requests
    }

    return render(request, "main/inspector.html", context)


def boat_request(request, pk):
    if not request.user.is_authenticated:
        return redirect("main:login")

    boat = get_object_or_404(Boat, pk=pk)

    if request.user.is_inspector:
        # notify user that his request is inspected now
        notification = Notification(owner=boat.owner, boat=boat)
        notification.save()

    return render(request, "main/request.html", {"request": boat})


# TODO: that's going to be notifications
def user_boat_requests(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(owner=request.user)
        return render(request, "main/user_requests.html", {"boats": boats})

    return redirect("main:login")


def boats(request):
    if request.user.is_authenticated:
        boats = Boat.objects.filter(owner=request.user)
        return render(request, "main/user_boats.html", {"boats": boats})
    
    return redirect("main:login")


def fines(request):
    if request.user.is_authenticated:
        fines = Fine.objects.filter(owner=request.user)
        return render(request, "main/user_fines.html", {"fines": fines})
        
    return redirect("main:login")


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
        
        messages.add_message(request, messages.ERROR, "Login or password is wrong")
        return redirect("main:login")


class SignUp(View):
    def get(self, request):
        form = UserForm()
        return render(request, "main/signup.html", {"form": form})

    def post(self, request):
        form = UserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password'])
            user.save()

            login(request, user)

            return redirect("main:index")

        messages.add_message(request, messages.INFO, "User with this email exists")
        return render(request, "main/signup.html", {"form": form})


class RegisterBoat(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, "main/register_boat.html", {})

        return redirect("main:login")

    def post(self, request):
        if request.user.is_authenticated:
            form = BoatForm(request.POST or None)
            if form.is_valid():
                boat = form.save(commit=False)
                boat.owner = request.user
                boat.save()
                
                return redirect("main:index")
        
        return redirect("main:login")
