from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .models import *

# Create your views here.
from django.urls import reverse


def index(request):
    return render(request, "healthtracker/index.html")

def login_view(request):
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
            return render(request, "healthtracker/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "healthtracker/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def checkhealth(request):
    if request.method == 'POST':
        regnumber = request.POST["regnumber"]
        try:
            pateint = Patients.objects.get(RegNumber=regnumber)
        except Patients.DoesNotExist:
            pateint = None
        if pateint != None:
            data = PatientsStatus.objects.filter(Patient=pateint).order_by('-Time')
        else:
            data = []
        return render(request, "healthtracker/pateintprofile.html", {
            "data": data
        })
    else:
        return render(request, "healthtracker/chekhealth.html")
