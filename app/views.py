from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Patient
from django.db import IntegrityError
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect, HttpRequest
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request:HttpRequest):
    return render(request, "app/index.html")


def login_view(request:HttpRequest):
    if request.user.is_anonymous:
        if request.method == "POST":


            # Attempt to sign user in
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)

            # Check if authentication successful
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "app/login.html", {
                    "message": "Invalid username and/or password."
                })
        return render(request, "app/login.html")
    return redirect("index")


def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirm"]
        if password != confirmation:
            return render(request, "app/signup.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = Patient.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "app/signup.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return redirect("index")
    return render(request, "app/signup.html")

def logout_view(request:HttpRequest):
    logout(request)
    return redirect("index")